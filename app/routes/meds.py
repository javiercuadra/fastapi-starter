import time
from functools import lru_cache
from typing import Dict, List
from fastapi import APIRouter, Depends
from app.security.auth import verify_credentials
from app.services.github_client import fetch_meds_csv
from app.services.csv_parser import parse_meds_csv

router = APIRouter()

# Cache configuration
CACHE_TTL_SECONDS = 300  # 5 minutes
_cache_timestamp = 0
_cached_data = None

def get_cached_meds() -> List[Dict[str, str]]:
    """
    Fetches and parses medication data with caching.
    Cache expires after CACHE_TTL_SECONDS.
    
    Returns:
        List of medication dictionaries
    """
    global _cache_timestamp, _cached_data
    
    current_time = time.time()
    
    # Check if cache is valid
    if _cached_data is not None and (current_time - _cache_timestamp) < CACHE_TTL_SECONDS:
        return _cached_data
    
    # Cache miss or expired - fetch fresh data
    csv_text = fetch_meds_csv()
    
    try:
        meds_data = parse_meds_csv(csv_text)
    except ValueError as e:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing CSV data: {str(e)}"
        )
    
    # Update cache
    _cached_data = meds_data
    _cache_timestamp = current_time
    
    return meds_data

@router.get("/meds")
def get_meds(_: bool = Depends(verify_credentials)):
    """
    Protected endpoint that fetches, parses, and returns the medication list
    from the private GitHub repository.
    
    Data is cached for 5 minutes to reduce GitHub API calls and improve performance.
    """

    # Get cached or fresh data
    meds_data = get_cached_meds()

    return {
        "count": len(meds_data),
        "items": meds_data
    }