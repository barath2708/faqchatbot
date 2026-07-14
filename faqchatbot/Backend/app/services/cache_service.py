import json
import hashlib
import logging

import redis

from app.config import settings

logger = logging.getLogger(__name__)

# Use Redis URL directly for Upstash (or fallback to host/port config)
redis_client = None
try:
    if settings.REDIS_URL:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    else:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            ssl=True,
            decode_responses=True,
        )
    # Test the connection
    redis_client.ping()
    logger.info("Redis cache connected successfully")
except Exception as e:
    logger.warning(f"Could not connect to Redis cache: {e}. Caching will be disabled.")
    redis_client = None


def _make_key(question: str) -> str:
    normalized = question.strip().lower()
    return "faq:" + hashlib.sha256(normalized.encode()).hexdigest()


def get_cached_answer(question: str) -> dict | None:
    if not redis_client:
        return None
    try:
        key = _make_key(question)
        cached = redis_client.get(key)
        return json.loads(cached) if cached else None
    except Exception as e:
        logger.warning(f"Cache retrieval failed: {e}")
        return None


def set_cached_answer(question: str, answer_data: dict) -> None:
    if not redis_client:
        return
    try:
        key = _make_key(question)
        redis_client.setex(key, settings.CACHE_TTL_SECONDS, json.dumps(answer_data))
    except Exception as e:
        logger.warning(f"Cache storage failed: {e}")