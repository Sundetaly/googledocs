import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Google docs
    CREDENTIALS_FILE: str
    INBOUND_FILE_NAME: str
    OUTBOUND_FILE_NAME: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
