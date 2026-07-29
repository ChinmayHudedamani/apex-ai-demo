# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise FastAPI Application Initialization

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_v1_router
from app.api.v1.health import router as health_router
from app.core.config import get_current_ist_str, CLINIC_LOCATION

from app.db.session import engine
from app.models.pro_tier import Base
from app.models.security_audit import SecurityAuditLog
from app.services.doctor_status_engine import start_doctor_status_scheduler
from app.middleware.firewall import SecurityFirewallMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.correlation import CorrelationIdMiddleware
from app.middleware.error_handler import global_exception_handler
from app.core.telemetry import init_telemetry

# Create SQLite Database Tables on Startup
Base.metadata.create_all(bind=engine)

# Initialize Sentry Telemetry SDK
init_telemetry()

# FastAPI Application Factory
app = FastAPI(
    title="APEX AI — Copus Dental Concierge API",
    description="Enterprise Production-Hardened FastAPI backend for Apex Dental Clinic concierge platform.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Register Global Exception Handler
app.add_exception_handler(Exception, global_exception_handler)

# Register Middlewares (Order: Correlation -> Headers -> Firewall -> CORS)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SecurityFirewallMiddleware, rate_limit_per_minute=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "https://localhost:8081",
        "https://apex-ai-demo.loca.lt",
        "https://apex-ai-backend.loca.lt",
        "*",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Top-Level & V1 Routers
app.include_router(health_router)
app.include_router(api_v1_router)


@app.on_event("startup")
def startup_event():
    start_doctor_status_scheduler()


@app.get("/", tags=["System Health & Info"])
def root_info():
    """Root endpoint returning service identity, IST timestamp, and status."""
    return {
        "service": "APEX AI Copus Dental Concierge API",
        "status": "ONLINE",
        "node": CLINIC_LOCATION["branch"],
        "timestamp_ist": get_current_ist_str(),
        "docs": "/docs"
    }
