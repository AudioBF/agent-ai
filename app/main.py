import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from app.config import settings

#logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s |%(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

#create aplication
app = FastAPI(
    title=settings.app_name,
    description="An AI agent that can perform with Tool Use",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Only allow requests from Streamlit frontend
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    logger.info("Health check requested.")
    return {"status": "ok", "env": settings.app_env}

@app.get("/hello/{name}")
def say_hello(name: str):
    if len(name) < 2:
       raise HTTPException(
           status_code=400,
           detail="Name must be at least 2 characters long."
        )
    return {"message": f"Hello, {name}!"}