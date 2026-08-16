# Delivery Delay Classification

Place this folder under:

`dbt/macros/ml/delivery_delay/`

This package trains a BigQuery ML binary logistic regression model using
`mart_delivery_features`.

## Important

The feature mart must exclude outcome-leakage fields such as:

- `delivered_timestamp`
- `transit_hours`
- `delay_hours`

The target is:

`target_is_delayed`

## 1. Train validation model

Training data defaults to dates through 2026-05-31.

```bash
dbt run-operation train_delivery_delay_validation
```

## 2. Evaluate on future holdout data

Defaults to 2026-06-01 through 2026-07-31.

```bash
dbt run-operation evaluate_delivery_delay_validation
```

Optional custom classification threshold:

```bash
dbt run-operation evaluate_delivery_delay_validation   --args '{threshold: 0.4}'
```

## 3. Inspect validation predictions

```bash
dbt run-operation predict_delivery_delay_validation
```

Example:

```bash
dbt run-operation predict_delivery_delay_validation   --args '{threshold: 0.5, limit_rows: 25}'
```

## 4. Train production model

Uses all rows currently available in `mart_delivery_features`.

```bash
dbt run-operation train_delivery_delay_production
```

## 5. Generate production predictions

```bash
dbt run-operation predict_delivery_delay_production
```

## Models

Validation:

`<target.schema>_ml.delivery_delay_logistic_validation`

Production:

`<target.schema>_ml.delivery_delay_logistic`

## Metrics

The validation macro returns:

- precision
- recall
- accuracy
- f1_score
- log_loss
- roc_auc

## Dependency

These macros use the existing `log_query_results` helper from the ML macros.
