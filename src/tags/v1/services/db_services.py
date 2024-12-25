from src.core.database.utils import BaseService, service_decorator

from ...models import TagsModel


class TagServices(BaseService):
    model = TagsModel
