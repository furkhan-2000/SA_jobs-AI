from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_PORT: int = 7070
    DATABASE_URL: Optional[str] = None  # placeholder
    LOG_LEVEL: str = "INFO"
    MAX_RETRIES: int = 3
    TIMEOUT: int = 15
    PAGE_SIZE: int = 20
    # Keys (placeholders — already stored in your memory)
    ADZUNA_APP_ID: str = "34b57806"
    ADZUNA_APP_KEY: str = "a4a65342386e18a41d55e203520809ad"
    JOOBLE_KEY: str = "bcf720ac-ffc5-429e-ae29-797dedf6ee44"
    CAREERJET_KEY: str = "6fde6cdcf3154cacfe7c6fe002c3c86c"
    OPENWEBNINJA_KEY: str = "ak_q7f0dwbhl7k7txtot1sp5ltun9lr7rwlgz2070mx1l3b53w"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
