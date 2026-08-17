from google.cloud import bigquery

PROJECT_ID = "diesel-command-483009-r5"
TABLE = f"{PROJECT_ID}.retail_ai_dev_marts.fct_incidents"

client = bigquery.Client(project=PROJECT_ID)


def get_incidents(
    start_date: str,
    end_date: str,
    domain: str | None = None,
    limit: int = 20,
) -> dict:
    """Get known incidents for a date range."""

    filters = [
        "date_key BETWEEN @start_date AND @end_date"
    ]

    if domain:
        filters.append("LOWER(domain) = LOWER(@domain)")

    query = f"""
        SELECT
            incident_id,
            date_key,
            started_at,
            resolved_at,
            severity,
            domain,
            title,
            description,
            affected_component,
            status,
            resolution_minutes
        FROM `{TABLE}`
        WHERE {" AND ".join(filters)}
        ORDER BY started_at DESC
        LIMIT @limit
    """

    params = [
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        bigquery.ScalarQueryParameter("limit", "INT64", limit),
    ]

    if domain:
        params.append(
            bigquery.ScalarQueryParameter(
                "domain", "STRING", domain
            )
        )

    rows = client.query(
        query,
        job_config=bigquery.QueryJobConfig(
            query_parameters=params
        ),
    ).result()

    return {
        "start_date": start_date,
        "end_date": end_date,
        "incidents": [
            {
                "incident_id": r.incident_id,
                "date": str(r.date_key),
                "severity": r.severity,
                "domain": r.domain,
                "title": r.title,
                "description": r.description,
                "affected_component": r.affected_component,
                "status": r.status,
                "resolution_minutes": r.resolution_minutes,
            }
            for r in rows
        ],
    }