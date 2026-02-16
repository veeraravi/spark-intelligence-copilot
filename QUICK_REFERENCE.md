# LangGraph Integration - Quick Reference Guide

## 🚀 Quick Start (2 minutes)

### Verify Installation
```bash
cd spark-intelligence-copilot
python test_integration.py
```

Expected output: `✅ All LangGraph integration tests passed!`

### Basic Workflow
```python
from orchestration import create_agent_state, build_spark_optimization_graph
from agents.metadata_agent import MetadataAgent
from agents.partition_agent import PartitionAgent
from agents.runtime_agent import RuntimeAgent
from agents.skew_agent import SkewAgent
from agents.delta_agent import DeltaAgent
from agents.cost_agent import CostAgent

# 1. Create state (factory function)
state = create_agent_state(
    job_id="job_001",
    job_name="My Job",
    source_type="delta",
    table_name="my_table",
    partition_count=100,
    execution_time_ms=5000,
    cpu_utilization=0.75,
    memory_used_mb=2048
)

# 2. Create agents
agents = {
    "metadata_agent": MetadataAgent(),
    "partition_agent": PartitionAgent(),
    "runtime_agent": RuntimeAgent(),
    "skew_agent": SkewAgent(),
    "delta_agent": DeltaAgent(),
    "cost_agent": CostAgent()
}

# 3. Build and execute
graph = build_spark_optimization_graph(agents)
result = await graph.compile().ainvoke(state)

# 4. Access results
recommendations = result["recommendations"]
issues = result["issues_detected"]
```

---

## 📚 Documentation Map

| Topic | File | Section |
|-------|------|---------|
| **Overview** | README_LANGGRAPH.md | Quick Start |
| **Architecture** | LANGGRAPH_INTEGRATION.md | Architecture Changes |
| **Usage Guide** | LANGGRAPH_GUIDE.md | Building and Running Graphs |
| **Change Details** | LANGGRAPH_CHANGELOG.md | Detailed Change Log |
| **Completion** | LANGGRAPH_COMPLETION.md | Verification Checklist |

---

## 🔧 Key Components

### State Model
**File**: `orchestration/state_model.py`
- **Class**: `AgentState` (TypedDict)
- **Factory**: `create_agent_state(...)`
- **Key Fields**: 15 fields including recommendations and issues_detected lists

### Graph Builder
**File**: `orchestration/graph_builder.py`
- **Class**: `SparkIntelligenceGraph`
- **Factory**: `build_spark_optimization_graph(agents)`
- **Execution**: `await compiled_graph.ainvoke(state)`

### Agents (6 total)
**Files**: `agents/{metadata,partition,runtime,skew,delta,cost}_agent.py`
- Each has async function + class wrapper
- Pattern: Read state → Analyze → Update state → Return state

### API Integration
**File**: `app/api_routes.py`
- **Endpoint**: `POST /api/v1/analyze/job`
- **Flow**: Request → State Creation → Graph Execution → Response

---

## 💻 Common Tasks

### Add a New Agent
```python
# 1. Create agents/new_agent.py
async def new_agent(state: AgentState) -> AgentState:
    # Analyze something
    state["field"] = result
    state["recommendations"].append("recommendation")
    return state

class NewAgent:
    async def __call__(self, state: AgentState) -> AgentState:
        return await new_agent(state)

# 2. Add to graph in build_spark_optimization_graph()
agents["new_agent"] = NewAgent()
graph.add_node("new_agent", new_agent)
```

### Access State Fields
```python
# Read
value = state.get("field_name", default_value)
value = state["field_name"]  # Raises KeyError if missing

# Write (lists auto-merged)
state["recommendations"].append("text")
state["issues_detected"].append({"type": "...", "description": "..."})

# Write (other fields)
state["field_name"] = value
```

### Handle Errors
```python
try:
    # Analysis code
    return state
except Exception as e:
    state["issues_detected"].append({
        "type": "agent_name",
        "severity": "error",
        "description": str(e)
    })
    return state
```

### Run Async Code in FastAPI
```python
@router.post("/endpoint")
async def my_endpoint(request: MyRequest):
    # Already in async context
    state = create_agent_state(...)
    graph = build_spark_optimization_graph(agents)
    result = await graph.compile().ainvoke(state)
    return response
```

---

## ❌ Common Mistakes

### ❌ Wrong: Using old API
```python
state.job_id = "value"  # Wrong - not a dataclass anymore
state.add_recommendation("text")  # Wrong - method doesn't exist
```

### ✅ Right: Using new API
```python
state["job_id"] = "value"  # Correct - TypedDict
state["recommendations"].append("text")  # Correct - list access
```

### ❌ Wrong: Forgetting factory function
```python
state = AgentState(...)  # Wrong - needs all fields
```

### ✅ Right: Using factory
```python
state = create_agent_state(
    job_id="...",
    job_name="...",
    source_type="...",
    # ... other params
)
```

### ❌ Wrong: Not awaiting async
```python
result = graph.compile().ainvoke(state)  # Wrong - missing await
```

### ✅ Right: Awaiting async
```python
result = await graph.compile().ainvoke(state)  # Correct
```

---

## 🧪 Testing

### Run All Tests
```bash
python test_integration.py
```

### Check Specific Component
```bash
python -m py_compile orchestration/state_model.py
python -m py_compile agents/metadata_agent.py
```

### Manual Test
```python
import asyncio
from orchestration import create_agent_state
from agents.metadata_agent import metadata_agent

async def test():
    state = create_agent_state(
        job_id="test",
        job_name="Test",
        source_type="parquet"
    )
    result = await metadata_agent(state)
    print(result["schema_info"])

asyncio.run(test())
```

---

## 📊 State Fields Reference

```python
# Required in factory
job_id: str              # Unique identifier
job_name: str            # Human-readable name
source_type: str         # "delta", "parquet", "csv", etc.

# Optional (have defaults)
table_name: Optional[str]              # Default: "unknown"
schema_info: Dict[str, Any]            # Default: {}
partition_count: int                   # Default: 0
partition_strategy: Optional[str]      # Default: None
skewed_columns: List[str]              # Default: []
execution_time_ms: int                 # Default: 0
cpu_utilization: float                 # Default: 0.0
memory_used_mb: int                    # Default: 0

# Auto-populated (reducers)
recommendations: Annotated[List[str], operator.add]           # Auto-concat
issues_detected: Annotated[List[Dict], operator.add]          # Auto-concat

# Auto-generated
created_at: str          # ISO timestamp
updated_at: str          # ISO timestamp
```

---

## 🔗 Import Reference

```python
# State and factory
from orchestration import AgentState, create_agent_state

# Graph
from orchestration import SparkIntelligenceGraph, build_spark_optimization_graph

# Agents (example - all follow same pattern)
from agents.metadata_agent import MetadataAgent, metadata_agent
from agents.partition_agent import PartitionAgent, partition_agent
from agents.runtime_agent import RuntimeAgent, runtime_agent
from agents.skew_agent import SkewAgent, skew_agent
from agents.delta_agent import DeltaAgent, delta_agent
from agents.cost_agent import CostAgent, cost_agent
```

---

## 🚦 Execution Flow

```
1. Request arrives at /api/v1/analyze/job
        ↓
2. Parse request (JobAnalysisRequest)
        ↓
3. Create state: create_agent_state(...)
        ↓
4. Build agents: {name: AgentClass(), ...}
        ↓
5. Build graph: build_spark_optimization_graph(agents)
        ↓
6. Compile: graph.compile()
        ↓
7. Execute: await compiled_graph.ainvoke(initial_state)
        ↓
8. Agents execute sequentially:
   - metadata_agent modifies state
   - partition_agent adds to state
   - runtime_agent adds to state
   - skew_agent adds to state
   - delta_agent adds to state
   - cost_agent adds to state
        ↓
9. Final state returned with:
   - All recommendations concatenated
   - All issues concatenated
   - All analysis fields populated
        ↓
10. Return JobAnalysisResponse with results
```

---

## 🐛 Debugging

### Enable Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect State
```python
# In agent function
logger.debug(f"State keys: {state.keys()}")
logger.debug(f"Recommendations: {state['recommendations']}")
logger.debug(f"Issues: {state['issues_detected']}")
```

### Check Graph
```python
graph = build_spark_optimization_graph(agents)
diagram = graph.visualize()
print(diagram)
```

### Test Individual Agent
```python
async def test_agent():
    state = create_agent_state(
        job_id="test",
        job_name="Test",
        source_type="delta",
        partition_count=100
    )
    result = await partition_agent(state)
    print(f"Strategy: {result.get('partition_strategy')}")
    print(f"Recommendations: {result['recommendations']}")

asyncio.run(test_agent())
```

---

## 📈 Performance Tips

1. **Reuse compiled graphs**: Compile once, invoke multiple times
2. **Use factory for state**: Don't manually create TypedDict
3. **Leverage reducers**: Use list operations, don't manage manually
4. **Async all the way**: Use `await` and `async def`

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| ImportError: cannot import AgentState | Run `pip install -r requirements.txt` |
| TypeError: missing required argument | Check factory function signature |
| AttributeError: 'dict' has no attribute 'job_id' | Use `state["job_id"]` not `state.job_id` |
| RuntimeError: Event loop | Use `asyncio.run()` or within async context |
| TypeError: create_agent_state() missing | Provide `job_id`, `job_name`, `source_type` |

---

## 📞 Quick Links

- **Integration Test**: `python test_integration.py`
- **Full Guide**: Open `LANGGRAPH_GUIDE.md`
- **API Endpoint**: `POST /api/v1/analyze/job`
- **Example Request**: See `LANGGRAPH_GUIDE.md` → "Usage Example"
- **Agent Code**: See `agents/*.py`
- **Graph Code**: See `orchestration/graph_builder.py`

---

## ✅ Checklist

Before deploying:
- [ ] Run `python test_integration.py` ✅
- [ ] Verify requirements.txt includes langgraph ✅
- [ ] Test API endpoint locally ✅
- [ ] Review LANGGRAPH_GUIDE.md ✅
- [ ] Check error handling in agents ✅
- [ ] Verify state creation in API routes ✅
- [ ] Test with sample data ✅

---

**Last Updated**: Current Session
**Status**: Ready for Production
**Questions?**: See documentation files in project root
