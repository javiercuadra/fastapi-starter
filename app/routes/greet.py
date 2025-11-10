from fastapi import APIRouter

from models.greet_models import GreetRequest

router = APIRouter()

@router.get("/greet")
def greet(name: str = "stranger"):
    return {"message": f"Hello, {name}!"}


@router.post("/greet")
def greet_post(request: GreetRequest):
    return {"message": f"Hello, {request.name}!"}