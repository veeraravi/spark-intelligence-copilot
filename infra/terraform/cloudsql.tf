# Cloud SQL configuration

variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "instance_name" {
  type = string
}

variable "database_version" {
  type = string
}

variable "tier" {
  type = string
}

resource "google_sql_database_instance" "main" {
  name             = var.instance_name
  database_version = var.database_version
  region           = var.region
  project          = var.project_id
  
  settings {
    tier              = var.tier
    availability_type = "REGIONAL"
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      binary_log_enabled             = true
    }
    
    ip_configuration {
      require_ssl = true
    }
  }
  
  deletion_protection = true
}

resource "google_sql_database" "spark_db" {
  name     = "spark_copilot"
  instance = google_sql_database_instance.main.name
  project  = var.project_id
}

resource "google_sql_user" "app_user" {
  name     = "spark_app"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
  project  = var.project_id
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

output "connection_name" {
  value = google_sql_database_instance.main.connection_name
}

output "database_name" {
  value = google_sql_database.spark_db.name
}

output "database_user" {
  value = google_sql_user.app_user.name
}
