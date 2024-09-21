from logging.config import dictConfig
from courseApi.config import DevConfig, config
import logging


def obfuscated(email: str, obfuscated_length):
    charecters = email[:obfuscated_length]
    first, last = email.split("@")
    return charecters + ("*" * (len(first) - obfuscated_length)) + "@" + last


class EmailObfusCationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 3) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfusCationFilter,
                    "obfuscated_length": 4 if isinstance(config, DevConfig) else 0,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(asctime)s %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    # "class": "logging.Formatter", # for creating log file in .log mode
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    # "format": "%(asctime)s.%(msecs)03dz | %(levelname)-8s | [%(correlation_id)s] | %(name)s:%(lineno)d - %(message)s", for when you are using .log file
                    "format": "%(asctime)s.%(msecs)03dz %(levelname)-8s [%(correlation_id)s] %(name)s:%(lineno)d - %(message)s",  # for when you are using json file
                },
            },
            "handlers": {
                "default": {
                    # "class": "logging.StreamHandler",
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "courseApi.log",
                    "maxBytes": 1024 * 1024,  # 1MB
                    "backupCount": 5,  # keep just 5 blogapi.log files
                    "encoding": "utf8",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "DEBUG"},
                "courseApi": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"},
            },
        }
    )
