"""Graph builder using LangGraph for orchestrating agent workflows"""

from typing import Callable, Dict, List, Optional
from langgraph.graph import StateGraph, END
import logging
from orchestration.state_model import AgentState

logger = logging.getLogger(__name__)


class SparkIntelligenceGraph:
    """
    LangGraph-based workflow orchestrator for Spark Intelligence agents.
    
    This class builds and manages a directed graph of agents that analyze
    and optimize Spark jobs through a coordinated workflow.
    """
    
    def __init__(self):
        """Initialize the graph builder"""
        self.graph = StateGraph(AgentState)
        self.start_node: Optional[str] = None
        self.end_node: str = END
        self.compiled_graph = None
        logger.info("Initialized SparkIntelligenceGraph")
    
    def add_node(self, name: str, func: Callable) -> "SparkIntelligenceGraph":
        """
        Add a node (agent) to the graph.
        
        Args:
            name: Node identifier
            func: Async function that processes the state
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Adding node: {name}")
        self.graph.add_node(name, func)
        return self
    
    def add_edge(self, source: str, target: str) -> "SparkIntelligenceGraph":
        """
        Add an edge between two nodes.
        
        Args:
            source: Source node name
            target: Target node name
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Adding edge: {source} -> {target}")
        self.graph.add_edge(source, target)
        return self
    
    def add_conditional_edge(
        self,
        source: str,
        condition_func: Callable,
        edges: Dict[str, str]
    ) -> "SparkIntelligenceGraph":
        """
        Add a conditional edge that routes based on state.
        
        Args:
            source: Source node name
            condition_func: Function that determines routing
            edges: Mapping of condition results to target nodes
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Adding conditional edge from: {source}")
        self.graph.add_conditional_edges(source, condition_func, edges)
        return self
    
    def set_entry_point(self, node: str) -> "SparkIntelligenceGraph":
        """
        Set the entry point of the graph.
        
        Args:
            node: Node name to start from
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Setting entry point: {node}")
        self.start_node = node
        self.graph.set_entry_point(node)
        return self
    
    def set_finish_point(self, node: str) -> "SparkIntelligenceGraph":
        """
        Set the finish point of the graph.
        
        Args:
            node: Node name that ends execution
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Setting finish point: {node}")
        self.graph.set_finish_point(node)
        return self
    
    def compile(self):
        """
        Compile the graph for execution.
        
        Returns:
            Compiled graph
        """
        if not self.start_node:
            raise ValueError("Entry point must be set before compiling")
        
        logger.info("Compiling graph")
        self.compiled_graph = self.graph.compile()
        return self.compiled_graph
    
    async def run(self, initial_state: AgentState) -> AgentState:
        """
        Execute the workflow with the given initial state.
        
        Args:
            initial_state: Initial agent state
            
        Returns:
            Final state after all agents have run
        """
        if not self.compiled_graph:
            self.compile()
        
        logger.info(f"Starting workflow for job: {initial_state['job_id']}")
        
        try:
            # Run the workflow
            final_state = await self.compiled_graph.ainvoke(initial_state)
            
            logger.info(f"Workflow completed for job: {initial_state['job_id']}")
            return final_state
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            raise
    
    def visualize(self) -> str:
        """
        Generate a visual representation of the graph.
        
        Returns:
            ASCII art representation of the graph
        """
        if not self.compiled_graph:
            self.compile()
        
        try:
            return self.compiled_graph.get_graph().draw_ascii()
        except Exception as e:
            logger.warning(f"Could not visualize graph: {str(e)}")
            return "Graph visualization not available"


def build_spark_optimization_graph(agents: Dict[str, Callable]) -> SparkIntelligenceGraph:
    """
    Factory function to build the standard Spark optimization workflow.
    
    Args:
        agents: Dictionary mapping agent names to agent functions
        
    Returns:
        Configured and compiled SparkIntelligenceGraph
    """
    graph = SparkIntelligenceGraph()
    
    # Add all agent nodes
    for agent_name, agent_func in agents.items():
        graph.add_node(agent_name, agent_func)
    
    # Set execution order
    graph.set_entry_point("metadata_agent")
    graph.add_edge("metadata_agent", "partition_agent")
    graph.add_edge("partition_agent", "skew_agent")
    graph.add_edge("skew_agent", "runtime_agent")
    graph.add_edge("runtime_agent", "delta_agent")
    graph.add_edge("delta_agent", "cost_agent")
    graph.set_finish_point("cost_agent")
    
    logger.info("Built standard Spark optimization graph")
    return graph
