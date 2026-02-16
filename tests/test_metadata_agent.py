"""Test suite for metadata agent"""

import pytest
from orchestration.state_model import AgentState
from agents.metadata_agent import MetadataAgent


@pytest.fixture
def test_state():
    """Create a test state"""
    return AgentState(
        job_id="test_job_1",
        job_name="Test Job",
        source_type="jdbc",
        table_name="test_table",
        partition_count=10,
        execution_time_ms=5000,
        cpu_utilization=0.75,
        memory_used_mb=2048
    )


@pytest.mark.asyncio
async def test_metadata_agent_analyze(test_state):
    """Test metadata agent analysis"""
    agent = MetadataAgent()
    result_state = await agent.analyze(test_state)
    
    assert result_state.schema_info is not None
    assert "columns" in result_state.schema_info
    assert len(result_state.schema_info["columns"]) > 0


@pytest.mark.asyncio
async def test_metadata_agent_extracts_column_info(test_state):
    """Test that metadata agent extracts column information"""
    agent = MetadataAgent()
    result_state = await agent.analyze(test_state)
    
    columns = result_state.schema_info.get("columns", [])
    assert any(col["name"] == "id" for col in columns)
