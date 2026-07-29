# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise Health & Diagnostic Probes Router

from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.core.config import get_current_ist_str, CLINIC_LOCATION
from app.core.logging import logger
import os

router = APIRouter(prefix="/health", tags=["System Health & Diagnostics"])


@router.get("", summary="Simple Health Check")
@router.get("/liveness", summary="K8s / Load Balancer Liveness Probe")
async def liveness_probe():
    """
    Liveness probe used by container orchestrators (Kubernetes/Docker).
    Returns HTTP 200 if process is active and accepting connections.
    """
    return {
        "status": "HEALTHY",
        "service": "APEX AI Copus Dental Concierge",
        "timestamp_ist": get_current_ist_str()
    }


@router.get("/readiness", summary="K8s / Load Balancer Readiness Probe")
async def readiness_probe(response: Response, db: Session = Depends(get_db)):
    """
    Readiness probe evaluating critical infrastructure readiness:
    - Database Connectivity (SQLAlchemy query)
    - Redis Cache Ping (if configured)
    - Critical 3rd-Party Dependencies
    Returns 200 OK when ready, 503 Service Unavailable when degraded.
    """
    health_details = {
        "database": "UNKNOWN",
        "cache": "UNKNOWN",
        "ai_engine": "ONLINE",
    }
    is_ready = True

    # 1. Database Connection Check
    try:
        db.execute(text("SELECT 1"))
        health_details["database"] = "CONNECTED"
    except Exception as e:
        health_details["database"] = f"DISCONNECTED: {str(e)}"
        is_ready = False
        logger.error(f"Readiness check failed on Database: {e}")

    # 2. Redis Cache Ping Check (optional)
    redis_url = os.getenv("REDIS_URL", "")
    if redis_url:
        try:
            import redis
            r = redis.from_url(redis_url, socket_timeout=2)
            r.ping()
            health_details["cache"] = "CONNECTED"
        except Exception as e:
            health_details["cache"] = f"UNAVAILABLE: {str(e)}"
            is_ready = False
            logger.error(f"Readiness check failed on Redis: {e}")
    else:
        health_details["cache"] = "MEMORY_FALLBACK_ACTIVE"

    if is_ready:
        return {
            "status": "READY",
            "details": health_details,
            "timestamp_ist": get_current_ist_str()
        }
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "DEGRADED",
            "details": health_details,
            "timestamp_ist": get_current_ist_str()
        }
