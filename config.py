import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Google docs
    # CREDENTIALS_FILE = Field(env='CREDENTIALS_FILE')
    # INBOUND_FILE_NAME = Field(env='INBOUND_FILE_NAME')
    # OUTBOUND_FILE_NAME = Field(env='OUTBOUND_FILE_NAME')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
