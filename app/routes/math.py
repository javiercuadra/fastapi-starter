from fastapi import APIRouter

from models.math_models import MathRequest

router = APIRouter()

@router.get("/math")
def math_index():
    return {
        "resource": "math",
        "operations": [
            {
                "method": "POST",
                "path": "/math/add",
                "description": "Returns the sum of a list of numbers."
            },
            {
                "method": "POST",
                "path": "/math/multiply",
                "description": "Returns the product of a list of numbers."
            }
        ]
    }

@router.post("/math/add")
def add_numbers(request: MathRequest):
    total = sum(request.numbers)
    return {"result": total}

@router.post("/math/multiply")
def multiply_numbers(request: MathRequest):
    total = 1
    for n in request.numbers:
        total *= n

    return {"result": total if request.numbers else 0}
