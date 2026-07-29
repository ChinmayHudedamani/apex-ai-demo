# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Global Unhandled Exception & Error Monitoring Middleware

import sys
from fastapi import Request
from starlette.responses import JSONResponse
from app.core.logging import logger

try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None


async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler catching all unhandled runtime exceptions.
    Prevents stack trace exposure to end-users and reports error metadata to Sentry.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    user_id = getattr(request.state, "user_id", "anonymous")

    # Log structured JSON error internally
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
        exc_info=sys.exc_info(),
        extra={
            "requestId": request_id,
            "userId": user_id,
            "contextMetadata": {
                "method": request.method,
                "path": request.url.path,
                "clientIp": request.client.host if request.client else "unknown",
            },
        },
    )

    # Attach context metadata to Sentry scope if SDK is active
    if sentry_sdk and sentry_sdk.Hub.current.client:
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("request_id", request_id)
            scope.set_tag("path", request.url.path)
            scope.set_user({"id": user_id})
            sentry_sdk.capture_exception(exc)

    # Return safe, non-leaking generic HTTP 500 error payload to client
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "detail": "An unexpected error occurred. Our engineering team has been notified.",
            "request_id": request_id,
        },
    )
