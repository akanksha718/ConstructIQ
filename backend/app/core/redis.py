"""Optional Redis client for caching and pub/sub.
 
 If REDIS_URL is not set or redis-py is not installed, the client
 is disabled and all operations are no-ops.
"""
 
from __future__ import annotations
 
import logging
import hashlib
import json
from typing import Optional
 
from app.core.config import settings
 
logger = logging.getLogger(__name__)
 
try:
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None  # type: ignore
 
 
class RedisClient:
    def __init__(self) -> None:
        self._client: Optional[redis.Redis] = None
        if not settings.REDIS_URL or redis is None:
            return
        try:
            self._client = redis.from_url(settings.REDIS_URL)
        except Exception:  # pragma: no cover - connection issues
            logger.exception("Failed to init Redis client; disabling.")
            self._client = None
 
    def enabled(self) -> bool:
        return self._client is not None
 
    async def get(self, key: str) -> Optional[bytes]:
        if not self.enabled():
            return None
        assert self._client is not None
        return await self._client.get(key)
 
    async def set(self, key: str, value: str, expire: int = 60) -> bool:
        if not self.enabled():
            return False
        assert self._client is not None
        try:
            await self._client.set(name=key, value=value, ex=expire)
            return True
        except Exception:  # pragma: no cover
            return False
 
    async def delete(self, key: str) -> bool:
        if not self.enabled():
            return False
        assert self._client is not None
        try:
            await self._client.delete(key)
            return True
        except Exception:  # pragma: no cover
            return False
 
    async def publish(self, channel: str, message: str) -> int:
        if not self.enabled():
            return 0
        assert self._client is not None
        try:
            return await self._client.publish(channel, message)
        except Exception:  # pragma: no cover
            return False
 
    async def close(self) -> None:
        if self._client is not None:
            await self._client.close()


class QueryCache:
    """Best-effort synchronous cache used by the synchronous chat request path."""

    VERSION_KEY = "constructiq:corpus-version"

    def __init__(self) -> None:
        self._client = None
        if not settings.REDIS_URL:
            return
        try:
            import redis  # type: ignore

            self._client = redis.Redis.from_url(
                settings.REDIS_URL, decode_responses=True, socket_timeout=1
            )
        except Exception:  # pragma: no cover - optional dependency
            logger.exception("Failed to initialise synchronous Redis cache.")

    def get_response(self, question: str, instruction: str) -> dict | None:
        if self._client is None:
            return None
        try:
            version = self._client.get(self.VERSION_KEY) or "0"
            digest = hashlib.sha256(f"{version}:{question}:{instruction}".encode()).hexdigest()
            value = self._client.get(f"constructiq:chat:{digest}")
            return json.loads(value) if value else None
        except Exception:  # pragma: no cover - cache must never block chat
            logger.warning("Redis cache read failed; continuing without cache.")
            return None

    def set_response(self, question: str, instruction: str, response: dict) -> None:
        if self._client is None:
            return
        try:
            version = self._client.get(self.VERSION_KEY) or "0"
            digest = hashlib.sha256(f"{version}:{question}:{instruction}".encode()).hexdigest()
            self._client.setex(
                f"constructiq:chat:{digest}", settings.QUERY_CACHE_TTL_SECONDS,
                json.dumps(response),
            )
        except Exception:  # pragma: no cover
            logger.warning("Redis cache write failed; continuing without cache.")

    def invalidate_corpus(self) -> None:
        """Advance the corpus version; existing keys expire naturally."""
        if self._client is None:
            return
        try:
            self._client.incr(self.VERSION_KEY)
        except Exception:  # pragma: no cover
            logger.warning("Redis corpus-version update failed.")


query_cache = QueryCache()
 
