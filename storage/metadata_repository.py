"""Repository for metadata persistence"""

import logging
from typing import Dict, Any, Optional
from storage.db_connection import DBConnection

logger = logging.getLogger(__name__)

class MetadataRepository:
    """Manages metadata storage and retrieval"""
    
    def __init__(self, db_connection: DBConnection):
        """
        Initialize metadata repository
        
        Args:
            db_connection: Database connection
        """
        self.db = db_connection
    
    async def save_metadata(self, metadata: Dict[str, Any]) -> bool:
        """
        Save metadata
        
        Args:
            metadata: Metadata dictionary
            
        Returns:
            Success status
        """
        logger.info(f"Saving metadata for {metadata.get('table_name')}")
        
        try:
            query = f"INSERT INTO metadata VALUES ({metadata})"
            await self.db.execute_query(query)
            return True
        except Exception as e:
            logger.error(f"Failed to save metadata: {str(e)}")
            return False
    
    async def get_metadata(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a table
        
        Args:
            table_name: Table name
            
        Returns:
            Metadata dictionary or None
        """
        logger.info(f"Fetching metadata for {table_name}")
        
        try:
            query = f"SELECT * FROM metadata WHERE table_name = '{table_name}'"
            results = await self.db.execute_query(query)
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to get metadata: {str(e)}")
            return None
