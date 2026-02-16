# Vertex AI configuration

variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "model_registry" {
  type = map(string)
}

resource "google_vertex_ai_featurestore" "featurestore" {
  name          = "spark-intelligence-fs"
  location      = var.region
  project       = var.project_id
  force_destroy = false
  
  online_serving_config {
    fixed_node_count = 2
  }
}

output "featurestore_id" {
  value = google_vertex_ai_featurestore.featurestore.id
}
