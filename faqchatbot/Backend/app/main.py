from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database import Base, engine, init_redis, close_redis, get_redis  # ← add get_redis here
from app.api import admin_api, question_api, source_api

logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.warning(f"Could not create database tables (DB may not be available): {e}")

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_api.router)
app.include_router(question_api.router)
app.include_router(source_api.router)


@app.on_event("startup")
async def startup():
    try:
        await init_redis()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.warning(f"Could not connect to Redis: {e}")


@app.on_event("shutdown")
async def shutdown():
    await close_redis()
    logger.info("Redis connection closed")


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/ping-redis")
async def ping_redis():
    r = get_redis()
    await r.set("foo", "bar")
    value = await r.get("foo")
    return {"foo": value}