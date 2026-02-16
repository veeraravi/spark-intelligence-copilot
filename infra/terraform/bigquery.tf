# BigQuery configuration

variable "project_id" {
  type = string
}

variable "datasets" {
  type = map(object({
    description = string
    location    = string
  }))
  default = {}
}

resource "google_bigquery_dataset" "datasets" {
  for_each = var.datasets
  
  dataset_id    = each.key
  friendly_name = each.key
  description   = each.value.description
  location      = each.value.location
  project       = var.project_id
  
  access {
    role          = "OWNER"
    user_by_email = google_service_account.spark_sa.email
  }
}

resource "google_service_account" "spark_sa" {
  account_id   = "spark-intelligence-sa"
  display_name = "Spark Intelligence Service Account"
  project      = var.project_id
}

resource "google_project_iam_member" "spark_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.spark_sa.email}"
}

output "service_account_email" {
  value = google_service_account.spark_sa.email
}
