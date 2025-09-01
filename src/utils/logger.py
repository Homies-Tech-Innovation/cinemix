# src/utils/logger.py
import logging
import sys
import os
import json as _json
from typing import Optional
from src.config import settings
# Singleton logger
_logger: Optional[logging.Logger] = None


def setup_logging(
    app_name: str = "cinemix",
    level: Optional[str] = None,
    json: Optional[bool] = None,
) -> logging.Logger:
    """
    Configure global logging:
    - Console always enabled
    - Optional file logging
    - JSON or plain text format
    """
    global _logger
    if _logger:
        return _logger

    # --- Config ---
    level_name = (level or settings.LOG_LEVEL).upper()
    use_json = json if json is not None else settings.LOG_JSON
    log_file = settings.LOG_FILE
    datefmt = "%Y-%m-%d %H:%M:%S"

    # --- Formatters ---
    class PlainFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
            formatter = logging.Formatter(fmt, datefmt=datefmt)
            return formatter.format(record)

    class JSONFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            log_obj = {
                "ts": self.formatTime(record, datefmt),
                "level": record.levelname,
                "logger": record.name,
                "msg": record.getMessage(),
            }
            if record.exc_info:
                log_obj["exc_info"] = self.formatException(record.exc_info)
            return _json.dumps(log_obj, ensure_ascii=False)

    formatter = JSONFormatter(datefmt=datefmt) if use_json else PlainFormatter()

    # --- Root logger ---
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # capture all levels

    # Clear old handlers
    for h in list(root.handlers):
        root.removeHandler(h)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(getattr(logging, level_name, logging.INFO))
    console.setFormatter(formatter)

    # Windows UTF-8 safe
    reconf = getattr(console.stream, "reconfigure", None)
    if callable(reconf):
        reconf(encoding="utf-8")

    root.addHandler(console)

    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level_name, logging.INFO))
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    # Align Uvicorn/FastAPI loggers
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        log = logging.getLogger(name)
        log.setLevel(getattr(logging, level_name, logging.INFO))
        log.propagate = True

    # App-specific logger
    _logger = logging.getLogger(app_name)
    _logger.setLevel(getattr(logging, level_name, logging.INFO))
    _logger.debug("Logger initialized", extra={"app": app_name, "json": use_json})

    return _logger


# Auto-init singleton
logger = setup_logging()
