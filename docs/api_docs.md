# Spark Intelligence Copilot - API Documentation

## Overview

The Spark Intelligence Copilot API provides endpoints for analyzing Spark jobs, detecting optimization opportunities, and retrieving performance recommendations.

**Base URL**: `http://localhost:8000/api/v1`

## Authentication

All API requests require an API key header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the service is running.

**Response**:
```json
{
  "status": "healthy",
  "service": "spark-intelligence-copilot"
}
```

### 2. Analyze Job

**POST** `/analyze/job`

Analyze a Spark job and provide optimization recommendations.

**Request Body**:
```json
{
  "job_id": "job_20231215_001",
  "job_name": "ETL Pipeline - Daily",
  "metrics": {
    "execution_time_ms": 300000,
    "cpu_utilization": 0.75,
    "memory_used_mb": 4096,
    "total_tasks": 250
  }
}
```

**Response**:
```json
{
  "job_id": "job_20231215_001",
  "recommendations": [
    "Optimize partition count for better parallelism",
    "Enable columnar caching for intermediate results",
    "Use broadcast join for small lookup tables"
  ],
  "optimization_score": 0.85,
  "estimated_savings": {
    "cpu": "15%",
    "memory": "20%",
    "time": "25%"
  }
}
```

**Status Codes**:
- `200`: Success
- `400`: Invalid request
- `500`: Server error

### 3. Analyze Partition

**POST** `/analyze/partition`

Analyze partition strategy and detect data skew.

**Request Body**:
```json
{
  "table_name": "transactions",
  "partition_count": 32,
  "data_skew_ratio": 0.45
}
```

**Response**:
```json
{
  "table_name": "transactions",
  "is_skewed": true,
  "skew_score": 0.45,
  "recommended_partitions": 64
}
```

### 4. Get Job Recommendations

**GET** `/recommendations/{job_id}`

Retrieve stored recommendations for a specific job.

**Path Parameters**:
- `job_id` (string, required): The job ID

**Response**:
```json
{
  "job_id": "job_20231215_001",
  "recommendations": [
    {
      "type": "partition",
      "description": "Rebalance partitions using hash distribution"
    },
    {
      "type": "cache",
      "description": "Cache lineage data before aggregation"
    },
    {
      "type": "join",
      "description": "Use broadcast join strategy for smaller table"
    }
  ]
}
```

### 5. Get Job Metrics

**GET** `/metrics/{job_id}`

Retrieve performance metrics for a job.

**Path Parameters**:
- `job_id` (string, required): The job ID

**Response**:
```json
{
  "job_id": "job_20231215_001",
  "execution_time_ms": 300000,
  "total_tasks": 250,
  "successful_tasks": 248,
  "failed_tasks": 2,
  "memory_used_mb": 4096,
  "cpu_utilization": 0.75
}
```

## Error Responses

### 400 - Bad Request
```json
{
  "detail": "Invalid job_id format"
}
```

### 404 - Not Found
```json
{
  "detail": "Job not found: job_20231215_999"
}
```

### 500 - Internal Server Error
```json
{
  "detail": "Error analyzing job: Database connection failed"
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse:
- **Limit**: 1000 requests per hour per API key
- **Rate Limit Headers**:
  - `X-RateLimit-Limit`: 1000
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

## Pagination

Endpoints that return lists support pagination:
- `limit`: Number of results (default: 20, max: 100)
- `offset`: Number of results to skip (default: 0)

Example:
```
GET /api/v1/recommendations?limit=50&offset=100
```

## Webhooks

Configure webhooks to receive notifications:

**POST** `/webhooks`

```json
{
  "event": "job.completed",
  "url": "https://example.com/webhook",
  "secret": "webhook_secret_key"
}
```

## SDK Usage

### Python

```python
import requests

api_key = "your_api_key"
headers = {"Authorization": f"Bearer {api_key}"}

# Analyze job
response = requests.post(
    "http://localhost:8000/api/v1/analyze/job",
    json={
        "job_id": "job_001",
        "job_name": "ETL Pipeline",
        "metrics": {
            "execution_time_ms": 300000,
            "cpu_utilization": 0.75,
            "memory_used_mb": 4096
        }
    },
    headers=headers
)

recommendations = response.json()
print(recommendations["recommendations"])
```

### JavaScript

```javascript
const apiKey = "your_api_key";
const baseUrl = "http://localhost:8000/api/v1";

async function analyzeJob(jobData) {
  const response = await fetch(`${baseUrl}/analyze/job`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(jobData)
  });
  
  return response.json();
}

// Usage
const recommendations = await analyzeJob({
  job_id: "job_001",
  job_name: "ETL Pipeline",
  metrics: {
    execution_time_ms: 300000,
    cpu_utilization: 0.75,
    memory_used_mb: 4096
  }
});
```

## Best Practices

1. **Cache Results**: Cache recommendations for the same job to reduce API calls
2. **Batch Requests**: Use batch endpoints when analyzing multiple jobs
3. **Handle Timeouts**: Implement exponential backoff for retries
4. **Monitor Usage**: Track API usage to optimize costs
5. **Secure Keys**: Never expose API keys in client-side code

## Support

For issues or questions:
- GitHub Issues: https://github.com/spark-intelligence/copilot/issues
- Email: support@sparkintelligence.com
