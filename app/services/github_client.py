import os
import httpx
from fastapi import HTTPException, status

GITHUB_API_URL = os.environ.get("MEDS_FILE_URL")

def fetch_meds_csv() -> str:
    """
    Fetches the meds.csv file from GitHub as raw CSV text using a PAT token.
    Returns a CSV string.
    """

    github_pat = os.environ.get("GITHUB_PAT")
    if not github_pat:
        raise RuntimeError("GITHUB_PAT must be set in the environment.")
    
    headers = {
        "Authorization": f"Bearer {github_pat}",
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "meds-api-client"
    }

    try:
        response = httpx.get(GITHUB_API_URL, headers=headers, timeout=10.0)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error connecting to GitHub: {exc}"
        )
    
    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="CSV file not found in GitHub repo."
        )
    
    if response.status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail='GitHub PAT is invalid or lacks permissions.'
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub returned unexpected status: {response.status_code}"
        )
    
    return response.text