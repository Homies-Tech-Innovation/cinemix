# src/utils/logger.py
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

LOG_COLORS = {
    "DEBUG": "\033[94m",    # Blue
    "INFO": "\033[92m",     # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",    # Red
    "CRITICAL": "\033[95m", # Magenta
}
RESET_COLOR = "\033[0m"

_app_logger = None  # Singleton to prevent multiple initializations


def _to_bool(val: object, default: bool = False) -> bool:
    if val is None:
        return default
    s = str(val).strip().lower()
    return s in {"1", "true", "yes", "y", "on"}


def setup_logging(
    app_name: str = "cinemix",
    level: Optional[str] = None,
    json: Optional[bool] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Setup application-wide logging.
    """
    global _app_logger
    if _app_logger:
        return _app_logger

    # --- Config values ---
    level_name = (level or os.getenv("LOG_LEVEL", "DEBUG")).upper()
    use_json = _to_bool(json if json is not None else os.getenv("LOG_JSON", "false"))
    log_file = log_file or os.getenv("LOG_FILE", "logs/cinemix.log")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # --- Formatters ---
    datefmt = "%Y-%m-%d %H:%M:%S"
    fmt_plain = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            msg = super().format(record)
            color = LOG_COLORS.get(record.levelname, "")
            return f"{color}{msg}{RESET_COLOR}" if not use_json else msg

    class JSONFormatter(logging.Formatter):
        def format(self, record):
            import json as _json
            base = {
                "ts": self.formatTime(record, datefmt),
                "level": record.levelname,
                "logger": record.name,
                "msg": record.getMessage(),
                # Optional debug fields:
                # "file": record.filename,
                # "line": record.lineno,
                # "func": record.funcName,
            }
            if record.exc_info:
                base["exc_info"] = self.formatException(record.exc_info)
            return _json.dumps(base, ensure_ascii=False)

    formatter = JSONFormatter(datefmt=datefmt) if use_json else ColoredFormatter(fmt_plain, datefmt=datefmt)

    # --- Handlers ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level_name)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(
        JSONFormatter(datefmt=datefmt) if use_json else logging.Formatter(fmt_plain, datefmt=datefmt)
    )
    file_handler.setLevel(level_name)

    # --- Root logger ---
    root = logging.getLogger()
    root.setLevel(getattr(logging, level_name, logging.DEBUG))  # that roo thing Fixed here

    # Remove existing handlers (avoid duplicates with --reload)
    for h in list(root.handlers):
        root.removeHandler(h)

    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # --- Apply to Uvicorn & FastAPI loggers ---
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        l = logging.getLogger(name)
        l.handlers = [console_handler, file_handler]
        l.setLevel(logging.WARNING)  # Lower noise, keep serious logs
        l.propagate = False

    # --- App logger ---
    app_logger = logging.getLogger(app_name)
    app_logger.setLevel(level_name)
    app_logger.info("Logger initialized ✅")

    _app_logger = app_logger
    return app_logger