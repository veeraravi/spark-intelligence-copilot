"""State model for LangGraph-based agent workflow"""

from typing import Dict, List, Any, Optional, TypedDict
from typing_extensions import Annotated
import operator
from datetime import datetime


class AgentState(TypedDict):
    """
    State object for LangGraph workflow.
    Uses TypedDict for compatibility with LangGraph.
    """
    job_id: str
    job_name: str
    source_type: str
    
    # Metadata information
    table_name: Optional[str]
    schema_info: Dict[str, Any]
    
    # Partition information
    partition_count: int
    partition_strategy: Optional[str]
    skewed_columns: List[str]
    
    # Runtime metrics
    execution_time_ms: int
    cpu_utilization: float
    memory_used_mb: int
    
    # Analysis results
    recommendations: Annotated[List[str], operator.add]
    issues_detected: Annotated[List[Dict[str, Any]], operator.add]
    
    # Metadata
    created_at: str
    updated_at: str


def create_agent_state(
    job_id: str,
    job_name: str,
    source_type: str,
    table_name: Optional[str] = None,
    schema_info: Optional[Dict[str, Any]] = None,
    partition_count: int = 0,
    execution_time_ms: int = 0,
    cpu_utilization: float = 0.0,
    memory_used_mb: int = 0,
) -> AgentState:
    """
    Factory function to create an AgentState.
    
    Args:
        job_id: Unique job identifier
        job_name: Human-readable job name
        source_type: Type of data source
        table_name: Optional table name
        schema_info: Optional schema information
        partition_count: Number of partitions
        execution_time_ms: Execution time in milliseconds
        cpu_utilization: CPU utilization ratio
        memory_used_mb: Memory used in MB
        
    Returns:
        AgentState instance
    """
    return AgentState(
        job_id=job_id,
        job_name=job_name,
        source_type=source_type,
        table_name=table_name,
        schema_info=schema_info or {},
        partition_count=partition_count,
        partition_strategy=None,
        skewed_columns=[],
        execution_time_ms=execution_time_ms,
        cpu_utilization=cpu_utilization,
        memory_used_mb=memory_used_mb,
        recommendations=[],
        issues_detected=[],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    )
