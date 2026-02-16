"""Repository for metrics persistence"""

import logging
from typing import Dict, Any, List
from storage.db_connection import DBConnection

logger = logging.getLogger(__name__)

class MetricsRepository:
    """Manages metrics storage and retrieval"""
    
    def __init__(self, db_connection: DBConnection):
        """
        Initialize metrics repository
        
        Args:
            db_connection: Database connection
        """
        self.db = db_connection
    
    async def save_metrics(self, job_id: str, metrics: Dict[str, Any]) -> bool:
        """
        Save job metrics
        
        Args:
            job_id: Job ID
            metrics: Metrics dictionary
            
        Returns:
            Success status
        """
        logger.info(f"Saving metrics for job {job_id}")
        
        try:
            query = f"INSERT INTO metrics VALUES ('{job_id}', {metrics})"
            await self.db.execute_query(query)
            return True
        except Exception as e:
            logger.error(f"Failed to save metrics: {str(e)}")
            return False
    
    async def get_metrics(self, job_id: str) -> List[Dict[str, Any]]:
        """
        Get metrics for a job
        
        Args:
            job_id: Job ID
            
        Returns:
            List of metrics
        """
        logger.info(f"Fetching metrics for job {job_id}")
        
        try:
            query = f"SELECT * FROM metrics WHERE job_id = '{job_id}'"
            results = await self.db.execute_query(query)
            return results
        except Exception as e:
            logger.error(f"Failed to get metrics: {str(e)}")
            return []
