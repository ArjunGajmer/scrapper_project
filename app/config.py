import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    REDIS_URL: str = os.getenv("REDIS_UR", "redis://localhost:6379/0")
    MAX_RETRY_COUNT: int = int(os.getenv('MAX_RETRY_COUNT', 10))
    RETRY_DELAY: int = int(os.getenv('RETRY_DELAY', 60 * 1))
    SCRAPED_DATA_STORE: str = os.getenv('SCRAPED_DATA_STORE', '../.scrapped_data')
    PATH_TO_MEDIA_STORE: str = os.getenv('SCRAPED_DATA_STORE', '../.scrapped_data/media')
    EMAIL_NOTIFICATION_SRC: str = os.getenv('EMAIL_NOTIFICATION_SRC', 'arj@somedomain.com')

    class Config:
        env_file = ".env"


settings = Settings()
