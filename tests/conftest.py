"""conftest.py - Pytest configuration and fixtures"""

import pytest
import asyncio
from pathlib import Path


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_data_dir():
    """Return path to test data directory"""
    return Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset imported modules between tests"""
    import sys
    
    modules_to_reset = [m for m in sys.modules if m.startswith("app") or m.startswith("agents")]
    
    yield
    
    for module in modules_to_reset:
        if module in sys.modules:
            del sys.modules[module]
