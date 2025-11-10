# fastapi-starter

## Purpose
This project is meant to give me some opportunity to brush up on my backend development by setting up a quick and simple backend server and an API I can call to ensure it is working properly.

## Setup

### 1) Create and activate virtual environment

(Git Bash)
```bash
python -m venv venv
source venv/Scripts/activate
```

### 2) Install dependencies


If this is the first time setting up:

```bash
pip install fastapi uvicorn
pip freeze > requirements.txt
```

Otherwise, after `requirements.txt` exists: 

```bash
pip install -r requirements.txt
```

### 3) Start the server

```bash
uvicorn app.main:app --reload
```

This will start the server at: `http://127.0.0.1:8000`

## Using the server

The following endpoints are available:

| Endpoint | Method | Description | Path | Payload
|----------|--------|-------------|---------|---------|
| `/` | GET | Landing route that provides usage instructions | http://127.0.0.1:8000/ | None |
| `/greet` | GET | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet?name=Javi | None |
| `/greet` | POST | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet | {"name":"Javi"} |
| `/math` | GET | Lists available math operations | http://127.0.0.1:8000/math | None |
| `/math/add` | POST | Sum a list of numbers | http://127.0.0.1:8000/math | {"numbers": [1,2,3]} |
| `/math/multiply` | POST | Multiply a list of numbers | http://127.0.0.1:8000/math | {"numbers": [1,2,3]} |
| `/health` | GET | Basic status check endpoint | http://127.0.0.1:8000/health |
