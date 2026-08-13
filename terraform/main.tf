provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  bucket_name = var.bucket_name != null ? var.bucket_name : "${var.project_id}-enterprise-ai-raw"

  labels = {
    project     = "enterprise-ai-operations-platform"
    environment = var.environment
    managed_by  = "terraform"
  }

  required_services = toset([
    "storage.googleapis.com",
    "bigquery.googleapis.com"
  ])
}

# --------------------------------------------------
# Enable required APIs
# --------------------------------------------------

resource "google_project_service" "required" {
  for_each = local.required_services

  project = var.project_id
  service = each.value

  disable_on_destroy = false
}

# --------------------------------------------------
# Cloud Storage
# --------------------------------------------------

resource "google_storage_bucket" "data_lake" {
  name     = local.bucket_name
  project  = var.project_id
  location = var.region

  uniform_bucket_level_access = true
  force_destroy               = var.force_destroy_bucket

  labels = local.labels

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age            = 30
      matches_prefix = ["raw/"]
    }

    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  depends_on = [
    google_project_service.required
  ]
}

# --------------------------------------------------
# BigQuery RAW dataset
# --------------------------------------------------

resource "google_bigquery_dataset" "raw" {
  project    = var.project_id
  dataset_id = var.raw_dataset_id
  location   = var.bq_location

  description = "Raw source-system data for the Enterprise AI Operations Platform."

  delete_contents_on_destroy = false

  labels = local.labels

  depends_on = [
    google_project_service.required
  ]
}

# --------------------------------------------------
# Customers
# --------------------------------------------------

resource "google_bigquery_table" "customers" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "customers"

  deletion_protection = false

  schema = file("${path.module}/schemas/customers.json")

  clustering = [
    "country_code",
    "customer_segment"
  ]
}

# --------------------------------------------------
# Products
# --------------------------------------------------

resource "google_bigquery_table" "products" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "products"

  deletion_protection = false

  schema = file("${path.module}/schemas/products.json")

  clustering = [
    "category",
    "subcategory",
    "status"
  ]
}

# --------------------------------------------------
# Warehouses
# --------------------------------------------------

resource "google_bigquery_table" "warehouses" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "warehouses"

  deletion_protection = false

  schema = file("${path.module}/schemas/warehouses.json")
}

# --------------------------------------------------
# Stores
# --------------------------------------------------

resource "google_bigquery_table" "stores" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "stores"

  deletion_protection = false

  schema = file("${path.module}/schemas/stores.json")

  clustering = [
    "country_code"
  ]
}

# --------------------------------------------------
# Orders
# --------------------------------------------------

resource "google_bigquery_table" "orders" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "orders"

  deletion_protection = false

  schema = file("${path.module}/schemas/orders.json")

  time_partitioning {
    type  = "DAY"
    field = "order_timestamp"
  }

  clustering = [
    "country_code",
    "sales_channel",
    "order_status"
  ]
}

# --------------------------------------------------
# Order Items
# --------------------------------------------------

resource "google_bigquery_table" "order_items" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "order_items"

  deletion_protection = false

  schema = file("${path.module}/schemas/order_items.json")

  clustering = [
    "order_id",
    "product_id"
  ]
}

# --------------------------------------------------
# Payments
# --------------------------------------------------

resource "google_bigquery_table" "payments" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "payments"

  deletion_protection = false

  schema = file("${path.module}/schemas/payments.json")

  time_partitioning {
    type  = "DAY"
    field = "payment_timestamp"
  }

  clustering = [
    "payment_method",
    "payment_status"
  ]
}

# --------------------------------------------------
# Shipments
# --------------------------------------------------

resource "google_bigquery_table" "shipments" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "shipments"

  deletion_protection = false

  schema = file("${path.module}/schemas/shipments.json")

  time_partitioning {
    type  = "DAY"
    field = "shipped_timestamp"
  }

  clustering = [
    "carrier",
    "warehouse_id",
    "delivery_status"
  ]
}

# --------------------------------------------------
# Inventory snapshots
# --------------------------------------------------

resource "google_bigquery_table" "inventory_snapshots" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "inventory_snapshots"

  deletion_protection = false

  schema = file("${path.module}/schemas/inventory_snapshots.json")

  time_partitioning {
    type  = "DAY"
    field = "snapshot_date"
  }

  clustering = [
    "warehouse_id",
    "product_id"
  ]
}

# --------------------------------------------------
# Pipeline runs
# --------------------------------------------------

resource "google_bigquery_table" "pipeline_runs" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "pipeline_runs"

  deletion_protection = false

  schema = file("${path.module}/schemas/pipeline_runs.json")

  time_partitioning {
    type  = "DAY"
    field = "business_date"
  }

  clustering = [
    "pipeline_name",
    "status"
  ]
}

# --------------------------------------------------
# Incidents
# --------------------------------------------------

resource "google_bigquery_table" "incidents" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "incidents"

  deletion_protection = false

  schema = file("${path.module}/schemas/incidents.json")

  time_partitioning {
    type  = "DAY"
    field = "started_at"
  }

  clustering = [
    "severity",
    "domain",
    "status"
  ]
}