from dataclasses import dataclass
from os import getenv


@dataclass
class TgBot:
    token: str
    fsm_type: str


@dataclass
class Redis:
    host: str
    port: int
    db: int
    password: str


@dataclass
class Config:
    bot: TgBot
    redis: Redis


def load_config() -> Config:
    return Config(
        bot=TgBot(
            token=getenv("BOT_TOKEN"),
            fsm_type=getenv("FSM_MODE", "memory")
        ),
        redis=Redis(
            host=getenv("REDIS_HOST", "localhost"),
            port=int(getenv("REDIS_PORT", 6379)),
            db=int(getenv("REDIS_DB", 0)),
            password=getenv("REDIS_PASSWORD", "IGivgFCKBmBmETW6cyoGQi7q0JQidBPgbrGSuoOQMGS86XEG8GnnS2811pn0DLoy")
        )
    )
