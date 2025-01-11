from .cache_services import UserCacheServices as cache
from .db_services import UserDbServices as db


cache.set_db_services(db)
