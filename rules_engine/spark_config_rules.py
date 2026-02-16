"""Rules for Spark configuration optimization"""

import logging

logger = logging.getLogger(__name__)

class SparkConfigRules:
    """Rules for optimizing Spark configurations"""
    
    @staticmethod
    def check_executor_memory(data_size_gb: float) -> dict:
        """
        Check recommended executor memory
        
        Args:
            data_size_gb: Data size in GB
            
        Returns:
            Configuration recommendations
        """
        if data_size_gb < 10:
            return {"executor_memory": "4g", "executor_cores": 4}
        elif data_size_gb < 100:
            return {"executor_memory": "16g", "executor_cores": 8}
        else:
            return {"executor_memory": "32g", "executor_cores": 16}
    
    @staticmethod
    def check_shuffle_partitions(row_count: int) -> int:
        """
        Check recommended shuffle partitions
        
        Args:
            row_count: Total number of rows
            
        Returns:
            Recommended shuffle partitions
        """
        return max(100, min(10000, row_count // 100000))
    
    @staticmethod
    def check_broadcast_threshold(table_size_mb: int) -> dict:
        """
        Check broadcast join threshold
        
        Args:
            table_size_mb: Table size in MB
            
        Returns:
            Broadcasting recommendations
        """
        return {
            "broadcast_threshold": f"{min(table_size_mb, 500)}mb",
            "should_broadcast": table_size_mb < 500
        }
