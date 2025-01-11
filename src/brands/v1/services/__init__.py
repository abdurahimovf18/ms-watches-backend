from .db_services import BrandDbServices
from .cache_services import BrandCacheServices
from .router_services import *


BrandCacheServices.set_db_services(BrandDbServices)
