"""Reasoning agent for RAG-based decision making"""

import logging
from typing import Dict, Any, List
from rag.retriever import Retriever

logger = logging.getLogger(__name__)

class ReasoningAgent:
    """Uses RAG to reason about Spark optimizations"""
    
    def __init__(self, retriever: Retriever):
        """
        Initialize reasoning agent
        
        Args:
            retriever: Retriever instance for document retrieval
        """
        self.retriever = retriever
    
    async def reason(self, state: Dict[str, Any]) -> List[str]:
        """
        Reason about optimizations using RAG
        
        Args:
            state: Job state
            
        Returns:
            List of recommendations
        """
        logger.info("ReasoningAgent: Starting RAG-based reasoning")
        
        recommendations = []
        
        try:
            # Retrieve relevant documents
            query = f"Optimize Spark job with {state.get('job_name')} metrics {state}"
            relevant_docs = await self.retriever.retrieve(query, top_k=3)
            
            # Generate recommendations based on retrieved context
            if relevant_docs:
                for doc in relevant_docs:
                    recommendations.append(f"Based on documentation: {doc.get('title')}")
            
            logger.info(f"ReasoningAgent: Generated {len(recommendations)} recommendations")
            
        except Exception as e:
            logger.error(f"ReasoningAgent: Error during reasoning: {str(e)}")
        
        return recommendations
