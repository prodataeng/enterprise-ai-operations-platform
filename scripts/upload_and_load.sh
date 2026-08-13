#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="${1:-}"
DATASET_ID="${2:-retail_ai_raw}"
BUCKET_NAME="${3:-${PROJECT_ID}-enterprise-ai-raw}"
if [[ -z "${PROJECT_ID}" ]]; then echo "Usage: $0 <project_id> [dataset_id] [bucket_name]"; exit 1; fi
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="${REPO_ROOT}/dataset/data"
DOCS_DIR="${REPO_ROOT}/dataset/docs"
SCHEMA_DIR="${REPO_ROOT}/terraform/schemas"
if [[ ! -d "${DATA_DIR}" ]]; then echo "Data directory not found: ${DATA_DIR}"; echo "Run the generator first."; exit 1; fi
gcloud config set project "${PROJECT_ID}"
gcloud storage cp "${DATA_DIR}"/*.csv "gs://${BUCKET_NAME}/raw/"
if [[ -d "${DOCS_DIR}" ]]; then gcloud storage cp "${DOCS_DIR}" "gs://${BUCKET_NAME}/docs/" --recursive; fi
load_table(){ local table="$1" file="$2" schema="$3"; echo "Loading ${table}..."; bq --project_id="${PROJECT_ID}" load --replace --source_format=CSV --skip_leading_rows=1 --allow_quoted_newlines "${PROJECT_ID}:${DATASET_ID}.${table}" "gs://${BUCKET_NAME}/raw/${file}" "${SCHEMA_DIR}/${schema}"; }
load_table customers customers.csv customers.json
load_table products products.csv products.json
load_table warehouses warehouses.csv warehouses.json
load_table stores stores.csv stores.json
load_table orders orders.csv orders.json
load_table order_items order_items.csv order_items.json
load_table payments payments.csv payments.json
load_table shipments shipments.csv shipments.json
load_table inventory_snapshots inventory_snapshots.csv inventory_snapshots.json
load_table pipeline_runs pipeline_runs.csv pipeline_runs.json
load_table incidents incidents.csv incidents.json
bq --project_id="${PROJECT_ID}" ls "${PROJECT_ID}:${DATASET_ID}"
