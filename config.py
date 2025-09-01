import logging
from logging.config import dictConfig


def setup_logging(level: str | int = "INFO") -> None:
    """
    Configure application-wide logging, including uvicorn loggers.
    Call this early in main before creating the FastAPI app.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "loggers": {
                "controllers": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
                "services": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
                "repositories": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
                "uvicorn": {"handlers": ["console"], "level": "INFO"},
                "uvicorn.error": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "root": {"handlers": ["console"], "level": level},
        }
    )
