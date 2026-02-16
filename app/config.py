"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = "Spark Intelligence Copilot"
    api_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Configuration
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://example.com"
    ]
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/spark_copilot")
    
    # Cloud Configuration
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")
    gcp_region: str = os.getenv("GCP_REGION", "us-central1")
    
    # Vector Store Configuration
    vectorstore_type: str = os.getenv("VECTORSTORE_TYPE", "pinecone")
    vectorstore_index: str = os.getenv("VECTORSTORE_INDEX", "spark-intelligence")
    
    # ML Model Configuration
    model_registry_path: str = os.getenv("MODEL_REGISTRY_PATH", "/models")
    runtime_predictor_model: str = os.getenv("RUNTIME_PREDICTOR_MODEL", "runtime_predictor_v1")
    
    # Spark Configuration
    spark_master_url: str = os.getenv("SPARK_MASTER_URL", "local")
    spark_appname: str = "SparkIntelligenceCopilot"
    
    # Kafka Configuration
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic_events: str = "spark-events"
    kafka_topic_metrics: str = "spark-metrics"
    
    # RAG Configuration
    rag_similarity_threshold: float = 0.7
    rag_top_k_results: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
