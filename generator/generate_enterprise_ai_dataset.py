from pathlib import Path
import pandas as pd, numpy as np, random, json, shutil

random.seed(42); np.random.seed(42)

# Local Mac paths
project_dir=Path(__file__).resolve().parent.parent
base=project_dir/'enterprise_ai_retail_dataset'
if base.exists(): shutil.rmtree(base)
(base/'data').mkdir(parents=True); (base/'docs').mkdir(); (base/'generator').mkdir()

start=pd.Timestamp('2025-01-01'); end=pd.Timestamp('2026-07-31'); dates=pd.date_range(start,end,freq='D')

countries=np.array(['SE','NO','DK','FI','DE']); probs=np.array([.42,.18,.16,.14,.10])

# customers
n_customers=15000
customers=pd.DataFrame({
 'customer_id':[f'C{i:07d}' for i in range(1,n_customers+1)],
 'country_code':np.random.choice(countries,n_customers,p=probs),
 'signup_date':start+pd.to_timedelta(np.random.randint(0,(end-start).days+1,n_customers),unit='D'),
 'customer_segment':np.random.choice(['new','regular','loyal','vip'],n_customers,p=[.18,.48,.27,.07]),
 'preferred_channel':np.random.choice(['web','mobile_app'],n_customers,p=[.42,.58]),
 'marketing_opt_in':np.random.choice([True,False],n_customers,p=[.68,.32]),
 'age_band':np.random.choice(['18-24','25-34','35-44','45-54','55+'],n_customers,p=[.16,.31,.24,.18,.11])})
customers.to_csv(base/'data/customers.csv',index=False)

# products
cats={'Women':['Dresses','Tops','Jeans','Knitwear','Jackets'],'Men':['Shirts','T-Shirts','Jeans','Knitwear','Jackets'],'Kids':['Tops','Bottoms','Outerwear','Basics','Accessories'],'Home':['Textiles','Kitchen','Storage','Decor','Bathroom'],'Beauty':['Skincare','Haircare','Fragrance','Makeup','Bodycare']}
prange={'Women':(149,1299),'Men':(129,1199),'Kids':(79,699),'Home':(59,899),'Beauty':(49,799)}
prows=[]
for i in range(1,801):
    cat=random.choice(list(cats)); sub=random.choice(cats[cat]); price=round(random.uniform(*prange[cat]),2)
    prows.append([f'P{i:06d}',f'{cat[:2].upper()}-{sub[:3].upper()}-{i:04d}',cat,sub,price,round(price*random.uniform(.28,.52),2),np.random.choice(['core','seasonal','trend'],p=[.55,.3,.15]),np.random.choice(['active','discontinued'],p=[.94,.06])])
products=pd.DataFrame(prows,columns=['product_id','sku','category','subcategory','list_price_sek','unit_cost_sek','product_type','status'])
products.to_csv(base/'data/products.csv',index=False)
active=products[products.status=='active'].reset_index(drop=True)

warehouses=pd.DataFrame([['WH-SE-01','Eskilstuna','SE'],['WH-DE-01','Hamburg','DE'],['WH-DK-01','Copenhagen','DK']],columns=['warehouse_id','city','country_code'])
warehouses.to_csv(base/'data/warehouses.csv',index=False)

stores=pd.DataFrame([['ST-SE-STH-01','Stockholm Flagship','Stockholm','SE'],['ST-SE-GOT-01','Gothenburg Central','Gothenburg','SE'],['ST-NO-OSL-01','Oslo Central','Oslo','NO'],['ST-DK-CPH-01','Copenhagen Central','Copenhagen','DK'],['ST-FI-HEL-01','Helsinki Central','Helsinki','FI'],['ST-DE-BER-01','Berlin Mitte','Berlin','DE']],columns=['store_id','store_name','city','country_code'])
stores.to_csv(base/'data/stores.csv',index=False)

# daily order counts
mult=[]
for d in dates:
    x=1.0
    if d.weekday()>=4:x*=1.15
    if d.month in [11,12]:x*=1.30
    if d.month in [6,7]:x*=1.10
    if d.day in [24,25,26]:x*=1.16
    if d.month==11 and 20<=d.day<=30:x*=1.65
    mult.append(x)
counts=np.array([np.random.poisson(120*m*(1+0.0005*(d-start).days)) for d,m in zip(dates,mult)])
N=int(counts.sum())
order_dates=np.repeat(dates.values,counts)
order_ids=np.array([f'O{i:09d}' for i in range(1,N+1)])
cidx=np.random.randint(0,n_customers,N)
order_cc=customers.country_code.values[cidx]
customer_ids=customers.customer_id.values[cidx]
hours=np.clip(np.random.normal(16,5,N).astype(int),0,23); mins=np.random.randint(0,60,N)
order_ts=pd.to_datetime(order_dates)+pd.to_timedelta(hours,unit='h')+pd.to_timedelta(mins,unit='m')
channel=np.random.choice(['web','mobile_app'],N,p=[.4,.6]); status=np.random.choice(['completed','cancelled'],N,p=[.972,.028])

# order items
nitems=np.random.choice([1,2,3,4],N,p=[.48,.30,.16,.06])
item_order_idx=np.repeat(np.arange(N),nitems)
M=len(item_order_idx)
prod_idx=np.random.randint(0,len(active),M)
qty=np.random.choice([1,2,3],M,p=[.87,.11,.02])
base_price=active.list_price_sek.values[prod_idx]
cost_price=active.unit_cost_sek.values[prod_idx]
item_dates=pd.to_datetime(order_dates[item_order_idx])
rand=np.random.random(M)
disc=np.where((item_dates.month==11)&(item_dates.day>=20)&(item_dates.day<=30),np.random.choice([.15,.2,.25,.3],M,p=[.2,.4,.3,.1]),np.where(rand<.22,np.random.choice([.1,.15,.2],M,p=[.5,.35,.15]),0))
gross=qty*base_price; damt=gross*disc; net=gross-damt; icost=qty*cost_price
items=pd.DataFrame({'order_item_id':[f'OI{i:010d}' for i in range(1,M+1)],'order_id':order_ids[item_order_idx],'product_id':active.product_id.values[prod_idx],'quantity':qty,'unit_price_sek':np.round(base_price,2),'discount_pct':np.round(disc,2),'gross_line_amount_sek':np.round(gross,2),'discount_amount_sek':np.round(damt,2),'net_line_amount_sek':np.round(net,2)})
items.to_csv(base/'data/order_items.csv',index=False)

agg=pd.DataFrame({'idx':item_order_idx,'gross':gross,'disc':damt,'net':net,'cost':icost,'qty':qty}).groupby('idx').sum()
vatmap=pd.Series({'SE':.25,'NO':.25,'DK':.25,'FI':.24,'DE':.19})
vat_rate=vatmap[order_cc].values
source_available=order_ts+pd.to_timedelta(20,unit='m')
incident=(pd.to_datetime(order_ts).date==pd.Timestamp('2026-06-18').date())&(order_cc=='SE')
source_available=pd.Series(source_available)
source_available.loc[incident]=pd.to_datetime(order_ts[incident])+pd.to_timedelta(8.5,unit='h')
orders=pd.DataFrame({'order_id':order_ids,'customer_id':customer_ids,'order_timestamp':order_ts,'source_available_timestamp':source_available.values,'country_code':order_cc,'sales_channel':channel,'order_status':status,'item_quantity':agg.qty.values.astype(int),'gross_revenue_sek':np.round(agg.gross.values,2),'discount_amount_sek':np.round(agg.disc.values,2),'net_revenue_sek':np.round(agg.net.values,2),'vat_amount_sek':np.round(agg.net.values*vat_rate/(1+vat_rate),2),'estimated_cost_sek':np.round(agg.cost.values,2)})
orders.to_csv(base/'data/orders.csv',index=False)

# payments
pay_status=np.where(status=='cancelled','refunded','captured').astype(object)
pay_ts=order_ts+pd.to_timedelta(np.random.randint(0,6,N),unit='m')
pay_inc=(pd.to_datetime(pay_ts).date==pd.Timestamp('2026-03-07').date())
pi=np.where(pay_inc)[0]; chosen=np.random.choice(pi,size=max(1,int(len(pi)*.18)),replace=False); pay_status[chosen]='pending'
payments=pd.DataFrame({'payment_id':[f'PAY{i:09d}' for i in range(1,N+1)],'order_id':order_ids,'payment_method':np.random.choice(['card','klarna','paypal','gift_card'],N,p=[.55,.24,.16,.05]),'payment_status':pay_status,'payment_amount_sek':np.round(agg.net.values,2),'payment_timestamp':pay_ts})
payments.to_csv(base/'data/payments.csv',index=False)

# shipments
comp=np.where(status=='completed')[0]; S=len(comp)
ships_order_ts=pd.to_datetime(order_ts[comp]); ships_cc=order_cc[comp]
wh=np.random.choice(['WH-SE-01','WH-DE-01','WH-DK-01'],S,p=[.52,.32,.16]); carrier=np.random.choice(['DHL','PostNord','Bring','DB Schenker','Budbee'],S,p=[.26,.28,.15,.17,.14])
shipped=ships_order_ts+pd.to_timedelta(np.random.randint(8,36,S),unit='h')
promise_days=pd.Series({'SE':2,'NO':3,'DK':2,'FI':3,'DE':2})[ships_cc].values
promised=ships_order_ts+pd.to_timedelta(promise_days,unit='D')
delay=np.maximum(0,np.random.normal(0,10,S).astype(int)); bf=(ships_order_ts.month==11)&(ships_order_ts.day>=20)&(ships_order_ts.day<=30); delay[bf]+=np.random.randint(0,24,bf.sum())
delivered=promised+pd.to_timedelta(delay-6,unit='h'); min_deliv=shipped+pd.to_timedelta(12,unit='h'); delivered=pd.Series(np.maximum(delivered.values,min_deliv.values))
dh=np.maximum(0,(pd.to_datetime(delivered)-promised).dt.total_seconds()/3600)
post=(ships_order_ts.date>=pd.Timestamp('2026-01-12').date())&(ships_order_ts.date<=pd.Timestamp('2026-01-15').date())&(carrier=='PostNord'); dh=np.asarray(dh); dh[post]+=24; delivered.loc[post]=pd.to_datetime(delivered.loc[post])+pd.to_timedelta(24,unit='h')
shipments=pd.DataFrame({'shipment_id':[f'SHP{i:09d}' for i in range(1,S+1)],'order_id':order_ids[comp],'warehouse_id':wh,'carrier':carrier,'shipped_timestamp':shipped,'promised_delivery_timestamp':promised,'delivered_timestamp':delivered.values,'delay_hours':np.round(dh,1),'delivery_status':np.where(dh>6,'delayed','on_time')})
shipments.to_csv(base/'data/shipments.csv',index=False)

# inventory snapshots
inv=[]
for sd in pd.date_range(start,end,freq='14D'):
    for w in warehouses.warehouse_id:
        psel=active.sample(180,replace=False,random_state=int(sd.dayofyear)+len(inv)%17)
        stock=np.maximum(0,np.random.normal(60,35,len(psel)).astype(int))
        peak=(sd.month==11 and 20<=sd.day<=30)
        if peak:
            mm=np.random.random(len(psel))<.15; stock[mm]=np.maximum(0,np.random.normal(6,7,mm.sum()).astype(int))
        for pid_,q in zip(psel.product_id,stock): inv.append([sd.date(),w,pid_,int(q),20,bool(q<=20),int(max(0,40-q))])
inventory=pd.DataFrame(inv,columns=['snapshot_date','warehouse_id','product_id','on_hand_quantity','reorder_point','below_reorder_point','recommended_reorder_quantity'])
inventory.to_csv(base/'data/inventory_snapshots.csv',index=False)

# pipeline runs
pipes=['orders_ingestion','payments_ingestion','shipments_ingestion','inventory_ingestion','dbt_daily_transform','daily_metrics_publish']; hours_map={'orders_ingestion':2,'payments_ingestion':2,'shipments_ingestion':3,'inventory_ingestion':4,'dbt_daily_transform':5,'daily_metrics_publish':6}
pr=[]; rid=1
for d in dates:
    for p in pipes:
        sched=d+pd.Timedelta(hours=hours_map[p]); actual=sched+pd.Timedelta(minutes=int(np.random.randint(0,8))); dur=max(3,int(np.random.normal(18,7))); st='success'; err=''
        if d==pd.Timestamp('2026-06-18') and p=='orders_ingestion': st='failed'; err='Upstream source timeout for SE partition; retry exhausted after 3 attempts.'
        elif d==pd.Timestamp('2026-03-07') and p=='payments_ingestion': st='partial_success'; err='Payment provider API returned intermittent HTTP 429 responses.'
        elif random.random()<.004: st='failed'; err=random.choice(['BigQuery quota exceeded','Upstream API timeout','Schema mismatch detected','Authentication token expired'])
        pr.append([f'RUN{rid:09d}',p,d.date(),sched,actual,actual+pd.Timedelta(minutes=dur),dur,st,err]); rid+=1
pipeline_runs=pd.DataFrame(pr,columns=['pipeline_run_id','pipeline_name','business_date','scheduled_start_timestamp','actual_start_timestamp','completed_timestamp','duration_minutes','status','error_message'])
pipeline_runs.to_csv(base/'data/pipeline_runs.csv',index=False)

# incidents
incidents=pd.DataFrame([
 ['INC-2026-001','2026-01-12 09:10:00','2026-01-15 18:20:00','medium','delivery','PostNord delivery delays','PostNord deliveries in Nordic markets were delayed due to regional capacity constraints.','PostNord','resolved'],
 ['INC-2026-002','2026-03-07 08:30:00','2026-03-07 13:10:00','high','payments','Payment ingestion partially degraded','Payment provider rate limiting caused a subset of payment records to remain pending.','payments_ingestion','resolved'],
 ['INC-2026-003','2026-06-18 02:12:00','2026-06-18 11:05:00','critical','data_platform','Sweden orders ingestion failed','Sweden order partition was delayed after an upstream source timeout. Revenue dashboards showed an apparent decline until backfill completed.','orders_ingestion','resolved']
],columns=['incident_id','started_at','resolved_at','severity','domain','title','description','affected_component','status'])
incidents.to_csv(base/'data/incidents.csv',index=False)

# RAG docs
(base/'docs/business_metrics.md').write_text('''# Business Metrics

## Realized Net Revenue
Realized net revenue is net revenue from completed orders only. Cancelled orders are excluded.

## Average Order Value
Average Order Value = realized net revenue / completed orders.

## Delivery Delay
A shipment is delayed when it arrives more than 6 hours after its promised delivery timestamp.

## Data Freshness
Daily orders data should be available downstream by 03:00 UTC. A delay above 60 minutes is a freshness incident.
''')

(base/'docs/incident_runbook.md').write_text('''# Incident Runbook

## Revenue Drop Investigation
1. Compare actual revenue with forecast and comparable historical periods.
2. Break variance down by country, channel and category.
3. Validate data freshness before concluding the business actually declined.
4. Check pipeline runs and source availability timestamps.
5. If a partition is late, classify the event as a data-quality incident.
6. Backfill the partition and rerun downstream transformations.

## Payment Investigation
Check payment status distribution, ingestion health, provider rate limits and pending-record reconciliation.

## Delivery Delay Investigation
Compare delay rate by carrier and market, then separate warehouse dispatch delay from carrier transit delay.
''')

(base/'docs/security_policy.md').write_text('''# AI and Data Access Policy

- Agents use least-privilege service accounts.
- Analytical tools are read-only unless a human explicitly approves a write action.
- Generated SQL is restricted to approved datasets.
- Destructive SQL is prohibited for autonomous agents.
- PII must not be surfaced without authorization.
- All tool calls must be logged.
''')

(base/'docs/architecture_overview.md').write_text('''# Architecture Overview

Operational commerce systems produce order, payment, shipment and inventory data. Google Cloud ingestion pipelines load the data into BigQuery. Transformation models create trusted analytics marts. Pipeline-run metadata is retained for operational troubleshooting. The AI operations assistant will later combine structured BigQuery data with documentation and incident history.
''')

dictionary={
 'customers.csv':{'grain':'one row per customer','pk':'customer_id'},
 'products.csv':{'grain':'one row per product','pk':'product_id'},
 'orders.csv':{'grain':'one row per order','pk':'order_id','fk':['customer_id'],'use_cases':['revenue','forecasting','anomaly detection','freshness incidents']},
 'order_items.csv':{'grain':'one row per order-product line','pk':'order_item_id','fk':['order_id','product_id']},
 'payments.csv':{'grain':'one row per payment','pk':'payment_id','fk':['order_id']},
 'shipments.csv':{'grain':'one row per shipment','pk':'shipment_id','fk':['order_id','warehouse_id'],'use_cases':['delay prediction','carrier analysis']},
 'inventory_snapshots.csv':{'grain':'one row per product/warehouse/snapshot','pk':['snapshot_date','warehouse_id','product_id']},
 'pipeline_runs.csv':{'grain':'one row per pipeline/day','pk':'pipeline_run_id','use_cases':['root cause analysis','agent investigation']},
 'incidents.csv':{'grain':'one row per incident','pk':'incident_id','use_cases':['RAG','incident matching']}}
(base/'docs/data_dictionary.json').write_text(json.dumps(dictionary,indent=2))

summary={'customers':len(customers),'products':len(products),'orders':len(orders),'order_items':len(items),'payments':len(payments),'shipments':len(shipments),'inventory_snapshots':len(inventory),'pipeline_runs':len(pipeline_runs),'incidents':len(incidents)}
(base/'README.md').write_text('# Enterprise AI Retail & Logistics Dataset\n\nSynthetic multi-country retail/logistics dataset for an end-to-end Google Cloud AI project.\n\nDate range: 2025-01-01 to 2026-07-31\n\n## Row counts\n'+json.dumps(summary,indent=2)+'\n\n## Embedded scenarios\n- 2026-01-12 to 2026-01-15: PostNord delivery degradation.\n- 2026-03-07: payment-provider rate limiting.\n- 2026-06-18: Sweden orders ingestion delay that creates an apparent revenue drop.\n- Seasonal demand, payday effects and Black Friday peaks.\n- Inventory pressure around peak demand.\n\n## Intended later use\nForecasting, anomaly detection, delay prediction, RAG, agent tools, MCP, root-cause analysis, evaluation and observability.\n')

(base/'generator/generation_config.json').write_text(json.dumps({'seed':42,'date_range':['2025-01-01','2026-07-31'],'customers':n_customers,'products':800},indent=2))

# Copy generator and create ZIP in the project directory
shutil.copy(__file__,base/'generator/generate_enterprise_ai_dataset.py')
shutil.make_archive(str(project_dir/'enterprise_ai_retail_dataset'),'zip',base)

print(json.dumps(summary,indent=2))
print(f'\nDataset: {base}')
print(f'ZIP: {project_dir/"enterprise_ai_retail_dataset.zip"}')