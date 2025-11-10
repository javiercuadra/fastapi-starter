from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GreetRequest(BaseModel):
    name: str

class MathRequest(BaseModel):
    numbers: List[float] = []

@app.get("/")
def root():
    return {
        "message": "Welcome! Try /greet?name=YourName to get a personalized greeting."
    }

@app.get("/greet")
def greet(name: str = "stranger"):
    return {"message": f"Hello, {name}!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/greet")
def greet_post(request: GreetRequest):
    return {"message": f"Hello, {request.name}!"}

@app.get("/math")
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

@app.post("/math/add")
def add_numbers(request: MathRequest):
    total = sum(request.numbers)
    return {"result": total}

@app.post("/math/multiply")
def multiply_numbers(request: MathRequest):
    total = 1
    for n in request.numbers:
        total *= n

    return {"result": total if request.numbers else 0}
