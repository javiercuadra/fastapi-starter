from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()

    assert "resources" in data
    assert "greet" in data["resources"]
    assert "math" in data["resources"]

def test_greet_get_empty():
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, stranger!"}

def test_greet_get_query_param():
    response = client.get("/greet?name=Javi")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Javi!"}

def test_greet_post():
    payload = {"name": "Javier"}
    response = client.post("/greet", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Javier!"}

def test_math_add():
    payload = {"numbers": [1,2,3,4]}
    response = client.post("/math/add", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 10}

def test_math_multiply():
    payload = {"numbers": [1,2,3,4]}
    response = client.post("/math/multiply", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 24}