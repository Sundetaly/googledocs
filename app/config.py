import os
from typing import List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Google docs
    CREDENTIALS_FILE: str
    INBOUND_FILE_NAME: str
    OUTBOUND_FILE_NAME: str
    MOBILE_PHONE_CODES: List[str] = ["700", "701", "702", "705", "707", "708", "747", "771", "775", "776", "777", "778"]

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
