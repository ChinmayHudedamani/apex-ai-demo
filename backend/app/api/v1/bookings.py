# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Booking & OT Emergency Override API Endpoints

from fastapi import APIRouter, HTTPException, status
from app.schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    OTOverrideRequest,
    OTOverrideResponse
)
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings & Schedule Management"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, summary="Create appointment slot lock")
def create_booking(request: BookingCreateRequest) -> BookingResponse:
    """Creates appointment booking, generates un-guessable APX- check-in code, and registers in roster."""
    try:
        return BookingService.create_booking(request)
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ke).strip("'\"")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/ot-override", response_model=OTOverrideResponse, summary="Issue OT Emergency Schedule Override")
def ot_override(request: OTOverrideRequest) -> OTOverrideResponse:
    """Dispatches emergency schedule override alerts for surgical interventions."""
    try:
        return BookingService.process_ot_override(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
