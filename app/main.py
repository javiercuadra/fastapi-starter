from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.routes.greet import router as greet_router
from app.routes.health import router as health_router
from app.routes.math import router as math_router
from app.routes.meds import router as meds_router
from app.routes.root import router as root_router
from app.security.auth import validate_auth_config
from app.services.github_client import validate_github_config

app = FastAPI()

# Validate configuration at startup to fail fast
@app.on_event("startup")
def startup_validation():
    """Validate environment configuration at application startup."""
    validate_auth_config()
    validate_github_config()

app.include_router(greet_router)
app.include_router(health_router)
app.include_router(math_router)
app.include_router(meds_router)
app.include_router(root_router)
