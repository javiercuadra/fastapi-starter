from fastapi import APIRouter, Depends
from app.security.auth import verify_credentials
from app.services.github_client import fetch_meds_csv
from app.services.csv_parser import parse_meds_csv

router = APIRouter()

@router.get("/meds")
def get_meds(_: bool = Depends(verify_credentials)):
    """
    Protected endpoint that fetches, parses, and returns the medication list
    from the private GitHub repository.
    """

    # Fetch raw CSV text from GitHub
    csv_text = fetch_meds_csv()

    # Convert CSV into list of dictionaries
    meds_data = parse_meds_csv(csv_text)

    return {
        "count": len(meds_data),
        "items": meds_data
    }