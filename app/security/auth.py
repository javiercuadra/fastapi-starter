import os
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verifies incoming Basic Auth credentials against environment variables.
    Returns True if valid; raises HTTP 401 if invalid.
    """

    # Load expected username/password from environment
    expected_username = os.environ.get("MEDS_API_USERNAME")
    expected_password = os.environ.get("MEDS_API_PASSWORD")

    # Ensure both are set
    if not expected_username or not expected_password:
        raise RuntimeError(
            "MEDS_API_USERNAME and MEDS_API_PASSWORD must be set in environment variables."
        )
    
    # Constant-time comparison to prevent timing attack
    username_match = secrets.compare_digest(credentials.username, expected_username)
    password_match = secrets.compare_digest(credentials.password, expected_password)

    if not (username_match and password_match):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Basic"}
        )

    return True 