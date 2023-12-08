import logging.config

logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "{asctime} - {name} - {levelname} - {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console",
        },
    },
    "loggers": {
        "app_logger": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

logging.config.dictConfig(logging_conf)
logger = logging.getLogger("app_logger")
