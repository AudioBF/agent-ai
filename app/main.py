import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.agent import run_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="AI Agent with Tool Use",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    logger.info("Health check called")
    return {"status": "ok", "env": settings.app_env}


@app.get("/hello/{name}")
def say_hello(name: str):
    if len(name) < 2:
        raise HTTPException(
            status_code=400,
            detail="Name must have at least 2 characters.",
        )
    return {"message": f"Hello, {name}!"}


@app.post("/chat")
def chat(request: ChatRequest):
    logger.info(f"Message received: {request.message}")
    try:
        response = run_agent(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal agent error.")
