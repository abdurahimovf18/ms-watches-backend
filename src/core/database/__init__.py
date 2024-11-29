from sqlalchemy import MetaData

from .database_set import default_metadata

import src.auth.models


METADATA: MetaData = default_metadata
