import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = os.getenv('app_host', '127.0.0.1')
    app_port: int = os.getenv('app_port', 8000)

    server_host: str = os.getenv('server_host', '127.0.0.1')
    server_port: int = os.getenv('server_port', 9000)

    db_url: str = os.getenv('db_url', '')

    time_format: str = os.getenv('time_format', '%Y-%m-%d %H:%M')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


load_dotenv()
settings = Settings()
