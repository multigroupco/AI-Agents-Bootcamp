import asyncio
import duckdb
import polars as pl
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("analytical_engine")
db = duckdb.connect(":memory:")

class QueryConfig(BaseModel):
    sql_query: str = Field(..., description="DuckDB SQL query to execute")
    return_format: str = Field(default="json", description="Output format: 'json' or 'markdown'")

def initialize_data_lake():
    df = pl.DataFrame({
        "transaction_id": range(1, 100001),
        "user_id": [i % 5000 for i in range(100000)],
        "amount": [x * 1.15 for x in range(100000)],
        "status": ["COMPLETED", "PENDING", "FAILED", "REFUNDED"] * 25000
    })
    arrow_table = df.to_arrow()
    db.register("transactions", arrow_table)

@mcp.tool()
def get_database_schema() -> str:
    try:
        result_df = db.execute("DESCRIBE;").pl()
        return result_df.write_json()
    except Exception as e:
        return f'{{"error": "{str(e)}" }}'

@mcp.tool()
def execute_analytical_query(config: QueryConfig) -> str:
    try:
        result_df = db.execute(config.sql_query).pl()
        if config.return_format == "markdown":
            return result_df.to_pandas().to_markdown(index=False)
        return result_df.write_json()
    except duckdb.Error as e:
        return f'{{"error": "DuckDB execution failed", "details": "{str(e)}" }}'
    except Exception as e:
        return f'{{"error": "System fault", "details": "{str(e)}" }}'

@mcp.tool()
def get_table_summary(table_name: str) -> str:
    try:
        result_df = db.execute(f"SUMMARIZE {table_name};").pl()
        return result_df.write_json()
    except duckdb.Error as e:
        return f'{{"error": "Failed to summarize table", "details": "{str(e)}" }}'

@mcp.tool()
def get_row_count(table_name: str) -> str:
    try:
        result = db.execute(f"SELECT COUNT(*) as count FROM {table_name};").fetchone()
        return f'{{"table": "{table_name}", "row_count": {result[0]} }}'
    except duckdb.Error as e:
        return f'{{"error": "Failed to count rows", "details": "{str(e)}" }}'

if __name__ == "__main__":
    initialize_data_lake()
    mcp.run(transport="stdio")
