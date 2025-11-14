from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Welcome to my API. Refer below to the resources available.",
        "resources": {
            "greet": "/greet",
            "math": "/math",
            "meds": "/meds"
        }
    }
