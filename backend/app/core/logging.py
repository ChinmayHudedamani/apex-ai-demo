# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise Structured JSON Logger

import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """
    Production-grade JSON Formatter for FastAPI application logs.
    Outputs structured JSON logs conforming to SRE observability standards.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "logLevel": record.levelname,
            "loggerName": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Inject correlation ID, user ID, and context metadata if present in log record
        if hasattr(record, "requestId"):
            log_entry["requestId"] = getattr(record, "requestId")
        if hasattr(record, "userId"):
            log_entry["userId"] = getattr(record, "userId")
        if hasattr(record, "contextMetadata") and isinstance(getattr(record, "contextMetadata"), dict):
            log_entry["metadata"] = getattr(record, "contextMetadata")

        # Include exception details if exception occurred
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logger(name: str = "apex_ai") -> logging.Logger:
    """Configures structured JSON logging for stdout."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    logger.propagate = False
    return logger


logger = setup_logger()
