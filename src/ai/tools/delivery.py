from google.cloud import bigquery

PROJECT_ID = "diesel-command-483009-r5"
MODEL = f"{PROJECT_ID}.retail_ai_dev_ml.delivery_delay_logistic"
TABLE = f"{PROJECT_ID}.retail_ai_dev_ml.mart_delivery_features"

client = bigquery.Client(project=PROJECT_ID)


def get_high_risk_shipments(
    country_code: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 10,
) -> dict:
    """Get shipments with the highest predicted delivery-delay risk.

    Args:
        country_code: Optional country code such as SE, NO, DK, FI or DE.
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        limit: Maximum number of shipments to return.
    """

    filters = []

    if country_code:
        filters.append("country_code = @country_code")

    if start_date:
        filters.append("date_key >= @start_date")

    if end_date:
        filters.append("date_key <= @end_date")

    where_clause = (
        "WHERE " + " AND ".join(filters)
        if filters
        else ""
    )

    query = f"""
        SELECT
            shipment_id,
            order_id,
            date_key,
            country_code,
            carrier,
            predicted_target_is_delayed,
            (
                SELECT prob
                FROM UNNEST(predicted_target_is_delayed_probs)
                WHERE label = TRUE
                LIMIT 1
            ) AS delay_probability
        FROM ML.PREDICT(
            MODEL `{MODEL}`,
            (
                SELECT *
                FROM `{TABLE}`
                {where_clause}
            )
        )
        ORDER BY delay_probability DESC
        LIMIT @limit
    """

    params = [
        bigquery.ScalarQueryParameter("limit", "INT64", limit)
    ]

    if country_code:
        params.append(
            bigquery.ScalarQueryParameter(
                "country_code",
                "STRING",
                country_code.upper(),
            )
        )

    if start_date:
        params.append(
            bigquery.ScalarQueryParameter(
                "start_date",
                "DATE",
                start_date,
            )
        )

    if end_date:
        params.append(
            bigquery.ScalarQueryParameter(
                "end_date",
                "DATE",
                end_date,
            )
        )

    config = bigquery.QueryJobConfig(query_parameters=params)

    rows = client.query(query, job_config=config).result()

    return {
        "country_code": country_code.upper() if country_code else None,
        "start_date": start_date,
        "end_date": end_date,
        "shipments": [
            {
                "shipment_id": row.shipment_id,
                "order_id": row.order_id,
                "date": str(row.date_key),
                "country_code": row.country_code,
                "carrier": row.carrier,
                "predicted_delayed": bool(row.predicted_target_is_delayed),
                "delay_probability": round(
                    float(row.delay_probability), 4
                ),
            }
            for row in rows
        ],
    }
SHIPMENTS_TABLE = (
    f"{PROJECT_ID}.retail_ai_dev_marts.fct_shipments"
)


def get_delivery_outcomes(
    country_code: str,
    start_date: str,
    end_date: str,
    limit: int = 50,
) -> dict:
    """Get actual delivery outcomes for a country and date range."""

    query = f"""
        SELECT
            shipment_id,
            order_id,
            date_key,
            country_code,
            carrier,
            delivery_status,
            is_delayed,
            delay_hours,
            transit_hours
        FROM `{SHIPMENTS_TABLE}`
        WHERE country_code = @country_code
          AND date_key BETWEEN @start_date AND @end_date
        ORDER BY delay_hours DESC
        LIMIT @limit
    """

    config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "country_code", "STRING", country_code.upper()
            ),
            bigquery.ScalarQueryParameter(
                "start_date", "DATE", start_date
            ),
            bigquery.ScalarQueryParameter(
                "end_date", "DATE", end_date
            ),
            bigquery.ScalarQueryParameter(
                "limit", "INT64", limit
            ),
        ]
    )

    rows = client.query(query, job_config=config).result()

    return {
        "country_code": country_code.upper(),
        "start_date": start_date,
        "end_date": end_date,
        "shipments": [
            {
                "shipment_id": r.shipment_id,
                "order_id": r.order_id,
                "date": str(r.date_key),
                "carrier": r.carrier,
                "delivery_status": r.delivery_status,
                "is_delayed": bool(r.is_delayed),
                "delay_hours": float(r.delay_hours),
                "transit_hours": r.transit_hours,
            }
            for r in rows
        ],
    }
if __name__ == "__main__":
    print(
    get_high_risk_shipments(
        country_code="SE",
        start_date="2026-07-25",
        end_date="2026-07-31",
        limit=10,
    )
)