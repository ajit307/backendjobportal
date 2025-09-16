from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    debug: bool = True

    class Config:
        env_file = ".env"       # Load variables from .env
        extra = "ignore"        # Ignore any unexpected env variables

# Create a single settings instance for the project
settings = Settings()
