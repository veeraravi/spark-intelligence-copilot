"""Agent for analyzing partition strategy"""

import logging
from orchestration.state_model import AgentState

logger = logging.getLogger(__name__)


async def partition_agent(state: AgentState) -> AgentState:
    """
    Analyze partition strategy.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with partition recommendations
    """
    logger.info(f"PartitionAgent: Analyzing partitions for {state.get('table_name')}")
    
    try:
        partition_count = state.get("partition_count", 0)
        
        # Analyze partition count
        if partition_count == 0:
            state["issues_detected"].append({
                "type": "partition",
                "severity": "warning",
                "description": "No partition information available"
            })
            state["partition_strategy"] = "unpartitioned"
        elif partition_count < 10:
            state["recommendations"].append("Increase partition count for better parallelism")
            state["partition_strategy"] = "under-partitioned"
        elif partition_count > 1000:
            state["recommendations"].append("Consider reducing partition count to avoid overhead")
            state["partition_strategy"] = "over-partitioned"
        else:
            state["partition_strategy"] = "optimal"
        
        logger.info(f"PartitionAgent: Strategy identified: {state.get('partition_strategy')}")
        
    except Exception as e:
        logger.error(f"PartitionAgent: Error analyzing partitions: {str(e)}")
        state["issues_detected"].append({
            "type": "partition",
            "severity": "error",
            "description": str(e)
        })
    
    return state


class PartitionAgent:
    """LangGraph-compatible partition agent wrapper"""
    
    def __init__(self):
        """Initialize partition agent"""
        self.name = "partition_agent"
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Call the agent"""
        return await partition_agent(state)
