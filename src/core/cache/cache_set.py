from .cache_instances.redis_instance import get_instance
from .cache_settings import CACHE_ENV


cache = get_instance(
    host=CACHE_ENV.REDIS_HOST, 
    port=CACHE_ENV.REDIS_PORT,
    db=CACHE_ENV.REDIS_DB
)
