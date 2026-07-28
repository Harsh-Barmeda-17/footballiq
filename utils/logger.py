"""Centralised logging setup for FootballIQ. Every module gets its own named logger
that writes to both console and a shared log file."""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "footballiq.log"

_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger for `name` (use __name__ from the calling module).

    Safe to call multiple times with the same name — won't attach duplicate handlers.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if get_logger() is called again for the same name
    if logger.handlers:
        return logger

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Don't let messages bubble up to the root logger and print twice
    logger.propagate = False

    return logger