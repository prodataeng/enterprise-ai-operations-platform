variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Primary Google Cloud region"
  type        = string
  default     = "europe-north2"
}

variable "bq_location" {
  description = "BigQuery dataset location"
  type        = string
  default     = "EU"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "raw_dataset_id" {
  description = "BigQuery raw dataset ID"
  type        = string
  default     = "retail_ai_raw"
}

variable "bucket_name" {
  description = "Globally unique GCS bucket name"

  type    = string
  default = null
}

variable "force_destroy_bucket" {
  description = "Allow Terraform to destroy a non-empty development bucket"
  type        = bool
  default     = false
}