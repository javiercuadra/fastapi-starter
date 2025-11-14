"""
Pytest configuration and fixtures for the test suite.

This module sets up the Python path and provides reusable test fixtures.
"""
import os
import sys

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add the project root to the Python path for imports
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for testing the FastAPI application.
    
    Returns:
        TestClient: A test client for making requests to the app.
    """
    # Set minimal required environment variables for app startup
    # Individual tests can override these with @patch.dict
    with patch.dict(os.environ, {
        "MEDS_API_USERNAME": "test",
        "MEDS_API_PASSWORD": "test",
        "GITHUB_PAT": "test_token",
        "MEDS_FILE_URL": "https://api.github.com/test"
    }, clear=False):
        from app.main import app
        
        # Clear the meds cache before each test
        from app.routes import meds
        meds._cached_data = None
        meds._cache_timestamp = 0
        
        return TestClient(app)