from sqlalchemy import MetaData

from .database_set import default_metadata
from . import models


METADATA_SEQ: MetaData = [
    default_metadata,
]
