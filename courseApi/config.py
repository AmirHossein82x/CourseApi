from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
from functools import lru_cache


load_dotenv()


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    DB_FORCE_ROL_BACK: bool = False
    model_config = SettingsConfigDict(env_file=".env")


class GlobalConfig(BaseSettings):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    DB_FORCE_ROL_BACK: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()  # use cache
def get_config(env_state):
    configs = {"dev": DevConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
