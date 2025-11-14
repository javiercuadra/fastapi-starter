import os
import httpx
from fastapi import HTTPException, status

GITHUB_API_URL = os.environ.get("MEDS_FILE_URL")

# Create a persistent HTTP client for connection reuse
_http_client = None

def validate_github_config():
    """
    Validates that required GitHub configuration environment variables are set.
    Should be called at application startup to fail fast.
    Raises RuntimeError if configuration is invalid.
    """
    if not GITHUB_API_URL:
        raise RuntimeError("MEDS_FILE_URL must be set in the environment.")
    
    github_pat = os.environ.get("GITHUB_PAT")
    if not github_pat:
        raise RuntimeError("GITHUB_PAT must be set in the environment.")

def get_http_client() -> httpx.Client:
    """
    Returns a persistent HTTP client instance for connection reuse.
    Creates the client on first call.
    """
    global _http_client
    if _http_client is None:
        _http_client = httpx.Client(timeout=10.0)
    return _http_client

def fetch_meds_csv() -> str:
    """
    Fetches the meds.csv file from GitHub as raw CSV text using a PAT token.
    Returns a CSV string.
    """

    github_pat = os.environ.get("GITHUB_PAT")
    # This is validated at startup by validate_github_config()
    
    headers = {
        "Authorization": f"token {github_pat}",
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "meds-api-client"
    }

    try:
        client = get_http_client()
        response = client.get(GITHUB_API_URL, headers=headers)
    except Exception:
        # Log the full exception internally but don't expose details to client
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error connecting to GitHub."
        )
    
    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CSV file not found in GitHub repo."
        )
    
    if response.status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='GitHub PAT is invalid or lacks permissions.'
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub returned unexpected status: {response.status_code}"
        )
    
    return response.text