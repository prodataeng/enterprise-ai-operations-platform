# Enterprise AI Retail & Logistics Dataset

Synthetic multi-country retail/logistics dataset for an end-to-end Google Cloud AI project.

Date range: 2025-01-01 to 2026-07-31

## Row counts
{
  "customers": 15000,
  "products": 800,
  "orders": 91275,
  "order_items": 164335,
  "payments": 91275,
  "shipments": 88725,
  "inventory_snapshots": 22680,
  "pipeline_runs": 3462,
  "incidents": 3
}

## Embedded scenarios
- 2026-01-12 to 2026-01-15: PostNord delivery degradation.
- 2026-03-07: payment-provider rate limiting.
- 2026-06-18: Sweden orders ingestion delay that creates an apparent revenue drop.
- Seasonal demand, payday effects and Black Friday peaks.
- Inventory pressure around peak demand.

## Intended later use
Forecasting, anomaly detection, delay prediction, RAG, agent tools, MCP, root-cause analysis, evaluation and observability.
