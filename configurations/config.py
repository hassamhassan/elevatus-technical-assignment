from typing import Optional

from pydantic_settings import BaseSettings


class DevelopmentSettings(BaseSettings):
    """
    Settings class to manage development environment variables.
    """
    MONGODB_URL: Optional[str] = None
    ACCESS_TOKEN_EXPIRE: Optional[str] = None
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: Optional[str] = None

    class Config:
        env_file = ".env"


settings = DevelopmentSettings()
