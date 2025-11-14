"""
Pytest configuration and fixtures for the test suite.

This module sets up the Python path and provides reusable test fixtures.
"""
import os
import sys

import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path for imports
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)

from app.main import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for testing the FastAPI application.
    
    Returns:
        TestClient: A test client for making requests to the app.
    """
    return TestClient(app)