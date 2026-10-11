"""Structured logging configuration for AgriGuard AI."""

import logging
import os
import sys
from pathlib import Path


def get_logger(name: str = "agriguard") -> logging.Logger:
    """Returns a pre-configured logger with console and file output."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "agriguard.log"

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setFormatter(formatter)
    logger.addHandler(c_handler)

    # File handler
    try:
        f_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)
    except Exception:
        pass

    return logger
