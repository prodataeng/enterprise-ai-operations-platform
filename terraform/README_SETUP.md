# Phase 1 - GCP Raw Landing Layer

## 1. Authenticate
```bash
gcloud auth login
gcloud auth application-default login
```

## 2. Configure Terraform
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```
Edit `terraform.tfvars` and set `project_id`.

## 3. Provision
```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan
terraform apply
```

## 4. Generate the source data
Run your existing generator so `enterprise_ai_retail_dataset/data/` and `docs/` exist.

## 5. Upload + load
From repo root:
```bash
./scripts/upload_and_load.sh YOUR_GCP_PROJECT_ID
```
If you override the bucket name:
```bash
./scripts/upload_and_load.sh YOUR_GCP_PROJECT_ID retail_ai_raw YOUR_BUCKET_NAME
```

## 6. Validate
Replace `YOUR_GCP_PROJECT_ID` in `scripts/validate_raw.sql` and run it in BigQuery.
