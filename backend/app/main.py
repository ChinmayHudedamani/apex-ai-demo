# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise FastAPI Application Initialization

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_v1_router
from app.core.config import get_current_ist_str, CLINIC_LOCATION

from app.db.session import engine
from app.models.pro_tier import Base
from app.services.doctor_status_engine import start_doctor_status_scheduler

# Create SQLite Database Tables on Startup
Base.metadata.create_all(bind=engine)

# FastAPI Application Factory
app = FastAPI(
    title="APEX AI — Copus Dental Concierge API",
    description="Enterprise Clean Architecture FastAPI backend for Apex Dental Clinic concierge platform.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware (Wildcard access during development for local React & web integrations)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API V1 Router
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


@app.get("/health", tags=["System Health & Info"])
def health_check():
    """Liveness health check endpoint."""
    return {
        "status": "HEALTHY",
        "timestamp_ist": get_current_ist_str()
    }
