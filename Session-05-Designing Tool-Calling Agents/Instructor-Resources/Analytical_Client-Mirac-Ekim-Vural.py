import asyncio
import json
import sys
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

llm = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

async def chat_session():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["analytical_server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            mcp_tools = await session.list_tools()
            
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema if hasattr(t, "inputSchema") else t.input_schema
                    }
                }
                for t in mcp_tools.tools
            ]

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an analytical assistant connected to a DuckDB data warehouse via MCP tools. "
                        "When asked data questions, check the schema or summarize tables if necessary, "
                        "and run aggregated SQL queries rather than requesting raw rows. "
                        "Once you receive tool results, provide a clear direct answer to the user."
                    )
                }
            ]

            print("\nAnalytical Assistant initialized. Type 'exit' or 'quit' to end.\n")

            while True:
                try:
                    user_input = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nExiting session.")
                    break

                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit"):
                    print("Exiting session.")
                    break

                messages.append({"role": "user", "content": user_input})

                while True:
                    response = await llm.chat.completions.create(
                        model="llama3.1",
                        messages=messages,
                        tools=openai_tools,
                        temperature=0
                    )

                    response_message = response.choices[0].message
                    messages.append(response_message.model_dump(exclude_unset=True))

                    if not response_message.tool_calls:
                        print(f"\nAssistant: {response_message.content}\n")
                        break

                    for tool_call in response_message.tool_calls:
                        func_name = tool_call.function.name
                        func_args = json.loads(tool_call.function.arguments)

                        print(f"\n[Invoking tool: {func_name} with args: {func_args}]")
                        
                        tool_output = await session.call_tool(func_name, arguments=func_args)
                        
                        output_texts = [
                            item.text for item in tool_output.content 
                            if hasattr(item, "text")
                        ]
                        raw_result = "\n".join(output_texts) if output_texts else str(tool_output)

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": raw_result
                        })

if __name__ == "__main__":
    asyncio.run(chat_session())
