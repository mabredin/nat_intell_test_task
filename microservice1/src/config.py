from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_prefix = "app_"

    ROOT_PATH: str = ""
    DEBUG: bool = True
    PROJECT_NAME: str = "Test"


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "database_"

    DRIVER: str = "postgresql+asyncpg"
    POSTGRES_HOST: str = "database"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "nat_intel"
    echo: bool = False

    @property
    def url(self):
        return f"{self.DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class TokenSettings(BaseSettings):
    class Config:
        env_prefix = "token_"

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def bcrypt_context(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def oauth2_scheme(self):
        return OAuth2PasswordBearer(tokenUrl="api/v1/token")


app_settings = AppSettings()
database_settings = DatabaseSettings()
token_settings = TokenSettings()
