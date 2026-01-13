from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio
import json
import redis.asyncio as redis
import os

router = APIRouter(prefix="/api/v1/events", tags=["events"])

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

async def event_stream() -> AsyncGenerator[str, None]:
    """SSE stream com Redis pub/sub"""
    r = redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("sunops:events")
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield f"data: {message['data']}\n\n"
    finally:
        await pubsub.unsubscribe("sunops:events")
        await r.close()

@router.get("/stream")
async def sse_endpoint():
    """Endpoint SSE para dashboard"""
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/publish")
async def publish_event(event_type: str, data: dict):
    """Publica evento no Redis"""
    r = redis.from_url(REDIS_URL, decode_responses=True)
    event = {"type": event_type, "data": data}
    await r.publish("sunops:events", json.dumps(event))
    await r.close()
    return {"status": "published"}
