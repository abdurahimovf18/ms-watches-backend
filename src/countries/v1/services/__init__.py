from .cache_services import CountryCacheServices as cache
from .db_services import CountryDbServices as db


cache.set_db_services(db)
