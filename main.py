from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GreetRequest(BaseModel):
    name: str

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