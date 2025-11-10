from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Welcome! Try /greet?name=YourName to get a personalized greeting."
    }
