# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Reception & Check-In Verification API Endpoints

from fastapi import APIRouter, HTTPException, status
from app.schemas.reception import (
    PaymentVerificationRequest,
    PaymentVerificationResponse,
    RosterResponse,
    DirectMessageRequest,
    CallbackConfirmRequest
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


@router.post("/direct-message", summary="Send a direct receptionist-to-patient message")
def send_reception_direct_message(request: DirectMessageRequest):
    """Logs a direct receptionist message to patient chat log."""
    return BookingService.send_direct_message(request.patient_id, request.message)


@router.post("/confirm-callback", summary="Confirm after-hours high-ticket callback request")
def confirm_after_hours_callback(request: CallbackConfirmRequest):
    """Confirms high-ticket callback and sets status to BOOKED_CONFIRMED."""
    try:
        return BookingService.confirm_callback(request.booking_id)
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ke).strip("'\"")
        )
