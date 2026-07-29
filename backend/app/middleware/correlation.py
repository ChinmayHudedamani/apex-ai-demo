# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Correlation ID & Structured Request Context Middleware

import uuid
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that generates or extracts an X-Request-ID correlation header
    for every incoming request and emits structured JSON access logs.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # Extract existing X-Request-ID from client header or generate new UUID4
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        # Extract user identity if present in headers or state
        user_id = request.headers.get("X-User-ID") or getattr(request.state, "user_id", "anonymous")

        response: Response = await call_next(request)

        # Attach X-Request-ID header to response
        response.headers["X-Request-ID"] = request_id

        latency_ms = round((time.time() - start_time) * 1000, 2)
        client_ip = request.client.host if request.client else "unknown"

        # Emit structured JSON access log
        log_extra = {
            "requestId": request_id,
            "userId": user_id,
            "contextMetadata": {
                "method": request.method,
                "path": request.url.path,
                "statusCode": response.status_code,
                "latencyMs": latency_ms,
                "clientIp": client_ip,
                "userAgent": request.headers.get("User-Agent", "unknown"),
            },
        }

        logger.info(
            f"HTTP {request.method} {request.url.path} -> {response.status_code} ({latency_ms}ms)",
            extra=log_extra,
        )

        return response
