"""Dependency injection for FastAPI endpoints"""

from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_settings():
    """Dependency to inject application settings"""
    return settings

async def get_logger():
    """Dependency to inject logger"""
    return logger
