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
uvicorn main:app --reload
```

This will start the server at: `http://127.0.0.1:8000`

## Using the server

The following endpoints are available:

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Landing route that provides usage instructions | http://127.0.0.1:8000/ |
| `/greet?name=YourName` | GET | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet?name=Javi |
| `/health` | GET | Basic status check endpoint | http://127.0.0.1:8000/health |
