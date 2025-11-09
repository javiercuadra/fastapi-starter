from fastapi import FastAPI

app = FastAPI()

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