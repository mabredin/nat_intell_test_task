import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)


class AppSettings(BaseSettings):
    class Config:
        env_prefix = "app_"

    DEBUG: bool = os.getenv("DEBUG") or True
    PROJECT_NAME: str = os.getenv("PROJECT_NAME") or "Test"


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "database_"

    DRIVER: str = "postgresql+asyncpg"
    POSTGRES_HOST: str = os.getenv("DB_HOST") or "localhost"
    POSTGRES_PORT: str = os.getenv("DB_PORT") or "5432"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER") or "postgres"
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD") or "postgres"
    POSTGRES_DB: str = os.getenv("POSTGRES_DB") or "nat_intel"
    echo: bool = os.getenv("ECHO") or False

    @property
    def url(self):
        return f"{self.DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class TokenSettings(BaseSettings):
    class Config:
        env_prefix = "token_"

    SECRET_KEY_TOKEN: str = (
        os.getenv("SECRET_KEY_TOKEN")
        or "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = os.getenv("ALGORITHM") or "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 30

    @property
    def bcrypt_context(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def oauth2_scheme(self):
        return OAuth2PasswordBearer(tokenUrl="api/v1/token")


class OuterMicroserviceSettings(BaseSettings):
    class Config:
        env_prefix = "token_"

    GET_BALANCE: str = (
        os.getenv("GET_BALANCE") or "http://localhost:8002/api/v1/balance/"
    )
    GET_LATEST_BLOCK: str = (
        os.getenv("GET_LATEST_BLOCK")
        or "http://localhost:8002/api/v1/info/latest_block"
    )
    VERIFY_ADDRESS: str = (
        os.getenv("VERIFY_ADDRESS") or "http://localhost:8002/api/v1/verify_address/"
    )

    @property
    def bcrypt_context(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def oauth2_scheme(self):
        return OAuth2PasswordBearer(tokenUrl="api/v1/token")


app_settings = AppSettings()
database_settings = DatabaseSettings()
token_settings = TokenSettings()
outer_microservice_settings = OuterMicroserviceSettings()
