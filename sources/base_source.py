"""Base class for data sources"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSource(ABC):
    """Abstract base class for data sources"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize source with configuration
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the source"""
        pass
    
    @abstractmethod
    async def get_metadata(self, table_name: str) -> Dict[str, Any]:
        """Get table metadata"""
        pass
    
    @abstractmethod
    async def read_data(self, table_name: str, limit: int = 1000) -> list:
        """Read data from source"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Close connection to the source"""
        pass
