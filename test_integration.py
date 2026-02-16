"""Quick integration test for LangGraph setup"""

import asyncio
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_langgraph_integration():
    """Test that all LangGraph components work together"""
    
    print("Testing LangGraph Integration...")
    print("-" * 50)
    
    try:
        # Test 1: Import state model
        print("✓ Testing state model import...")
        from orchestration.state_model import create_agent_state, AgentState
        print("  └─ AgentState imported successfully")
        
        # Test 2: Create initial state
        print("✓ Testing state creation...")
        initial_state = create_agent_state(
            job_id="test_job_001",
            job_name="Test Job",
            source_type="parquet",
            table_name="test_table",
            partition_count=50,
            execution_time_ms=3000,
            cpu_utilization=0.65,
            memory_used_mb=1024,
        )
        print(f"  └─ State created with {len(initial_state)} fields")
        print(f"  └─ Initial recommendations: {initial_state['recommendations']}")
        print(f"  └─ Initial issues: {initial_state['issues_detected']}")
        
        # Test 3: Import all agents
        print("✓ Testing agent imports...")
        from agents.metadata_agent import MetadataAgent, metadata_agent
        from agents.partition_agent import PartitionAgent, partition_agent
        from agents.runtime_agent import RuntimeAgent, runtime_agent
        from agents.skew_agent import SkewAgent, skew_agent
        from agents.delta_agent import DeltaAgent, delta_agent
        from agents.cost_agent import CostAgent, cost_agent
        print("  └─ All 6 agents imported successfully")
        
        # Test 4: Run individual agents
        print("✓ Testing individual agent execution...")
        
        # Test metadata agent
        state = await metadata_agent(initial_state.copy())
        print(f"  └─ metadata_agent: Added schema_info = {bool(state.get('schema_info'))}")
        
        # Test partition agent
        state = await partition_agent(state)
        print(f"  └─ partition_agent: Partition strategy = {state.get('partition_strategy')}")
        print(f"    Recommendations count: {len(state['recommendations'])}")
        
        # Test runtime agent
        state = await runtime_agent(state)
        print(f"  └─ runtime_agent: Issues detected = {len(state['issues_detected'])}")
        
        # Test skew agent
        state = await skew_agent(state)
        print(f"  └─ skew_agent: Skewed columns = {state.get('skewed_columns')}")
        
        # Test delta agent
        state = await delta_agent(state)
        print(f"  └─ delta_agent: Recommendations now = {len(state['recommendations'])}")
        
        # Test cost agent
        state = await cost_agent(state)
        print(f"  └─ cost_agent: Final recommendations = {len(state['recommendations'])}")
        
        # Test 5: Import graph builder
        print("✓ Testing graph builder import...")
        from orchestration.graph_builder import SparkIntelligenceGraph, build_spark_optimization_graph
        print("  └─ SparkIntelligenceGraph imported successfully")
        
        # Test 6: Build graph
        print("✓ Testing graph construction...")
        agents_dict = {
            "metadata_agent": MetadataAgent(),
            "partition_agent": PartitionAgent(),
            "runtime_agent": RuntimeAgent(),
            "skew_agent": SkewAgent(),
            "delta_agent": DeltaAgent(),
            "cost_agent": CostAgent()
        }
        
        graph = build_spark_optimization_graph(agents_dict)
        print("  └─ Graph built successfully")
        
        # Test 7: Compile graph
        print("✓ Testing graph compilation...")
        compiled_graph = graph.compile()
        print("  └─ Graph compiled successfully")
        
        # Test 8: Execute full workflow
        print("✓ Testing full workflow execution...")
        fresh_state = create_agent_state(
            job_id="test_workflow",
            job_name="Workflow Test",
            source_type="delta",
            table_name="workflow_table",
            partition_count=100,
            execution_time_ms=5000,
            cpu_utilization=0.80,
            memory_used_mb=2048,
        )
        
        result = await compiled_graph.ainvoke(fresh_state)
        print("  └─ Workflow executed successfully")
        print(f"  └─ Final recommendations: {len(result.get('recommendations', []))}")
        for i, rec in enumerate(result.get('recommendations', [])[:3], 1):
            print(f"    {i}. {rec[:60]}...")
        
        print(f"  └─ Final issues: {len(result.get('issues_detected', []))}")
        for i, issue in enumerate(result.get('issues_detected', [])[:2], 1):
            print(f"    {i}. {issue.get('type')}: {issue.get('description')[:50]}...")
        
        print("\n" + "=" * 50)
        print("✅ All LangGraph integration tests passed!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error:")
        print(f"  {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_langgraph_integration())
    sys.exit(0 if success else 1)
