# Terraform variables

variable "gcp_project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "gcp_region" {
  type        = string
  description = "GCP Region"
  default     = "us-central1"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "production"
}

variable "app_name" {
  type        = string
  description = "Application name"
  default     = "spark-intelligence-copilot"
}

variable "gke_cluster_config" {
  type = object({
    machine_type   = string
    node_count     = number
    min_node_count = number
    max_node_count = number
  })
  description = "GKE cluster configuration"
  
  default = {
    machine_type   = "n2-standard-4"
    node_count     = 3
    min_node_count = 2
    max_node_count = 10
  }
}

variable "enable_monitoring" {
  type        = bool
  description = "Enable Google Cloud Monitoring"
  default     = true
}

variable "enable_logging" {
  type        = bool
  description = "Enable Google Cloud Logging"
  default     = true
}
