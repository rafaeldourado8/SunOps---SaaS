from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .routers import auth, workflows, agents

app = FastAPI(
    title="SunwOps API",
    description="Sistema de Gestão para Empresas de Energia Solar",
    version="1.0.0"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - OWASP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# Routers
app.include_router(auth.router)
app.include_router(workflows.router)
app.include_router(agents.router)

import redis
import pika
import os
from sqlalchemy import text
from ..infrastructure.database.config import AsyncSessionLocal

@app.get("/")
async def root():
    return {"message": "SunwOps API", "version": "1.0.0"}

@app.get("/health")
async def health():
    status = {"status": "healthy", "services": {}}
    
    # PostgreSQL
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        status["services"]["postgresql"] = "connected"
    except Exception as e:
        status["services"]["postgresql"] = f"error: {str(e)}"
        status["status"] = "degraded"
    
    # Redis
    try:
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        r = redis.from_url(redis_url)
        r.ping()
        status["services"]["redis"] = "connected"
    except Exception as e:
        status["services"]["redis"] = f"error: {str(e)}"
        status["status"] = "degraded"
    
    # RabbitMQ
    try:
        rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        connection.close()
        status["services"]["rabbitmq"] = "connected"
    except Exception as e:
        status["services"]["rabbitmq"] = f"error: {str(e)}"
        status["status"] = "degraded"
    
    return status
