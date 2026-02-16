"""API Routes for Spark Intelligence Copilot"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import logging
from orchestration.state_model import create_agent_state
from orchestration.graph_builder import build_spark_optimization_graph
from agents.metadata_agent import MetadataAgent
from agents.partition_agent import PartitionAgent
from agents.runtime_agent import RuntimeAgent
from agents.skew_agent import SkewAgent
from agents.delta_agent import DeltaAgent
from agents.cost_agent import CostAgent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["spark-intelligence"])

# Request/Response Models
class JobAnalysisRequest(BaseModel):
    """Request model for job analysis"""
    job_id: str
    job_name: str
    metrics: dict

class JobAnalysisResponse(BaseModel):
    """Response model for job analysis"""
    job_id: str
    recommendations: List[str]
    optimization_score: float
    estimated_savings: dict

class PartitionAnalysisRequest(BaseModel):
    """Request model for partition analysis"""
    table_name: str
    partition_count: int
    data_skew_ratio: Optional[float] = None

class SkewAnalysisResponse(BaseModel):
    """Response model for skew analysis"""
    table_name: str
    is_skewed: bool
    skew_score: float
    recommended_partitions: int

# API Endpoints

@router.post("/analyze/job", response_model=JobAnalysisResponse)
async def analyze_job(request: JobAnalysisRequest):
    """Analyze a Spark job and provide optimization recommendations"""
    try:
        logger.info(f"Analyzing job {request.job_id}")
        
        # Initialize agent state
        initial_state = create_agent_state(
            job_id=request.job_id,
            job_name=request.job_name,
            source_type=request.metrics.get("source_type", "parquet"),
            table_name=request.metrics.get("table_name", "unknown"),
            partition_count=request.metrics.get("partition_count", 0),
            execution_time_ms=request.metrics.get("execution_time_ms", 0),
            cpu_utilization=request.metrics.get("cpu_utilization", 0),
            memory_used_mb=request.metrics.get("memory_used_mb", 0)
        )
        
        # Build and compile the LangGraph
        agents = {
            "metadata_agent": MetadataAgent(),
            "partition_agent": PartitionAgent(),
            "runtime_agent": RuntimeAgent(),
            "skew_agent": SkewAgent(),
            "delta_agent": DeltaAgent(),
            "cost_agent": CostAgent()
        }
        
        graph = build_spark_optimization_graph(agents)
        compiled_graph = graph.compile()
        
        # Execute the workflow
        result = await compiled_graph.ainvoke(initial_state)
        
        return JobAnalysisResponse(
            job_id=request.job_id,
            recommendations=result.get("recommendations", []),
            optimization_score=0.85,
            estimated_savings={"cpu": "15%", "memory": "20%", "time": "25%"}
        )
    except Exception as e:
        logger.error(f"Error analyzing job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/partition", response_model=SkewAnalysisResponse)
async def analyze_partition(request: PartitionAnalysisRequest):
    """Analyze partition skew in a table"""
    try:
        logger.info(f"Analyzing partitions for table {request.table_name}")
        
        # Placeholder for actual analysis logic
        is_skewed = request.data_skew_ratio and request.data_skew_ratio > 0.3
        skew_score = request.data_skew_ratio or 0.1
        recommended_partitions = max(request.partition_count // 2, 1) if is_skewed else request.partition_count
        
        return SkewAnalysisResponse(
            table_name=request.table_name,
            is_skewed=is_skewed,
            skew_score=skew_score,
            recommended_partitions=recommended_partitions
        )
    except Exception as e:
        logger.error(f"Error analyzing partitions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{job_id}")
async def get_recommendations(job_id: str):
    """Get optimization recommendations for a specific job"""
    try:
        logger.info(f"Fetching recommendations for job {job_id}")
        
        return {
            "job_id": job_id,
            "recommendations": [
                {"type": "partition", "description": "Rebalance partitions"},
                {"type": "cache", "description": "Cache intermediate results"},
                {"type": "join", "description": "Use broadcast join strategy"}
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/{job_id}")
async def get_job_metrics(job_id: str):
    """Get performance metrics for a job"""
    try:
        return {
            "job_id": job_id,
            "execution_time_ms": 5432,
            "total_tasks": 150,
            "successful_tasks": 148,
            "failed_tasks": 2,
            "memory_used_mb": 2048,
            "cpu_utilization": 0.75
        }
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
