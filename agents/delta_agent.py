"""Agent for analyzing Delta Lake operations"""

import logging
from orchestration.state_model import AgentState

logger = logging.getLogger(__name__)


async def delta_agent(state: AgentState) -> AgentState:
    """
    Analyze Delta Lake operations.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with Delta-specific recommendations
    """
    logger.info(f"DeltaAgent: Analyzing Delta Lake operations for {state.get('table_name')}")
    
    try:
        # Check if table uses Delta format
        if state.get("source_type") == "delta":
            state["recommendations"].append("Enable Delta Lake Z-ordering for faster scans")
            state["recommendations"].append("Run OPTIMIZE command to compact small files")
            state["recommendations"].append("Configure auto-compaction for WRITE operations")
            
            logger.info("DeltaAgent: Delta Lake recommendations generated")
        
    except Exception as e:
        logger.error(f"DeltaAgent: Error analyzing Delta operations: {str(e)}")
        state["issues_detected"].append({
            "type": "delta",
            "severity": "error",
            "description": str(e)
        })
    
    return state


class DeltaAgent:
    """LangGraph-compatible Delta Lake agent wrapper"""
    
    def __init__(self):
        """Initialize delta agent"""
        self.name = "delta_agent"
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Call the agent"""
        return await delta_agent(state)
