import re
from decimal import Decimal
from datetime import date, datetime

from google.cloud import bigquery


PROJECT_ID = "diesel-command-483009-r5"
LOCATION = "europe-north2"

ALLOWED_DATASETS = {
    "retail_ai_dev_marts",
    "retail_ai_dev_ml",
}

MAX_BYTES = 1_000_000_000  # 1 GB

client = bigquery.Client(project=PROJECT_ID)


def to_json_safe(value):
    """Convert BigQuery/Python values into JSON-serializable values."""

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, list):
        return [to_json_safe(v) for v in value]

    if isinstance(value, dict):
        return {
            k: to_json_safe(v)
            for k, v in value.items()
        }

    return value


def query_bigquery(sql: str) -> dict:
    """Run a read-only GoogleSQL query against approved BigQuery datasets.

    Args:
        sql: GoogleSQL SELECT query generated to answer an analytical question.
    """

    sql = sql.strip().rstrip(";")
    upper = sql.upper()

    # Only SELECT / CTE queries
    if not (
        upper.startswith("SELECT")
        or upper.startswith("WITH")
    ):
        return {
            "error": "Only SELECT queries are allowed."
        }

    # Block destructive / write operations
    blocked = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "MERGE",
        "DROP",
        "CREATE",
        "ALTER",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
        "CALL",
        "EXPORT",
    ]

    if any(
        re.search(rf"\b{word}\b", upper)
        for word in blocked
    ):
        return {
            "error": "Query contains a blocked SQL operation."
        }

    # Validate referenced datasets
    datasets = re.findall(
        rf"`{re.escape(PROJECT_ID)}\.([A-Za-z0-9_]+)\.",
        sql,
    )

    if any(
        dataset not in ALLOWED_DATASETS
        for dataset in datasets
    ):
        return {
            "error": "Query references an unapproved dataset."
        }

    # Prevent large result sets
    if "LIMIT" not in upper:
        sql += "\nLIMIT 100"

    # Dry run first
    dry_config = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False,
        use_legacy_sql=False,
    )

    dry_job = client.query(
        sql,
        job_config=dry_config,
        location=LOCATION,
    )

    estimated_bytes = (
        dry_job.total_bytes_processed or 0
    )

    if estimated_bytes > MAX_BYTES:
        return {
            "error": "Query exceeds the allowed scan size.",
            "estimated_bytes": estimated_bytes,
        }

    # Execute query
    config = bigquery.QueryJobConfig(
        maximum_bytes_billed=MAX_BYTES,
        use_legacy_sql=False,
    )

    rows = client.query(
        sql,
        job_config=config,
        location=LOCATION,
    ).result()

    result = [
        {
            key: to_json_safe(value)
            for key, value in row.items()
        }
        for row in rows
    ]

    return {
        "sql": sql,
        "estimated_bytes": estimated_bytes,
        "row_count": len(result),
        "rows": result,
    }