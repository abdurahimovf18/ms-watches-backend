from datetime import timezone
from pathlib import Path
from pydantic_settings import BaseSettings


# BASE_DIR points to the root directory of the project (3 levels up from the current file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ENV_FILE_PATH specifies the path to the .env file located at the root of the project
ENV_FILE_PATH = BASE_DIR / ".env"

# DEBUG flag for enabling/disabling development mode features like detailed error messages
DEBUG = True

TIMEZONE = timezone.utc

ALLOWED_HOSTS: list[str] = ["http://localhost:3000", "http://0.0.0.0:3000", "http://127.0.0.1:3000"]


class Settings(BaseSettings):
    """
    Base Settings class for the application. This class is used to load and manage
    all environment variables from a `.env` file or other external configuration sources.

    The `Settings` class leverages `pydantic.BaseSettings` to automatically read values 
    from environment variables, making it easier to manage environment-based configurations.

    Attributes:
        SECRET_KEY (str): A secret key for cryptographic operations (e.g., JWT signing, HMAC).
        
    The `.env` file (or environment variables) should define values for any required settings
    like `SECRET_KEY`. These values are automatically loaded into class attributes.

    Example Usage:
        ```python
        # Assuming ENV_FILE_PATH is set correctly
        settings = Settings()  # Load settings from .env file or environment
        print(settings.SECRET_KEY)  # Access the secret key from the settings
        ```
    """

    ######################
    # postgresql secrets #
    ######################

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str 
    DB_PORT: int
    DB_NAME: str

    ############################
    # Authentification secrets #
    ############################

    SECRET_KEY: str 
    
    JWT_ALGORITHM: str 
    JWT_EXPIRE_MINUTE: int 
    
    JWT_REFRESH_EXPIRE_DAYS: int 
    ISSUER: str
    AUDIENCE: str

    ################
    # Cache secrets#
    ################

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    

    class Config:
        """
        Configuration class for `BaseSettings`.

        The `Config` class is used to configure settings specific to the pydantic 
        `BaseSettings` class, such as specifying the location of the `.env` file 
        or customizing the behavior of environment variable loading.

        Attributes:
            env_file (str): Path to the .env file where environment variables are stored.
        
        Example:
            If the environment variables are stored in a `.env` file at `./config/.env`:
                env_file = './config/.env'
        """
        
        # Specify the path to the .env file that contains environment variables
        env_file = ENV_FILE_PATH  # Ensure this is set correctly to the actual file path




ENV_SETTINGS = Settings()


class BaseEnvConsumer:
    """
    A base class to facilitate the consumption of environment-based settings
    into class attributes, typically from environment variables or a configuration 
    system (like `BaseSettings` from `pydantic` or similar).

    This class dynamically assigns attributes to its instances based on its annotations
    and retrieves the corresponding values from the provided `settings` (typically environment-based).

    Example:
        ```python
        class DatabaseEnvConsumer(BaseEnvConsumer):
            db_file: str

        DB_ENV = DatabaseEnvConsumer()

        print(DB_ENV.db_file)
        ```

        In this example, the class `DatabaseEnvConsumer` inherits from `BaseEnvConsumer` 
        and defines a `db_file` attribute. When an instance of `DatabaseEnvConsumer` 
        is created, it will attempt to populate the `db_file` attribute with the 
        corresponding value from the environment settings (e.g., `ENV_SETTINGS`).

    Attributes:
        settings (BaseSettings): The environment configuration settings to retrieve values from.
        (By default, `ENV_SETTINGS` is used as the source.)

    Methods:
        __init__: Initializes the instance and assigns values to annotated attributes 
                  from the provided settings or default values if available.
        get_data: Retrieves the value for a given key from the settings or defaults.
    """

    settings: BaseSettings = ENV_SETTINGS  # Default environment settings to load values from

    def __init__(self):
        """
        Initializes the instance by dynamically assigning values to class attributes 
        based on type annotations. The values are fetched from the `settings` object 
        (usually environment variables or a similar configuration source).

        This constructor loops through all class annotations (which define expected settings) 
        and attempts to assign values from the environment or provided settings.

        Raises:
            AttributeError: If a required setting is missing and cannot be found in either 
                            the settings or as a class attribute.
        """

        for key in type(self).__annotations__.keys():
            data = self.get_data(key)
            setattr(self, key, data)

    def get_data(self, key: str):
        """
        Retrieves the value for a specified key either from the provided `settings` 
        or as a default class attribute. If neither is found, an `AttributeError` is raised.

        Args:
            key (str): The name of the attribute to fetch from the settings.

        Returns:
            The value of the setting for the provided key.

        Raises:
            AttributeError: If neither the `settings` nor the class has an attribute 
                            matching the specified `key`.
        """

        if hasattr(self.settings, key):
            return getattr(self.settings, key)
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            raise AttributeError(f"Environment settings: {self.settings} has no required Attribute {key}")
