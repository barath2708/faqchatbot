from sqlalchemy import create_engine # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import redis.asyncio as redis  # ADD THIS IMPORT

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency - yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- ADD EVERYTHING BELOW THIS LINE ----------

redis_client: redis.Redis | None = None

async def init_redis():
    """Called once on app startup to open the Redis connection."""
    global redis_client
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        ssl=True,
        decode_responses=True,
    )

async def close_redis():
    """Called once on app shutdown to close the Redis connection cleanly."""
    if redis_client:
        await redis_client.close()

def get_redis():
    """FastAPI dependency - use this in routes that need Redis."""
    return redis_client