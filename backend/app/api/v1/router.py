# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — API v1 Router Aggregator

from fastapi import APIRouter
from app.api.v1.doctors import router as doctors_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.reception import router as reception_router
from app.api.v1.pro_tier import router as pro_tier_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(doctors_router)
api_v1_router.include_router(bookings_router)
api_v1_router.include_router(reception_router)
api_v1_router.include_router(pro_tier_router)
