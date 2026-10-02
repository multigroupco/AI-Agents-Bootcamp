(function(root){
'use strict';
const companies=[
 {id:'atlas',name:'Atlas Yazılım',sector:'Kurumsal yazılım',unit:'milyon USD',years:[{year:2022,revenue:820,profit:98},{year:2023,revenue:990,profit:139},{year:2024,revenue:1188,profit:190}],notes:['Abonelik gelirleri büyümeyi destekliyor.','Yeni pazarlara giriş satış giderlerini artırıyor.'],risks:['Büyük müşterilerde gelir yoğunlaşması','Bulut altyapı maliyetleri'],source:'DEMO-FIN-01'},
 {id:'nova',name:'Nova Teknoloji',sector:'Kurumsal yazılım',unit:'milyon USD',years:[{year:2022,revenue:700,profit:84},{year:2023,revenue:840,profit:101},{year:2024,revenue:924,profit:92}],notes:['Gelir artarken net kâr son yılda geriliyor.','Ürün geçişi kısa vadede gider yaratıyor.'],risks:['Ürün geçişinde müşteri kaybı','Fiyat rekabeti'],source:'DEMO-FIN-02'}
];
function finance(id){
 const c=companies.find(x=>x.id===id);if(!c)throw Error('Şirket bulunamadı');
 const rows=c.years.map((x,i)=>({...x,margin:x.profit/x.revenue*100,growth:i?(x.revenue/c.years[i-1].revenue-1)*100:null,source:c.source+' / '+x.year}));
 return {company:c,rows,cagr:((rows.at(-1).revenue/rows[0].revenue)**(1/(rows.length-1))-1)*100,trace:['Şirket ve örnek kayıt seçildi: '+c.source,'Gelir ve net kâr sayısal alanlardan okundu.','Büyüme, net kâr marjı ve CAGR kodla hesaplandı.','Her yıl kendi veri satırıyla eşleştirildi.']};
}
const today='2018-09-01';
const orders=[
 {id:'DEMO-1001',owner:'ayse',item:'Kablosuz kulaklık',status:'delivered',purchase:'2018-08-10',delivered:'2018-08-25',estimated:'2018-08-20',price:240,freight:20},
 {id:'DEMO-1002',owner:'ayse',item:'Çalışma sandalyesi',status:'delivered',purchase:'2018-07-15',delivered:'2018-08-12',estimated:'2018-07-30',price:620,freight:80},
 {id:'DEMO-1003',owner:'ayse',item:'Masa lambası',status:'shipped',purchase:'2018-08-26',delivered:null,estimated:'2018-09-04',price:150,freight:15},
 {id:'DEMO-2001',owner:'deniz',item:'Kahve makinesi',status:'delivered',purchase:'2018-08-18',delivered:'2018-08-26',estimated:'2018-08-27',price:400,freight:25},
 {id:'DEMO-1004',owner:'ayse',item:'Bluetooth hoparlör',status:'delivered',purchase:'2018-08-01',delivered:'2018-08-18',estimated:'2018-08-17',price:350,freight:30}
];
const diff=(a,b)=>(Date.parse(a+'T00:00:00Z')-Date.parse(b+'T00:00:00Z'))/86400000;
function refund(orderId,reason,requests=[]){
 const o=orders.find(x=>x.id===orderId&&x.owner==='ayse'&&x.purchase<today);
 const trace=['Oturum: örnek müşteri Ayşe; rol değişikliği metinden alınmaz.'];
 if(!o)return {code:'NOT_FOUND',label:'Sipariş bulunamadı',amount:0,canRequest:false,trace:[...trace,'R0/R1: kayıt yok veya oturuma ait değil.']};
 const base={order:o,amount:0,canRequest:false,trace};trace.push('R1: sipariş oturumdaki müşteriye ait.');
 if(!['changed_mind','damaged','wrong_item','late'].includes(reason))return {...base,code:'INVALID_REASON',label:'İade nedeni seçin'};
 if(['created','approved','invoiced','processing'].includes(o.status))return {...base,code:'NOT_DELIVERED_CANCELLABLE',label:'Teslim edilmedi; iptal yolu kullanılmalı'};
 if(o.status==='shipped'||(o.delivered&&o.delivered>today))return {...base,code:'IN_TRANSIT',label:'Sipariş yolda',trace:[...trace,'R3: teslim gerçekleşmeden iade talebi açılamaz.']};
 if(['canceled','unavailable'].includes(o.status))return {...base,code:'ALREADY_CLOSED',label:'Sipariş kapanmış'};
 if(!o.delivered)return {...base,code:'NEEDS_HUMAN',label:'Teslim bilgisi eksik; destek incelemeli'};
 if(requests.some(x=>x.orderId===o.id))return {...base,code:'DUPLICATE_REQUEST',label:'Bu sipariş için talep zaten var',trace:[...trace,'R11: ikinci talep açılması engellendi.']};
 const days=diff(today,o.delivered),window=['damaged','wrong_item'].includes(reason)?30:14;
 const eligible=days>=0&&days<=window,late=diff(o.delivered,o.estimated)>=10;
 const freightOnly=!eligible&&late&&days<=30;
 const amount=eligible?o.price+((window===30||late)?o.freight:0):(freightOnly?o.freight:0);
 trace.push(`R6/R7: teslimden ${days} gün geçti; seçilen nedenin penceresi ${window} gün.`, `R9: tahmini teslimden ${diff(o.delivered,o.estimated)} gün sapma; kargo iadesi koşulu ${late?'var':'yok'}.`, `R8: önerilen tutar ${amount.toLocaleString('tr-TR',{minimumFractionDigits:2,maximumFractionDigits:2})} BRL; ${freightOnly?'yalnız kargo':eligible?(amount>o.price?'ürün + kargo':'yalnız ürün bedeli'):'iade hakkı yok'}.`);
 return {...base,trace,days,window,amount,freightOnly,canRequest:amount>0,code:eligible?'ELIGIBLE':'NOT_ELIGIBLE_WINDOW',label:eligible?'İade talebi açılabilir':freightOnly?'Ürün penceresi kapalı; kargo talebi açılabilir':'İade süresi geçmiş',review:amount>500?'PENDING_SENIOR':'PENDING_REVIEW'};
}
function approve(orderId,reason,consent,requests){
 if(consent!==true)throw Error('Talep için açık kullanıcı onayı gerekli.');
 const r=refund(orderId,reason,requests);if(!r.canRequest)throw Error(r.label);
 const request={id:'DEMO-TALEP-'+String(requests.length+1).padStart(3,'0'),orderId,amount:r.amount,status:r.review};requests.push(request);return request;
}
const trials=[
 {id:'DEMO-CT-01',name:'HER2 pozitif meme kanseri örnek protokolü',city:'İstanbul',criteria:[{field:'age',min:18,max:75,label:'18–75 yaş'},{field:'condition',equals:'breast',label:'Meme kanseri'},{field:'her2',equals:'positive',label:'HER2 pozitif'},{field:'stage',equals:'III',label:'Evre III'},{field:'ecog',min:0,max:1,label:'ECOG 0 veya 1'},{field:'brain',equals:'no',label:'Beyin metastazı yok'}]},
 {id:'DEMO-CT-02',name:'HER2 negatif meme kanseri örnek protokolü',city:'Ankara',criteria:[{field:'age',min:18,max:80,label:'18–80 yaş'},{field:'condition',equals:'breast',label:'Meme kanseri'},{field:'her2',equals:'negative',label:'HER2 negatif'},{field:'stage',equals:'III',label:'Evre III'},{field:'ecog',min:0,max:2,label:'ECOG 0–2'}]},
 {id:'DEMO-CT-03',name:'Meme kanseri gözlemsel örnek protokolü',city:'İstanbul',criteria:[{field:'age',min:18,max:85,label:'18–85 yaş'},{field:'condition',equals:'breast',label:'Meme kanseri'},{field:'stage',equals:'III',label:'Evre III'}]}
];
function match(profile){
 return trials.map(t=>{
 const criteria=t.criteria.map(c=>{const v=profile[c.field],missing=v===''||v==null;const met=!missing&&(c.equals!==undefined?v===c.equals:Number.isFinite(Number(v))&&Number(v)>=c.min&&Number(v)<=c.max);return {...c,status:missing?'UNKNOWN':met?'MET':'NOT_MET',evidence:missing?'Profilde belirtilmedi':`${c.field}: ${v}`,source:t.id+' / '+c.label};});
 const counts={MET:0,NOT_MET:0,UNKNOWN:0};criteria.forEach(c=>counts[c.status]++);
 return {...t,criteria,counts,status:counts.NOT_MET?'Uyumsuz kriter var':counts.UNKNOWN?'Eksik bilgi var':'Tanımlı örnek kriterler karşılandı'};
 }).sort((a,b)=>a.counts.NOT_MET-b.counts.NOT_MET||a.counts.UNKNOWN-b.counts.UNKNOWN);
}
const api={companies,finance,today,orders,refund,approve,trials,match,diff};
if(typeof module!=='undefined')module.exports=api;else root.DemoEngine=api;
})(typeof window!=='undefined'?window:globalThis);
