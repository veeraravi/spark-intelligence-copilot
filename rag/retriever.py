"""Retriever for RAG pipeline"""

import logging
from typing import List, Dict, Any
from rag.vectorstore import VectorStore

logger = logging.getLogger(__name__)

class Retriever:
    """Retrieves relevant documents for RAG"""
    
    def __init__(self, vectorstore: VectorStore):
        """
        Initialize retriever
        
        Args:
            vectorstore: VectorStore instance
        """
        self.vectorstore = vectorstore
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        logger.info(f"Retrieving documents for: {query}")
        
        try:
            results = await self.vectorstore.search(query, top_k)
            logger.info(f"Retrieved {len(results)} documents")
            return results
        except Exception as e:
            logger.error(f"Retrieval failed: {str(e)}")
            return []
