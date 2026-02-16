"""Rules for handling data skew"""

import logging

logger = logging.getLogger(__name__)

class SkewRules:
    """Rules for detecting and handling data skew"""
    
    @staticmethod
    def detect_skew(partition_sizes: list) -> float:
        """
        Detect data skew ratio
        
        Args:
            partition_sizes: List of partition sizes
            
        Returns:
            Skew ratio (0-1)
        """
        if not partition_sizes:
            return 0.0
        
        avg_size = sum(partition_sizes) / len(partition_sizes)
        max_size = max(partition_sizes)
        
        return (max_size - avg_size) / max_size if max_size > 0 else 0.0
    
    @staticmethod
    def get_skew_mitigation_strategies(skew_ratio: float) -> list:
        """
        Get strategies to mitigate skew
        
        Args:
            skew_ratio: Skew ratio
            
        Returns:
            List of mitigation strategies
        """
        strategies = []
        
        if skew_ratio < 0.2:
            return ["No significant skew detected"]
        elif skew_ratio < 0.5:
            strategies = [
                "Use salting for join operations",
                "Consider pre-filtering data"
            ]
        else:
            strategies = [
                "Repartition data with even distribution",
                "Use two-stage join strategy",
                "Consider adaptive partitioning"
            ]
        
        return strategies
