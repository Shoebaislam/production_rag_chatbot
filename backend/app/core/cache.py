import hashlib
import redis

from backend.app.core.config import settings


redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True
)


def make_cache_key(question: str) -> str:
    normalized = question.strip().lower()
    hashed = hashlib.sha256(normalized.encode()).hexdigest()
    return f"chat:{hashed}"


def get_cache(question: str):
    key = make_cache_key(question)
    return redis_client.get(key)


def set_cache(question: str, value: str):
    key = make_cache_key(question)
    redis_client.set(
        key,
        value,
        ex=settings.cache_ttl_seconds
    )