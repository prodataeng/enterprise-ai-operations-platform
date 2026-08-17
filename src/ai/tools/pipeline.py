from google.cloud import bigquery

PROJECT_ID = "diesel-command-483009-r5"
TABLE = f"{PROJECT_ID}.retail_ai_dev_marts.fct_pipeline_runs"

client = bigquery.Client(project=PROJECT_ID)


def get_pipeline_health(
    start_date: str,
    end_date: str,
    pipeline_name: str | None = None,
    limit: int = 50,
) -> dict:
    """Get pipeline failures, delays and partial-success runs for a period."""

    filters = [
        "date_key BETWEEN @start_date AND @end_date"
    ]

    if pipeline_name:
        filters.append("LOWER(pipeline_name) = LOWER(@pipeline_name)")

    query = f"""
        SELECT
            pipeline_run_id,
            date_key,
            pipeline_name,
            status,
            duration_minutes,
            start_delay_minutes,
            error_message,
            is_successful_run,
            is_failed_run,
            is_partial_success_run
        FROM `{TABLE}`
        WHERE {" AND ".join(filters)}
          AND (
              is_failed_run = TRUE
              OR is_partial_success_run = TRUE
              OR start_delay_minutes > 60
          )
        ORDER BY date_key DESC, start_delay_minutes DESC
        LIMIT @limit
    """

    params = [
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        bigquery.ScalarQueryParameter("limit", "INT64", limit),
    ]

    if pipeline_name:
        params.append(
            bigquery.ScalarQueryParameter(
                "pipeline_name", "STRING", pipeline_name
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
        "issues": [
            {
                "pipeline_run_id": r.pipeline_run_id,
                "date": str(r.date_key),
                "pipeline_name": r.pipeline_name,
                "status": r.status,
                "duration_minutes": r.duration_minutes,
                "start_delay_minutes": r.start_delay_minutes,
                "error_message": r.error_message,
            }
            for r in rows
        ],
    }