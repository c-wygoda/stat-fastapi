from datetime import timedelta
from enum import Enum
from logging import basicConfig

from pydantic_settings import BaseSettings

from .models import Satellite

# TODO: Dynamically create fake, but "current" TLE
SAT1 = """HOTSAT-1
1 56954U 23084Y   24023.63059975  .00008549  00000+0  45379-3 0  9997
2 56954  97.5287 142.5644 0013039 154.9977 205.1890 15.15507477 34018"""


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARNING"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class Settings(BaseSettings):
    satellites: list[Satellite] = [
        Satellite(tle=SAT1, block_time=(timedelta(seconds=10), timedelta(seconds=10)))
    ]
    loglevel: LogLevel = LogLevel.INFO
    database: str = "sqlite://"

    @classmethod
    def load(cls) -> "Settings":
        settings = Settings()
        basicConfig(level=settings.loglevel.value)
        return settings
