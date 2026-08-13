output "data_lake_bucket" {
  description = "GCS landing/data lake bucket name"
  value       = google_storage_bucket.data_lake.name
}

output "raw_dataset" {
  description = "BigQuery raw dataset ID"
  value       = google_bigquery_dataset.raw.dataset_id
}

output "raw_dataset_fqn" {
  description = "Fully qualified BigQuery dataset"
  value       = "${var.project_id}.${google_bigquery_dataset.raw.dataset_id}"
}