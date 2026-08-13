bq --project_id=diesel-command-483009-r5 load \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  diesel-command-483009-r5:retail_ai_raw.customers \
  gs://diesel-command-483009-r5-enterprise-ai-raw/raw/customers.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.products \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/products.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.warehouses \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/warehouses.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.stores \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/stores.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.orders \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/orders.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.order_items \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/order_items.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.payments \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/payments.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.shipments \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/shipments.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.inventory_snapshots \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/inventory_snapshots.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.pipeline_runs \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/pipeline_runs.csv

bq --project_id=diesel-command-483009-r5 load --replace --source_format=CSV --skip_leading_rows=1 \
diesel-command-483009-r5:retail_ai_raw.incidents \
gs://diesel-command-483009-r5-enterprise-ai-raw/raw/incidents.csv
