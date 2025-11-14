"""
Tests for the /meds endpoint.

This module tests the medications endpoint including authentication,
CSV parsing, caching behavior, and error handling.
"""
import os
from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException, status


def test_meds_endpoint_requires_auth(client):
    """Test that /meds endpoint requires authentication."""
    response = client.get("/meds")
    assert response.status_code == 401


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
def test_meds_endpoint_with_invalid_credentials(client):
    """Test that /meds endpoint rejects invalid credentials."""
    response = client.get("/meds", auth=("wrong", "credentials"))
    assert response.status_code == 401


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.get_http_client")
def test_meds_endpoint_with_valid_credentials(mock_http_client, client):
    """Test that /meds endpoint returns data with valid credentials."""
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "name,dosage,frequency\nAspirin,100mg,daily\nIbuprofen,200mg,twice daily"
    
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_http_client.return_value = mock_client
    
    response = client.get("/meds", auth=("testuser", "testpass"))
    assert response.status_code == 200
    
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert data["count"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "Aspirin"
    assert data["items"][1]["name"] == "Ibuprofen"


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.get_http_client")
def test_meds_endpoint_github_404(mock_http_client, client):
    """Test that /meds endpoint returns 404 when GitHub file not found."""
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 404
    
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_http_client.return_value = mock_client
    
    response = client.get("/meds", auth=("testuser", "testpass"))
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.get_http_client")
def test_meds_endpoint_github_401(mock_http_client, client):
    """Test that /meds endpoint returns 500 when GitHub auth fails."""
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 401
    
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_http_client.return_value = mock_client
    
    response = client.get("/meds", auth=("testuser", "testpass"))
    assert response.status_code == 500
    assert "PAT" in response.json()["detail"]


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.get_http_client")
def test_meds_endpoint_connection_error(mock_http_client, client):
    """Test that /meds endpoint handles connection errors gracefully."""
    # Mock a connection error
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Connection failed")
    mock_http_client.return_value = mock_client
    
    response = client.get("/meds", auth=("testuser", "testpass"))
    assert response.status_code == 502
    # Should not expose exception details
    assert "Connection failed" not in response.json()["detail"]
    assert "GitHub" in response.json()["detail"]


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.get_http_client")
def test_meds_endpoint_empty_csv(mock_http_client, client):
    """Test that /meds endpoint handles empty CSV data."""
    # Mock the HTTP response with empty CSV
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = ""
    
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_http_client.return_value = mock_client
    
    response = client.get("/meds", auth=("testuser", "testpass"))
    # Should return error due to CSV validation
    assert response.status_code == 500


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "testuser",
    "MEDS_API_PASSWORD": "testpass",
    "GITHUB_PAT": "fake_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.get_http_client")
def test_meds_endpoint_caching(mock_http_client, client):
    """Test that /meds endpoint caches responses."""
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "name,dosage\nAspirin,100mg"
    
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_http_client.return_value = mock_client
    
    # First request
    response1 = client.get("/meds", auth=("testuser", "testpass"))
    assert response1.status_code == 200
    
    # Second request - should use cache
    response2 = client.get("/meds", auth=("testuser", "testpass"))
    assert response2.status_code == 200
    
    # Should only call GitHub API once due to caching
    assert mock_client.get.call_count == 1
    
    # Both responses should be identical
    assert response1.json() == response2.json()
