import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "resources/logs"
os.makedirs(LOG_DIR, exist_ok=True)


class ExcludeErrorsFilter:
    def filter(self, record):
        return record.levelno < logging.ERROR


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d - %(message)s",
        },
    },
    "filters": {
        "exclude_errors": {
            "()": ExcludeErrorsFilter,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # "daily_rotating_file": {
        #     "level": "INFO",
        #     "class": "logging.handlers.TimedRotatingFileHandler",
        #     "filename": str(LOG_DIR / "django.log"),
        #     "when": "midnight",
        #     "backupCount": 30,
        #     "formatter": "verbose",
        #     "filters": ["exclude_errors"],
        # },
        # "error_file": {
        #     "level": "ERROR",
        #     "class": "logging.handlers.TimedRotatingFileHandler",
        #     "filename": str(LOG_DIR / "django_error.log"),
        #     "when": "midnight",
        #     "backupCount": 30,
        #     "formatter": "verbose",
        # },
    },
    "loggers": {
        "django": {
            "handlers": ["console"], #, "daily_rotating_file", "error_file"],
            "level": "INFO",
            "propagate": True,
        },
        "root": {
            "handlers": ["console"], #, "daily_rotating_file", "error_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
