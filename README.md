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

Create a `.env` file in the project root with the following variables:

```
# Required for /meds endpoint
MEDS_API_USERNAME=your_username
MEDS_API_PASSWORD=your_password
GITHUB_PAT=your_github_personal_access_token
MEDS_FILE_URL=https://api.github.com/repos/owner/repo/contents/path/to/meds.csv
```

**Note:** The `.env` file is gitignored and should never be committed to version control.

### 4) Start the server

```bash
uvicorn app.main:app --reload
```

This will start the server at: `http://127.0.0.1:8000`

## Using the server

The following endpoints are available:

| Endpoint | Method | Description | Path | Payload | Auth Required
|----------|--------|-------------|---------|---------|---------------|
| `/` | GET | Landing route that provides usage instructions | http://127.0.0.1:8000/ | None | No |
| `/greet` | GET | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet?name=Javi | None | No |
| `/greet` | POST | Returns a personalized greeting based on the `name` query parameter | http://127.0.0.1:8000/greet | {"name":"Javi"} | No |
| `/math` | GET | Lists available math operations | http://127.0.0.1:8000/math | None | No |
| `/math/add` | POST | Sum a list of numbers | http://127.0.0.1:8000/math/add | {"numbers": [1,2,3]} | No |
| `/math/multiply` | POST | Multiply a list of numbers | http://127.0.0.1:8000/math/multiply | {"numbers": [1,2,3]} | No |
| `/health` | GET | Basic status check endpoint | http://127.0.0.1:8000/health | None | No |
| `/meds` | GET | Fetches medication data from a private GitHub repository (cached for 5 minutes) | http://127.0.0.1:8000/meds | None | Yes (HTTP Basic Auth) |

### Authentication

The `/meds` endpoint requires HTTP Basic Authentication. Include credentials in your requests:

**Using curl:**
```bash
curl -u username:password http://127.0.0.1:8000/meds
```

**Using Python requests:**
```python
import requests
response = requests.get('http://127.0.0.1:8000/meds', auth=('username', 'password'))
```

### Medications Endpoint Features

The `/meds` endpoint includes several production-ready features:

- **Authentication**: Protected by HTTP Basic Auth using credentials from environment variables
- **Caching**: Responses are cached for 5 minutes to reduce GitHub API calls and improve performance
- **Validation**: CSV data is validated with a configurable row limit (default: 10,000 rows) to prevent memory exhaustion
- **Error Handling**: Proper HTTP status codes and error messages for various failure scenarios
- **Connection Pooling**: Uses persistent HTTP client for better performance
- **Security**: Environment variables are validated at startup for fail-fast behavior

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
- Edge case testing (empty lists, single values, negative numbers, floats)
- Special character handling in string inputs
- Authentication and authorization testing for protected endpoints
- Error handling scenarios (network errors, invalid data, missing resources)
- Caching behavior validation
- Comprehensive validation of response formats and status codes

The `/meds` endpoint tests use mocking to avoid actual GitHub API calls during testing.
