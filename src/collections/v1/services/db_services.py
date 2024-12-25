from src.core.database.utils import BaseService, service_decorator

from ...models import CollectionsModel


class CollectionServices(BaseService):
    model = CollectionsModel
