from google.cloud import bigquery

PROJECT_ID = "diesel-command-483009-r5"
MODEL = f"{PROJECT_ID}.retail_ai_dev_ml.revenue_forecast_arima"

client = bigquery.Client(project=PROJECT_ID)


def get_revenue_anomalies(country_code: str, limit: int = 10) -> dict:
    """Get historical revenue anomalies for a country."""

    query = f"""
        SELECT
            date_key,
            country_code,
            net_revenue_sek,
            is_anomaly,
            lower_bound,
            upper_bound,
            anomaly_probability
        FROM ML.DETECT_ANOMALIES(
            MODEL `{MODEL}`,
            STRUCT(0.99 AS anomaly_prob_threshold)
        )
        WHERE country_code = @country_code
          AND is_anomaly = TRUE
        ORDER BY anomaly_probability DESC
        LIMIT @limit
    """

    config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "country_code",
                "STRING",
                country_code.upper(),
            ),
            bigquery.ScalarQueryParameter(
                "limit",
                "INT64",
                limit,
            ),
        ]
    )

    rows = client.query(query, job_config=config).result()

    return {
        "country_code": country_code.upper(),
        "anomalies": [
            {
                "date": str(row.date_key),
                "actual_revenue_sek": float(row.net_revenue_sek),
                "expected_lower_bound": float(row.lower_bound),
                "expected_upper_bound": float(row.upper_bound),
                "anomaly_probability": float(row.anomaly_probability),
                "direction": (
                    "LOW"
                    if row.net_revenue_sek < row.lower_bound
                    else "HIGH"
                ),
            }
            for row in rows
        ],
    }