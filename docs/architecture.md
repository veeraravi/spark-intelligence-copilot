# Spark Intelligence Copilot - Architecture Guide

## Overview

Spark Intelligence Copilot is an AI-powered platform for analyzing, monitoring, and optimizing Apache Spark and Databricks jobs. It combines machine learning, rule-based engines, and retrieval-augmented generation (RAG) to provide intelligent recommendations for performance optimization.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │         Orchestration Layer                     │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │  Graph Builder & State Management        │  │   │
│  │  │  ┌────────────────────────────────────┐  │  │   │
│  │  │  │ Agent 1: Metadata Analysis          │  │  │   │
│  │  │  │ Agent 2: Partition Strategy         │  │  │   │
│  │  │  │ Agent 3: Runtime Prediction         │  │  │   │
│  │  │  │ Agent 4: Data Skew Detection        │  │  │   │
│  │  │  │ Agent 5: Delta Lake Optimization    │  │  │   │
│  │  │  │ Agent 6: Cost Analysis              │  │  │   │
│  │  │  └────────────────────────────────────┘  │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   Rules  │  │    RAG   │  │    ML    │            │
│  │  Engine  │  │ Pipeline │  │  Models  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
         │                │                    │
         ▼                ▼                    ▼
    ┌──────────┐  ┌──────────┐       ┌──────────────┐
    │ Storage  │  │Connectors│       │ Data Sources │
    │  Layer   │  │  (GCS,   │       │  (JDBC, API, │
    │(Database)│  │  BQ, Etc)│       │   Kafka)     │
    └──────────┘  └──────────┘       └──────────────┘
```

## Core Components

### 1. **API Layer**
- **Framework**: FastAPI
- **Endpoints**: Job analysis, partition analysis, recommendations
- **Authentication**: API key-based
- **Rate Limiting**: Token bucket algorithm

### 2. **Orchestration Layer**
- **State Model**: Immutable state passing through agents
- **Graph Builder**: Manages workflow DAG execution
- **Agent Pattern**: Specialized agents for different analyses

### 3. **Agents**
Each agent performs specialized analysis:

- **MetadataAgent**: Extracts schema, column types, table statistics
- **PartitionAgent**: Analyzes partitioning strategy and recommendations
- **RuntimeAgent**: Predicts runtime and identifies bottlenecks
- **SkewAgent**: Detects data skew and suggests mitigation
- **DeltaAgent**: Delta Lake-specific optimizations
- **CostAgent**: Estimates compute costs and savings

### 4. **Rules Engine**
- **PartitionRules**: Optimal partition count calculations
- **SparkConfigRules**: CPU, memory, shuffle partition recommendations
- **SkewRules**: Skew detection and mitigation strategies

### 5. **RAG Pipeline**
- **Document Ingestion**: Spark docs, Databricks docs, internal logs
- **Vector Store**: Pinecone/Weaviate for embeddings
- **Retriever**: Semantic search for relevant documentation
- **ReasoningAgent**: Uses retrieved context for better recommendations

### 6. **ML Models**
- **RuntimePredictor**: Linear regression for runtime prediction
- **FeatureBuilder**: Feature engineering from job metadata
- **ModelTraining**: Training pipeline for all predictive models

### 7. **Storage Layer**
- **Database**: PostgreSQL for metadata and metrics
- **MetadataRepository**: Table schema and statistics
- **MetricsRepository**: Historical job performance data

### 8. **Connectors**
- **SparkEventParser**: Parse Spark event logs
- **GCSClient**: Google Cloud Storage integration
- **BigQueryClient**: BigQuery data warehouse integration

## Data Flow

1. **Ingest**: Spark event logs ingested via Kafka or direct API
2. **Parse**: SparkEventParser extracts structured metrics
3. **Analyze**: Orchestration layer routes through appropriate agents
4. **Enrich**: RAG pipeline retrieves relevant documentation
5. **Recommend**: Rules engine + ML models generate recommendations
6. **Store**: Results persisted in PostgreSQL
7. **Return**: Recommendations returned via REST API

## Deployment Architecture

### Local Development
```bash
docker-compose up  # Starts all services locally
```

### Cloud Deployment (GCP)
- **Compute**: Google Kubernetes Engine (GKE)
- **Database**: Cloud SQL (PostgreSQL)
- **Data Warehouse**: BigQuery
- **ML**: Vertex AI
- **Storage**: Google Cloud Storage
- **Networking**: Cloud Load Balancing, Cloud Armor

### Infrastructure as Code
- **Terraform**: All GCP resources defined in code
- **Kubernetes**: Manifests for deployment, service, ingress
- **Docker**: Containerized application

## Scalability Considerations

1. **Horizontal Scaling**: Load balancer distributes requests across API instances
2. **Database**: Cloud SQL with automatic backups and failover
3. **Message Queue**: Kafka for asynchronous event processing
4. **Caching**: Redis for result caching
5. **Vector Store**: Pinecone for distributed embedding search

## Security

- Service accounts with minimal permissions
- Network policies for internal communication
- Secrets management via Google Secret Manager
- TLS/SSL for all external communication
- Input validation and sanitization
- Rate limiting per API key

## Monitoring and Logging

- Google Cloud Logging for centralized logs
- Cloud Monitoring for metrics and alerts
- Distributed tracing with Cloud Trace
- Application Performance Monitoring (APM)

## Future Enhancements

1. Real-time streaming analysis
2. Multi-cloud support (AWS, Azure)
3. GraphQL API alongside REST
4. Advanced ML models (neural networks)
5. Cost prediction and optimization
6. Automated job tuning
