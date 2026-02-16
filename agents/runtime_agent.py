"""Agent for predicting and optimizing runtime"""

import logging
from orchestration.state_model import AgentState

logger = logging.getLogger(__name__)


async def runtime_agent(state: AgentState) -> AgentState:
    """
    Analyze and predict runtime performance.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with runtime analysis
    """
    logger.info(f"RuntimeAgent: Analyzing runtime for job {state.get('job_id')}")
    
    try:
        execution_time = state.get("execution_time_ms", 0)
        cpu_util = state.get("cpu_utilization", 0)
        memory_mb = state.get("memory_used_mb", 0)
        
        # Analyze runtime metrics
        if execution_time > 60000:  # > 1 minute
            state["issues_detected"].append({
                "type": "runtime",
                "severity": "warning",
                "description": "Long execution time detected"
            })
            state["recommendations"].append("Consider caching intermediate results")
            state["recommendations"].append("Enable adaptive query execution")
        
        if cpu_util < 0.5:
            state["recommendations"].append("CPU utilization is low - consider reducing executor count")
        elif cpu_util > 0.95:
            state["recommendations"].append("High CPU utilization - add more executors")
        
        if memory_mb > 8192:
            state["recommendations"].append("High memory usage - consider data compression")
        
        logger.info(f"RuntimeAgent: Runtime analysis completed")
        
    except Exception as e:
        logger.error(f"RuntimeAgent: Error analyzing runtime: {str(e)}")
        state["issues_detected"].append({
            "type": "runtime",
            "severity": "error",
            "description": str(e)
        })
    
    return state


class RuntimeAgent:
    """LangGraph-compatible runtime agent wrapper"""
    
    def __init__(self):
        """Initialize runtime agent"""
        self.name = "runtime_agent"
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Call the agent"""
        return await runtime_agent(state)
