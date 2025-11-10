from fastapi import FastAPI

from app.routes.greet import router as greet_router
from app.routes.health import router as health_router
from app.routes.math import router as math_router
from app.routes.root import router as root_router

app = FastAPI()

app.include_router(greet_router)
app.include_router(health_router)
app.include_router(math_router)
app.include_router(root_router)