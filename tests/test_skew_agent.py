"""Test suite for skew agent"""

import pytest
from orchestration.state_model import AgentState
from agents.skew_agent import SkewAgent


@pytest.fixture
def test_state():
    """Create a test state"""
    return AgentState(
        job_id="test_job_1",
        job_name="Test Job",
        source_type="delta",
        table_name="test_table",
        partition_count=10,
        execution_time_ms=5000
    )


@pytest.mark.asyncio
async def test_skew_agent_detects_skew(test_state):
    """Test detection of data skew"""
    agent = SkewAgent()
    result_state = await agent.analyze(test_state)
    
    assert len(result_state.issues_detected) > 0
    assert len(result_state.skewed_columns) > 0
    assert len(result_state.recommendations) > 0


@pytest.mark.asyncio
async def test_skew_agent_provides_mitigation_strategies(test_state):
    """Test that skew agent provides mitigation strategies"""
    agent = SkewAgent()
    result_state = await agent.analyze(test_state)
    
    recommendations = result_state.recommendations
    assert any("salting" in r.lower() for r in recommendations)
