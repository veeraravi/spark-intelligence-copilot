"""Rules for partition optimization"""

import logging

logger = logging.getLogger(__name__)

class PartitionRules:
    """Rules for partition optimization"""
    
    @staticmethod
    def check_optimal_partition_count(partition_count: int, row_count: int) -> tuple:
        """
        Check if partition count is optimal
        
        Args:
            partition_count: Current partition count
            row_count: Total number of rows
            
        Returns:
            Tuple of (is_optimal, recommendation)
        """
        recommended = max(1, row_count // 1000000)
        
        if abs(partition_count - recommended) / recommended > 0.2:
            return False, f"Optimal partition count is {recommended}"
        
        return True, "Partition count is optimal"
    
    @staticmethod
    def check_partition_strategy(table_name: str, schema_info: dict) -> list:
        """
        Check partition strategy
        
        Args:
            table_name: Table name
            schema_info: Schema information
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if "date" in str(schema_info):
            recommendations.append("Consider date-based partitioning")
        
        if "region" in str(schema_info):
            recommendations.append("Consider geographic partitioning")
        
        return recommendations
