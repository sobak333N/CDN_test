from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_INNER_PORT: int
    FETCH_URL: str
    PAGE_LIMIT: int
    CITIES_LIMIT: int
    # API_KEY: str
    # BEARER_TOKEN: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    class config:
        env_file = ".env"
        extra = "ignore"


config = Settings()