from src.utils.schemas import BaseDbSchema



class WDDbSchema(BaseDbSchema):
    content: str
    watch_id: int
    