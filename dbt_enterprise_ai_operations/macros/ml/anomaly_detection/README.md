# Revenue anomaly detection

Place this folder under:

`dbt/macros/ml/anomaly_detection/`

It reuses the production BigQuery ML model:

`revenue_forecast_arima`

## Historical anomalies

```bash
dbt run-operation detect_historical_revenue_anomalies
```

Optional threshold:

```bash
dbt run-operation detect_historical_revenue_anomalies \
  --args '{anomaly_prob_threshold: 0.90}'
```

## Detect anomalies using the current revenue mart

```bash
dbt run-operation detect_revenue_anomalies
```

Optional threshold:

```bash
dbt run-operation detect_revenue_anomalies \
  --args '{anomaly_prob_threshold: 0.90}'
```

Default threshold is `0.95`.

This folder depends on the helper macros already created under revenue forecasting:

- `revenue_ml_model_name`
- `log_query_results`
