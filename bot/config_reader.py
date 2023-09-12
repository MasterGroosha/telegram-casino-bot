from enum import Enum
from typing import Optional

from pydantic import field_validator, SecretStr, RedisDsn, FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class FSMMode(str, Enum):
    MEMORY = "memory"
    REDIS = "redis"


class Settings(BaseSettings):
    bot_token: SecretStr
    fsm_mode: FSMMode
    redis: Optional[RedisDsn] = None
    bot_language: str
    starting_points: int = 50
    send_gameover_sticker: bool = False
    throttle_time_spin: int = 2
    throttle_time_other: int = 1

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @field_validator("redis", mode="after")
    @classmethod
    def skip_validating_redis(cls, v: Optional[RedisDsn], info: FieldValidationInfo):
        if info.data.get("fsm_mode") == FSMMode.REDIS and v is None:
            err = 'FSM Mode is set to "Redis", but Redis DNS is missing!'
            raise ValueError(err)
        return v
