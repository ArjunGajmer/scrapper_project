import redis
from urllib.parse import urlparse

from app.config import settings

redis_parsed_url = urlparse(settings.REDIS_URL)
host = redis_parsed_url.hostname
port = redis_parsed_url.port
db = int(redis_parsed_url.path.lstrip('/'))
redis_client = redis.StrictRedis(host=host, port=port, db=db)


def cache_data(key: str, value: str, ttl: int = 3600):
    redis_client.set(key, value, ex=ttl)


def get_cached_data(key: str):
    return redis_client.get(key)


def destroy_cached_data(key_like):
    keys_to_delete = redis_client.keys(match=key_like)
    for key in keys_to_delete:
        redis_client.delete(key)
