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

### 3) Configure environment variables

Create a `.env` file in the root directory with the following variables:

```bash
# Required for /meds endpoint
MEDS_API_USERNAME=your_username
MEDS_API_PASSWORD=your_password
GITHUB_PAT=your_github_personal_access_token
MEDS_FILE_URL=https://api.github.com/repos/owner/repo/contents/path/to/meds.csv
```

**Note:** The `/meds` endpoint requires these environment variables to be set for authentication and GitHub API access.

### 4) Start the server

```bash
uvicorn app.main:app --reload
```

This will start the server at: `http://127.0.0.1:8000`

## Using the server

The following endpoints are available:

| Endpoint | Method | Description | Path | Payload | Auth |
|----------|--------|-------------|---------|---------|------|
| `/` | GET | Landing route that provides usage instructions | http://127.0.0.1:8000/ | None | None |
| `/greet` | GET | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet?name=Javi | None | None |
| `/greet` | POST | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet | {"name":"Javi"} | None |
| `/math` | GET | Lists available math operations | http://127.0.0.1:8000/math | None | None |
| `/math/add` | POST | Sum a list of numbers | http://127.0.0.1:8000/math | {"numbers": [1,2,3]} | None |
| `/math/multiply` | POST | Multiply a list of numbers | http://127.0.0.1:8000/math | {"numbers": [1,2,3]} | None |
| `/health` | GET | Basic status check endpoint | http://127.0.0.1:8000/health | None | None |
| `/meds` | GET | Fetches medication data from a private GitHub repository as JSON | http://127.0.0.1:8000/meds | None | HTTP Basic Auth |

## Testing

This project uses `pytest` for testing with comprehensive test coverage.

### Running Tests

To run all tests:

```bash
pytest
```

To run tests with verbose output:

```bash
pytest -v
```

To run tests with code coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

To run tests with HTML coverage report:

```bash
pytest --cov=app --cov-report=html
```

This will generate a `htmlcov` directory with detailed coverage reports.

### Test Coverage

The test suite includes:
- Tests for all API endpoints (root, greet, health, math operations, meds)
- Authentication testing (valid/invalid credentials, missing auth)
- External API integration testing (GitHub API responses)
- CSV parsing and edge cases
- Edge case testing (empty lists, single values, negative numbers, floats)
- Special character handling in string inputs
- Comprehensive validation of response formats and status codes

Current test coverage: **100%** of application code
