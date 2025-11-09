from fastapi import FastAPI

app = FastAPI()

@app.get("/greet")
def greet(name: str = "stranger"):
    return {"message": f"Hello, {name}!"}