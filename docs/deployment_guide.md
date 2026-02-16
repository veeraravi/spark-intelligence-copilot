# Spark Intelligence Copilot - Deployment Guide

## Prerequisites

- Google Cloud Account with billing enabled
- `gcloud` CLI installed and configured
- `kubectl` installed
- Terraform >= 1.0
- Docker installed (for local testing)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/spark-intelligence/copilot.git
cd spark-intelligence-copilot
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your local settings
```

### 3. Start Local Services
```bash
docker-compose up -d
```

This starts:
- FastAPI application on localhost:8000
- PostgreSQL database on localhost:5432
- Redis cache on localhost:6379
- Kafka broker on localhost:9092
- Zookeeper on localhost:2181

### 4. Initialize Database
```bash
docker-compose exec api python -m scripts.init_db
```

### 5. Load Sample Data
```bash
docker-compose exec api python -m scripts.load_samples
```

### 6. Verify Installation
```bash
curl http://localhost:8000/health
```

## Cloud Deployment (GCP)

### 1. Set Environment Variables
```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
export ENVIRONMENT="production"
```

### 2. Create GCP Project
```bash
gcloud projects create spark-intelligence-prod \
  --set-as-default
```

### 3. Enable Required APIs
```bash
gcloud services enable \
  container.googleapis.com \
  sqladmin.googleapis.com \
  bigquery.googleapis.com \
  cloudkms.googleapis.com \
  storage-api.googleapis.com \
  artifactregistry.googleapis.com
```

### 4. Deploy Infrastructure with Terraform
```bash
cd infra/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="gcp_project_id=$GCP_PROJECT_ID"

# Apply configuration
terraform apply -var="gcp_project_id=$GCP_PROJECT_ID"
```

### 5. Configure kubectl
```bash
gcloud container clusters get-credentials spark-intelligence-cluster \
  --region=$GCP_REGION
```

### 6. Build and Push Docker Image
```bash
# Configure Docker authentication
gcloud auth configure-docker gcr.io

# Build image
docker build -f infra/docker/Dockerfile -t gcr.io/$GCP_PROJECT_ID/spark-intelligence-copilot:latest .

# Push to registry
docker push gcr.io/$GCP_PROJECT_ID/spark-intelligence-copilot:latest
```

### 7. Deploy to Kubernetes
```bash
cd infra/k8s

# Update deployment image reference
sed -i "s/PROJECT_ID/$GCP_PROJECT_ID/g" deployment.yaml

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

### 8. Verify Deployment
```bash
# Check deployment status
kubectl get deployments

# Check pods
kubectl get pods

# Check service
kubectl get service spark-intelligence-api

# Get external IP
kubectl get ingress spark-intelligence-ingress
```

### 9. Access Application
```bash
# Get the external IP
EXTERNAL_IP=$(kubectl get service spark-intelligence-api \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

curl http://$EXTERNAL_IP/health
```

## Configuration Management

### Environment Variables
See `.env.example` for all available options.

### Secrets Management
```bash
# Create secrets
kubectl create secret generic spark-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=api-key=$API_KEY

# Update existing secret
kubectl patch secret spark-secrets -p \
  '{"data":{"database-url":"'$(echo -n $DATABASE_URL|base64)+'"}}'
```

### ConfigMaps
```bash
# Create configmap
kubectl create configmap spark-config \
  --from-literal=gcp-project-id=$GCP_PROJECT_ID \
  --from-literal=gcp-region=$GCP_REGION

# View configmap
kubectl get configmap spark-config -o yaml
```

## Database Setup

### PostgreSQL Connection
```bash
# Get Cloud SQL connection string
gcloud sql instances describe spark-intelligence-db \
  --format='value(connectionName)'

# Connect using Cloud SQL Proxy
cloud_sql_proxy -instances=$INSTANCE_CONNECTION_NAME=tcp:5432

# Connect with psql
psql -h localhost -U spark_app -d spark_copilot
```

### Initialize Schema
```bash
# Run migrations
python -m scripts.migrate_db

# Seed initial data
python -m scripts.seed_data
```

## Backup and Recovery

### Database Backups
```bash
# Create manual backup
gcloud sql backups create --instance=spark-intelligence-db

# List backups
gcloud sql backups list --instance=spark-intelligence-db

# Restore from backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=spark-intelligence-db \
  --backup-configuration=default
```

### GCS Backups
```bash
# Enable automatic backups to GCS
gsutil rsync -r gs://spark-intelligence-bucket /backup/location
```

## Monitoring and Logs

### View Logs
```bash
# API logs
kubectl logs -f deployment/spark-intelligence-api

# All pod logs
kubectl logs -f --all-containers=true -l app=spark-intelligence-api
```

### Access GCP Monitoring
```bash
# Open Cloud Console
gcloud console projects describe $GCP_PROJECT_ID

# View metrics
gcloud monitoring metrics-descriptors list
```

## Scaling

### Auto-scaling Configuration
```bash
# Set HPA (Horizontal Pod Autoscaler)
kubectl autoscale deployment spark-intelligence-api \
  --min=2 --max=10 \
  --cpu-percent=80
```

### Manual Scaling
```bash
# Scale replicas
kubectl scale deployment spark-intelligence-api --replicas=5
```

## Troubleshooting

### Check Pod Status
```bash
kubectl describe pod POD_NAME
kubectl logs POD_NAME
```

### Database Issues
```bash
# Check Cloud SQL status
gcloud sql instances describe spark-intelligence-db

# View recent errors in Cloud Logging
gcloud logging read "resource.type=cloudsql_database" --limit 50
```

### Network Issues
```bash
# Check service endpoints
kubectl get endpoints

# Test connectivity
kubectl exec -it POD_NAME -- curl http://localhost:8000/health
```

## Cleanup

### Remove Kubernetes Resources
```bash
kubectl delete deployment spark-intelligence-api
kubectl delete service spark-intelligence-api
kubectl delete ingress spark-intelligence-ingress
```

### Destroy Infrastructure
```bash
terraform destroy -var="gcp_project_id=$GCP_PROJECT_ID"
```

### Remove GCP Project
```bash
gcloud projects delete $GCP_PROJECT_ID
```
