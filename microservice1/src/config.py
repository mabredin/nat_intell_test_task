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
    POSTGRES_DB: str = "postgres"
    echo: bool = False
    
    @property
    def url(self):
        return f"{self.DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    

app_settings = AppSettings()
database_settings = DatabaseSettings()
