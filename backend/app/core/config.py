from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Realtor Express API"
    ENV: str = "dev"
    DEBUG: bool = True

    DATABASE_URL: str

    JWT_SECRET: str = "change_me"
    JWT_ALG: str = "HS256"
    JWT_ACCESS_EXPIRES_MIN: int = 60

    # На MVP можно "*" или список доменов
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
