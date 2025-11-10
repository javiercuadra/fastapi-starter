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

@app.post("/math/sum")
def sum_numbers(request: MathRequest):
    total = sum(request.numbers)
    return {"result": total}

@app.post("/math/multiply")
def multiply_numbers(request: MathRequest):
    total = 1
    for n in request.numbers:
        total *= n

    return {"result": total if request.numbers else 0}