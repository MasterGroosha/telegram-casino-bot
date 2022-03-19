from typing import Optional

from pydantic import BaseSettings, BaseModel, validator


class Redis(BaseModel):
    host: str
    port: int = 6379
    db: int
    password: str = "IGivgFCKBmBmETW6cyoGQi7q0JQidBPgbrGSuoOQMGS86XEG8GnnS2811pn0DLoy"


class Settings(BaseSettings):
    bot_token: str
    fsm_mode: str
    redis: Optional[Redis]

    @validator("fsm_mode")
    def fsm_type_check(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect fsm_mode. Must be one of: memory, redis")
        return v

    @validator("redis")
    def skip_validating_redis(cls, v, values):
        if values["fsm_mode"] == "redis" and v is None:
            raise ValueError("Redis config is missing, though fsm_type is 'redis'")
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()
