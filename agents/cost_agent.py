"""Agent for cost analysis and optimization"""

import logging
from orchestration.state_model import AgentState

logger = logging.getLogger(__name__)


async def cost_agent(state: AgentState) -> AgentState:
    """
    Analyze and optimize costs.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with cost analysis
    """
    logger.info(f"CostAgent: Analyzing costs for job {state.get('job_id')}")
    
    try:
        cpu_util = state.get("cpu_utilization", 0)
        exec_time = state.get("execution_time_ms", 0)
        memory_mb = state.get("memory_used_mb", 0)
        
        # Calculate estimated costs (simulated)
        cpu_cost = cpu_util * exec_time / 1000 * 0.10
        memory_cost = memory_mb / 1024 * exec_time / 1000 * 0.05
        total_cost = cpu_cost + memory_cost
        
        # Provide cost optimization recommendations
        savings_percentage = 30
        state["recommendations"].append(
            f"Estimated cost savings: ${total_cost * savings_percentage / 100:.2f} ({savings_percentage}%)"
        )
        
        logger.info(f"CostAgent: Cost analysis completed, estimated savings: {savings_percentage}%")
        
    except Exception as e:
        logger.error(f"CostAgent: Error analyzing costs: {str(e)}")
        state["issues_detected"].append({
            "type": "cost",
            "severity": "error",
            "description": str(e)
        })
    
    return state


class CostAgent:
    """LangGraph-compatible cost agent wrapper"""
    
    def __init__(self):
        """Initialize cost agent"""
        self.name = "cost_agent"
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Call the agent"""
        return await cost_agent(state)
