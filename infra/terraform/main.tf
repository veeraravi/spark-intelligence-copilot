# Terraform main configuration

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  
  backend "gcs" {
    bucket = "spark-intelligence-terraform"
    prefix = "prod"
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Local variables
locals {
  environment = "production"
  app_name    = "spark-intelligence-copilot"
}

# Create GKE cluster
module "gke" {
  source = "./gke"
  
  project_id       = var.gcp_project_id
  region           = var.gcp_region
  cluster_name     = "${local.app_name}-cluster"
  machine_type     = "n2-standard-4"
  node_count       = 3
  min_node_count   = 2
  max_node_count   = 10
}

# Create Cloud SQL instance
module "cloudsql" {
  source = "./cloudsql"
  
  project_id       = var.gcp_project_id
  region           = var.gcp_region
  instance_name    = "${local.app_name}-db"
  database_version = "POSTGRES_15"
  tier             = "db-custom-2-8192"
}

# Create BigQuery datasets
module "bigquery" {
  source = "./bigquery"
  
  project_id = var.gcp_project_id
  
  datasets = {
    "spark_events" : {
      description = "Spark event logs"
      location    = var.gcp_region
    },
    "spark_metrics" : {
      description = "Spark job metrics"
      location    = var.gcp_region
    }
  }
}

# Vertex AI resources
module "vertexai" {
  source = "./vertexai"
  
  project_id = var.gcp_project_id
  region     = var.gcp_region
  
  model_registry = {
    runtime_predictor = "runtime_predictor_v1"
    skew_detector     = "skew_detector_v1"
  }
}

output "gke_cluster_name" {
  value       = module.gke.cluster_name
  description = "GKE cluster name"
}

output "cloudsql_connection_name" {
  value       = module.cloudsql.connection_name
  description = "Cloud SQL connection name"
}

output "bigquery_project" {
  value       = var.gcp_project_id
  description = "BigQuery project ID"
}
