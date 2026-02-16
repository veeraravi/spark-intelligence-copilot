"""Test suite for partition agent"""

import pytest
from orchestration.state_model import AgentState
from agents.partition_agent import PartitionAgent


@pytest.fixture
def test_state():
    """Create a test state"""
    return AgentState(
        job_id="test_job_1",
        job_name="Test Job",
        source_type="delta",
        table_name="test_table",
        partition_count=5,
        execution_time_ms=5000
    )


@pytest.mark.asyncio
async def test_partition_agent_detects_under_partitioning(test_state):
    """Test detection of under-partitioning"""
    agent = PartitionAgent()
    result_state = await agent.analyze(test_state)
    
    assert result_state.partition_strategy == "under-partitioned"
    assert len(result_state.recommendations) > 0


@pytest.mark.asyncio
async def test_partition_agent_detects_optimal_partitioning():
    """Test detection of optimal partitioning"""
    state = AgentState(
        job_id="test_job_2",
        job_name="Test Job 2",
        source_type="delta",
        table_name="test_table_2",
        partition_count=100,
        execution_time_ms=5000
    )
    
    agent = PartitionAgent()
    result_state = await agent.analyze(state)
    
    assert result_state.partition_strategy == "optimal"
