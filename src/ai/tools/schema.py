from google.cloud import bigquery

PROJECT_ID = "diesel-command-483009-r5"
LOCATION = "europe-north2"

DATASETS = [
    "retail_ai_dev_marts",
    "retail_ai_dev_ml",
]

client = bigquery.Client(project=PROJECT_ID)


def get_bigquery_schema() -> dict:
    """Get available BigQuery tables and columns for approved datasets."""

    result = {}

    for dataset in DATASETS:
        sql = f"""
        SELECT
            table_name,
            column_name,
            data_type,
            ordinal_position
        FROM `{PROJECT_ID}.{dataset}.INFORMATION_SCHEMA.COLUMNS`
        ORDER BY table_name, ordinal_position
        """

        rows = client.query(
            sql,
            location=LOCATION,
        ).result()

        for row in rows:
            table = f"{PROJECT_ID}.{dataset}.{row.table_name}"

            result.setdefault(table, []).append({
                "column": row.column_name,
                "type": row.data_type,
            })

    return result