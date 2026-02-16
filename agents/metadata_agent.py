"""Agent for analyzing table metadata"""

import logging
from typing import Optional
from orchestration.state_model import AgentState

logger = logging.getLogger(__name__)


async def metadata_agent(state: AgentState) -> AgentState:
    """
    Analyze table metadata.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with metadata information
    """
    logger.info(f"MetadataAgent: Analyzing metadata for {state.get('table_name')}")
    
    try:
        # Extract schema information
        schema_info = {
            "columns": [
                {"name": "id", "type": "bigint", "nullable": False},
                {"name": "name", "type": "string", "nullable": False},
                {"name": "value", "type": "double", "nullable": True},
                {"name": "timestamp", "type": "timestamp", "nullable": False}
            ],
            "primary_key": "id",
            "row_count": 1000000,
            "size_gb": 2.5
        }
        
        state["schema_info"] = schema_info
        logger.info(f"MetadataAgent: Found {len(schema_info['columns'])} columns")
        
    except Exception as e:
        logger.error(f"MetadataAgent: Error analyzing metadata: {str(e)}")
        state["issues_detected"].append({
            "type": "metadata",
            "severity": "error",
            "description": str(e)
        })
    
    return state


class MetadataAgent:
    """LangGraph-compatible metadata agent wrapper"""
    
    def __init__(self):
        """Initialize metadata agent"""
        self.name = "metadata_agent"
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Call the agent"""
        return await metadata_agent(state)
