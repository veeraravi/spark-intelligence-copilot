"""Factory for creating appropriate data source connectors"""

import logging
from typing import Dict, Any
from sources.jdbc_source import JDBCSource
from sources.file_source import FileSource
from sources.api_source import APISource
from sources.kafka_source import KafkaSource

logger = logging.getLogger(__name__)

class SourceFactory:
    """Factory for creating data source instances"""
    
    _sources = {
        "jdbc": JDBCSource,
        "file": FileSource,
        "api": APISource,
        "kafka": KafkaSource,
    }
    
    @classmethod
    def create(cls, source_type: str, config: Dict[str, Any]):
        """
        Create a data source instance
        
        Args:
            source_type: Type of source (jdbc, file, api, kafka)
            config: Configuration for the source
            
        Returns:
            Configured source instance
        """
        source_class = cls._sources.get(source_type.lower())
        if not source_class:
            raise ValueError(f"Unknown source type: {source_type}")
        
        logger.info(f"Creating {source_type} source")
        return source_class(config)
    
    @classmethod
    def register(cls, source_type: str, source_class):
        """Register a new source type"""
        cls._sources[source_type.lower()] = source_class
        logger.info(f"Registered source type: {source_type}")
