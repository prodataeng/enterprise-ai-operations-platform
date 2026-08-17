from src.ai.tools.schema import get_bigquery_schema

schema = get_bigquery_schema()

for table, columns in schema.items():
    if any(x in table for x in [
        "pipeline",
        "incident",
        "shipment",
    ]):
        print(f"\n=== {table} ===")
        for column in columns:
            print(column)