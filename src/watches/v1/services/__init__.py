from .db_services import WatchDbServices as db
from .cache_services import WatchCacheServices as cache


cache.set_db_services(db)
