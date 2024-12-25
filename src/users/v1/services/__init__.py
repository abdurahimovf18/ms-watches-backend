from .cache_services import UserCacheServices
from .db_services import UserDbServices


UserCacheServices.set_db_services(UserDbServices)
