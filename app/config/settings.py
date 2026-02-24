from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # JWT
    DATABASE_URL: str
    APP_SECRET_KEY: str
    ALGORITHM: str
    APP_ACCESS_TOKEN_EXPIRE_MINUTES: int
    APP_REFRESH_TOKEN_EXPIRE_DAYS: int
    APP_ENVIRONMENT: str

    # Configuration
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()