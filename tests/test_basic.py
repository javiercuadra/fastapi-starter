"""
Basic tests for the FastAPI application endpoints.

This module tests the main API endpoints including root, greet, health, and math operations.
"""

def test_root(client):
    """Test the root endpoint returns welcome message and available resources."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()

    assert "resources" in data
    assert "greet" in data["resources"]
    assert "math" in data["resources"]
    assert "meds" in data["resources"]

def test_greet_get_empty(client):
    """Test GET /greet without name parameter returns default greeting."""
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, stranger!"}

def test_greet_get_query_param(client):
    """Test GET /greet with name query parameter returns personalized greeting."""
    response = client.get("/greet?name=Javi")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Javi!"}

def test_greet_post(client):
    """Test POST /greet with name in request body returns personalized greeting."""
    payload = {"name": "Javier"}
    response = client.post("/greet", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Javier!"}

def test_health(client):
    """Test the health check endpoint returns ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_math_index(client):
    """Test GET /math returns list of available math operations."""
    response = client.get("/math")
    assert response.status_code == 200
    data = response.json()
    assert "resource" in data
    assert data["resource"] == "math"
    assert "operations" in data
    assert len(data["operations"]) == 2

def test_math_add(client):
    """Test POST /math/add sums a list of numbers correctly."""
    payload = {"numbers": [1, 2, 3, 4]}
    response = client.post("/math/add", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 10}

def test_math_multiply(client):
    """Test POST /math/multiply multiplies a list of numbers correctly."""
    payload = {"numbers": [1, 2, 3, 4]}
    response = client.post("/math/multiply", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 24}

def test_math_add_empty_list(client):
    """Test POST /math/add with empty list returns 0."""
    payload = {"numbers": []}
    response = client.post("/math/add", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 0}

def test_math_multiply_empty_list(client):
    """Test POST /math/multiply with empty list returns 0."""
    payload = {"numbers": []}
    response = client.post("/math/multiply", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 0}

def test_math_add_single_number(client):
    """Test POST /math/add with single number returns that number."""
    payload = {"numbers": [42]}
    response = client.post("/math/add", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 42}

def test_math_multiply_single_number(client):
    """Test POST /math/multiply with single number returns that number."""
    payload = {"numbers": [42]}
    response = client.post("/math/multiply", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 42}

def test_math_add_negative_numbers(client):
    """Test POST /math/add correctly handles negative numbers."""
    payload = {"numbers": [10, -5, -3, 8]}
    response = client.post("/math/add", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 10}

def test_math_multiply_negative_numbers(client):
    """Test POST /math/multiply correctly handles negative numbers."""
    payload = {"numbers": [2, -3, 4]}
    response = client.post("/math/multiply", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": -24}

def test_math_add_floats(client):
    """Test POST /math/add correctly handles floating point numbers."""
    payload = {"numbers": [1.5, 2.5, 3.0]}
    response = client.post("/math/add", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 7.0}

def test_math_multiply_floats(client):
    """Test POST /math/multiply correctly handles floating point numbers."""
    payload = {"numbers": [2.0, 3.5, 2.0]}
    response = client.post("/math/multiply", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": 14.0}

def test_greet_get_special_characters(client):
    """Test GET /greet handles names with special characters."""
    response = client.get("/greet?name=José-María")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, José-María!"}

def test_greet_post_special_characters(client):
    """Test POST /greet handles names with special characters."""
    payload = {"name": "María-José"}
    response = client.post("/greet", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, María-José!"}