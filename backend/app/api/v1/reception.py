# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Reception & Check-In Verification API Endpoints

from fastapi import APIRouter, HTTPException, status
from app.schemas.reception import (
    PaymentVerificationRequest,
    PaymentVerificationResponse,
    RosterResponse
)
from app.services.booking_service import BookingService

router = APIRouter(prefix="/reception", tags=["Reception & Desk Check-In"])


@router.get("/roster", response_model=RosterResponse, summary="Get today's waiting room roster")
def get_waiting_room_roster() -> RosterResponse:
    """Retrieves active patient roster and check-in statuses."""
    return BookingService.get_roster()


@router.post("/verify", response_model=PaymentVerificationResponse, summary="Verify patient check-in code & payment")
def verify_patient_payment(request: PaymentVerificationRequest) -> PaymentVerificationResponse:
    """Validates arriving patient's APX- check-in code and marks desk payment collected."""
    try:
        return BookingService.verify_payment(request)
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ke).strip("'\"")
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
