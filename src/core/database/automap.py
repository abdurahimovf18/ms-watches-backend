from typing import TypeAlias, Any
import re

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from .database_settings import DB_SYNC_URL


# Create an AutomapBase instance for reflecting database tables
automap = automap_base()

# Create an engine for database connection
prep_engine = create_engine(DB_SYNC_URL)

# Prepare the AutomapBase instance by reflecting the database schema
automap.prepare(autoload_with=prep_engine)

# Define type aliases for better readability
ModelName: TypeAlias = str
TableName: TypeAlias = str


def model_to_table(name: ModelName) -> TableName:
    """
    Dynamically generates a table name in snake_case format from a given model name.
    Converts CamelCase model names to snake_case and removes the "_Model" suffix.

    Args:
        name (ModelName): The model name in CamelCase.

    Returns:
        TableName: The generated table name in snake_case.

    Example:
        >>> model_to_table("UserModel")
        'user'
        >>> model_to_table("SomeOtherClass")
        'some_other_class'
    """
    # Convert CamelCase to snake_case
    snake_case_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    # Remove "_model" suffix if present
    return snake_case_name.removesuffix("_model")


def get_model(name: ModelName | TableName, automap: Any = automap):
    """
    Retrieves the dynamically mapped model class or table class from the AutomapBase instance.

    Args:
        name (ModelName | TableName): The name of the model class or table.
            - If a model name is provided, it converts it to the corresponding table name.
        automap (Any): The AutomapBase instance containing the mapped classes.

    Returns:
        The dynamically mapped model class corresponding to the provided name.

    Raises:
        ValueError: If the specified model or table name does not exist in the AutomapBase instance.

    Example:
        >>> UsersModel = get_model("UserModel")
        >>> users_table = get_model("users")
    """
    # Convert the model name to a table name
    table_name = model_to_table(name)

    # Access the classes attribute of the automap object
    cls = automap.classes

    # Check if the table name exists in the automap classes
    if not hasattr(cls, table_name):
        table_define = "table" if name == table_name else "model"
        raise ValueError(f"automap_base object {automap!s} does not have {table_define} '{name}'.")

    # Return the dynamically mapped class
    return getattr(cls, table_name)
