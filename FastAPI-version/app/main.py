from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_router
from app.config import settings
from app.logging import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Image Classification API",
    version="1.0.0",
    description="Async FastAPI API for image classification with InceptionV3.",
    contact={"name": "Samuel Edungbola", "email": "sedungbola@gmail.com"},
    openapi_tags=[
        {"name": "auth", "description": "User registration and login"},
        {"name": "classify", "description": "Image classification"},
        {"name": "admin", "description": "Admin operations"},
        {"name": "system", "description": "Health and readiness checks"},
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging()

app.include_router(api_router, prefix="/v1")

Instrumentator().instrument(app).expose(app)

@app.get("/healthz", tags=["system"])
def healthz():
    return {"status": "ok"}

@app.get("/readyz", tags=["system"])
def readyz():
    from app.services.ml import model_loaded
    from app.db import db_ping
    return {"model": model_loaded(), "db": db_ping()}
