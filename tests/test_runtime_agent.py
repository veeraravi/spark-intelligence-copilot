"""Test suite for runtime agent"""

import pytest
from orchestration.state_model import AgentState
from agents.runtime_agent import RuntimeAgent


@pytest.fixture
def test_state():
    """Create a test state"""
    return AgentState(
        job_id="test_job_1",
        job_name="Test Job",
        source_type="jdbc",
        table_name="test_table",
        partition_count=10,
        execution_time_ms=120000,  # 2 minutes
        cpu_utilization=0.75,
        memory_used_mb=2048
    )


@pytest.mark.asyncio
async def test_runtime_agent_detects_long_execution(test_state):
    """Test detection of long execution time"""
    agent = RuntimeAgent()
    result_state = await agent.analyze(test_state)
    
    assert len(result_state.issues_detected) > 0
    assert len(result_state.recommendations) > 0


@pytest.mark.asyncio
async def test_runtime_agent_detects_high_memory_usage(test_state):
    """Test detection of high memory usage"""
    test_state.memory_used_mb = 9000
    
    agent = RuntimeAgent()
    result_state = await agent.analyze(test_state)
    
    recommendations = [r for r in result_state.recommendations if "compression" in r.lower()]
    assert len(recommendations) > 0
