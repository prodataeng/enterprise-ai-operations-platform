# Revenue forecasting dbt macros

Place `revenue_forecasting/` under `dbt/macros/ml/`.

Commands:

```bash
dbt run-operation train_revenue_forecast_validation
dbt run-operation evaluate_revenue_forecast_validation
dbt run-operation forecast_revenue_validation
dbt run-operation inspect_revenue_forecast_validation
dbt run-operation train_revenue_forecast_production
dbt run-operation forecast_revenue_production
```

Optional examples:

```bash
dbt run-operation inspect_revenue_forecast_validation --args '{show_all_candidate_models: true}'
dbt run-operation forecast_revenue_production --args '{horizon: 14, confidence_level: 0.95}'
```

The macros derive the ML dataset from the active dbt target:
`retail_ai_dev` -> `retail_ai_dev_ml`
`retail_ai` -> `retail_ai_ml`

Note: BigQuery ML supports `EMEA` as the continental holiday region; `EU` is not a supported holiday-region value.
