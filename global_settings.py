import os
from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):

    DEV: bool = True

    BASE_DIR = Path(__file__).resolve().parent

    DATABASE_PATH = os.path.join(BASE_DIR, 'database')


settings = Settings()

def state_project():
    return settings.DEV

# print(settings.DATABASE_PATH)