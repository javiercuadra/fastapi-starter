"""
Tests for the /meds endpoint.

This module tests the medications endpoint including authentication,
GitHub API integration, and CSV parsing.
"""
import os
from unittest.mock import patch, MagicMock
import pytest


def test_meds_no_auth(client):
    """Test /meds endpoint without authentication returns 401."""
    response = client.get("/meds")
    assert response.status_code == 401


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass"
})
def test_meds_invalid_credentials(client):
    """Test /meds endpoint with invalid credentials returns 401."""
    response = client.get("/meds", auth=("wrong_user", "wrong_pass"))
    assert response.status_code == 401


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass",
    "GITHUB_PAT": "test_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.httpx.get")
def test_meds_successful_retrieval(mock_get, client):
    """Test /meds endpoint with valid credentials and successful GitHub response."""
    # Mock the GitHub API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "name,dosage,frequency\nAspirin,100mg,daily\nIbuprofen,200mg,as needed"
    mock_get.return_value = mock_response
    
    response = client.get("/meds", auth=("test_user", "test_pass"))
    
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert data["count"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "Aspirin"
    assert data["items"][1]["name"] == "Ibuprofen"


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass",
    "GITHUB_PAT": "test_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.httpx.get")
def test_meds_github_404(mock_get, client):
    """Test /meds endpoint when GitHub returns 404."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    response = client.get("/meds", auth=("test_user", "test_pass"))
    
    assert response.status_code == 502
    assert "not found" in response.json()["detail"].lower()


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass",
    "GITHUB_PAT": "test_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.httpx.get")
def test_meds_github_401(mock_get, client):
    """Test /meds endpoint when GitHub returns 401 (invalid token)."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response
    
    response = client.get("/meds", auth=("test_user", "test_pass"))
    
    assert response.status_code == 502
    assert "invalid" in response.json()["detail"].lower() or "permissions" in response.json()["detail"].lower()


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass",
    "GITHUB_PAT": "test_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.httpx.get")
def test_meds_github_connection_error(mock_get, client):
    """Test /meds endpoint when connection to GitHub fails."""
    mock_get.side_effect = Exception("Connection timeout")
    
    response = client.get("/meds", auth=("test_user", "test_pass"))
    
    assert response.status_code == 502
    assert "error" in response.json()["detail"].lower()


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass",
    "GITHUB_PAT": "test_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.httpx.get")
def test_meds_empty_csv(mock_get, client):
    """Test /meds endpoint with empty CSV data."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "name,dosage,frequency\n"
    mock_get.return_value = mock_response
    
    response = client.get("/meds", auth=("test_user", "test_pass"))
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert len(data["items"]) == 0


@patch.dict(os.environ, {
    "MEDS_API_USERNAME": "test_user",
    "MEDS_API_PASSWORD": "test_pass",
    "GITHUB_PAT": "test_token",
    "MEDS_FILE_URL": "https://api.github.com/repos/test/test/contents/meds.csv"
})
@patch("app.services.github_client.httpx.get")
def test_meds_single_medication(mock_get, client):
    """Test /meds endpoint with a single medication."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "name,dosage,frequency\nAspirin,100mg,daily"
    mock_get.return_value = mock_response
    
    response = client.get("/meds", auth=("test_user", "test_pass"))
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Aspirin"
    assert data["items"][0]["dosage"] == "100mg"
    assert data["items"][0]["frequency"] == "daily"
