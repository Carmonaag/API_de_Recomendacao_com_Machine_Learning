import redis.asyncio as redis
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

redis_pool = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis_connection():
    return redis.Redis(connection_pool=redis_pool)

async def get_from_cache(key: str) -> dict | None:
    """
    Busca um valor do cache Redis.
    """
    try:
        redis_conn = await get_redis_connection()
        cached_data = await redis_conn.get(key)
        if cached_data:
            logger.debug(f"Cache hit for key: {key}")
            return json.loads(cached_data)
        logger.debug(f"Cache miss for key: {key}")
        return None
    except Exception as e:
        logger.error(f"Erro ao ler do cache Redis: {e}")
        return None

async def set_to_cache(key: str, value: dict, ttl: int = settings.CACHE_TTL):
    """
    Salva um valor no cache Redis com um TTL.
    """
    try:
        redis_conn = await get_redis_connection()
        await redis_conn.set(key, json.dumps(value, default=str), ex=ttl)
        logger.debug(f"Valor salvo no cache para a chave: {key}")
    except Exception as e:
        logger.error(f"Erro ao salvar no cache Redis: {e}")
