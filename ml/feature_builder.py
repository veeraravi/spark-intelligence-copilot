"""Feature engineering for ML models"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FeatureBuilder:
    """Builds features for ML models"""
    
    @staticmethod
    def build_features(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build ML features from job state
        
        Args:
            state: Job state
            
        Returns:
            Feature dictionary
        """
        logger.info("Building ML features")
        
        features = {
            "partition_count": state.get("partition_count", 0),
            "data_size_mb": state.get("memory_used_mb", 0),
            "cpu_cores": 8,
            "executor_memory_gb": 16,
            "source_type": state.get("source_type", "unknown"),
            "schema_complexity": len(state.get("schema_info", {}).get("columns", [])),
            "previous_runtime_ms": 5000
        }
        
        return features
    
    @staticmethod
    def normalize_features(features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize features for model input
        
        Args:
            features: Raw features
            
        Returns:
            Normalized features
        """
        logger.info("Normalizing features")
        
        normalized = {}
        for key, value in features.items():
            if isinstance(value, (int, float)):
                normalized[key] = (value - 100) / (1000 + 1)
            else:
                normalized[key] = value
        
        return normalized
