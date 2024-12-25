from src.core.database.utils import BaseService, service_decorator
from ...models import WatchesModel


class WatchServices(BaseService):
    model = WatchesModel

    @service_decorator()
    async def create_watch(cls, session, **kwargs):
        pass
        