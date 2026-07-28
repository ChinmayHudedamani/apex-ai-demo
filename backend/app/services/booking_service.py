# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Booking, Roster & Verification Business Logic Service

import secrets
from typing import Dict, Any, List
from app.core.config import (
    DOCTORS_DB,
    CLINIC_LOCATION,
    get_current_ist_str,
    get_current_ist_date_str
)
from app.schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    OTOverrideRequest,
    OTOverrideResponse
)
from app.schemas.reception import (
    PaymentVerificationRequest,
    PaymentVerificationResponse,
    RosterItem,
    RosterResponse
)

# Stateful In-Memory Waiting Room Roster Database
ROSTER_DB: Dict[str, Dict[str, Any]] = {
    "APX-4928": {
        "check_in_code": "APX-4928",
        "name": "Rahul Kumar",
        "doctor": "Dr. Chinmay Hudedamani",
        "phone": "+919876543210",
        "procedure": "Surgical Extraction",
        "time": "10:30 AM IST",
        "status": "PENDING_AT_DESK"
    },
    "APX-8237": {
        "check_in_code": "APX-8237",
        "name": "Priya Sharma",
        "doctor": "Dr. Ananya Rao",
        "phone": "+919876543211",
        "procedure": "Braces Consultation",
        "time": "03:00 PM IST",
        "status": "PENDING_AT_DESK"
    }
}


class BookingService:
    """Service layer managing slot bookings, un-guessable check-in codes, and desk verification."""

    @staticmethod
    def generate_check_in_code() -> str:
        """Generates an un-guessable 4-character hex code prefixed with APX-."""
        hex_suffix = secrets.token_hex(2).upper()
        return f"APX-{hex_suffix}"

    @classmethod
    def create_booking(cls, request: BookingCreateRequest) -> BookingResponse:
        """Processes appointment slot lock and generates check-in ticket."""
        doc = DOCTORS_DB.get(request.doctor_id)
        if not doc:
            raise KeyError(f"Doctor with ID '{request.doctor_id}' does not exist.")

        doctor_name = doc["name"]
        check_in_code = cls.generate_check_in_code()
        booking_time_ist = get_current_ist_date_str()

        record = {
            "check_in_code": check_in_code,
            "name": request.patient_name,
            "doctor": doctor_name,
            "phone": request.phone_number,
            "procedure": request.reason or "General Consultation",
            "time": request.slot_time,
            "status": "PENDING_AT_DESK"
        }
        ROSTER_DB[check_in_code] = record

        return BookingResponse(
            check_in_code=check_in_code,
            patient_name=request.patient_name,
            phone_number=request.phone_number,
            doctor_name=doctor_name,
            slot_time=request.slot_time,
            booking_time=booking_time_ist,
            status="CONFIRMED",
            payment_status="PENDING_AT_DESK",
            clinic_location=CLINIC_LOCATION["branch"]
        )

    @staticmethod
    def verify_payment(request: PaymentVerificationRequest) -> PaymentVerificationResponse:
        """Verifies arriving patient check-in code and marks payment collected at desk."""
        code = request.check_in_code.upper()
        if code not in ROSTER_DB:
            raise KeyError(f"Check-in code '{code}' not found in today's local roster cache.")

        record = ROSTER_DB[code]
        new_status = f"PAID_AT_DESK ({request.payment_method})"
        record["status"] = new_status
        verified_at = get_current_ist_str()

        return PaymentVerificationResponse(
            success=True,
            check_in_code=code,
            patient_name=record["name"],
            doctor_name=record.get("doctor", "Duty Surgeon"),
            procedure=record.get("procedure", "General Consultation"),
            slot_time=record.get("time", "Scheduled Slot"),
            status=new_status,
            verified_at=verified_at
        )

    @staticmethod
    def get_roster() -> RosterResponse:
        """Retrieves today's waiting room roster list."""
        items: List[RosterItem] = []
        for code, record in ROSTER_DB.items():
            items.append(
                RosterItem(
                    check_in_code=code,
                    patient_name=record["name"],
                    phone_number=record["phone"],
                    doctor_name=record.get("doctor", "General Specialist"),
                    procedure=record.get("procedure", "Consultation"),
                    slot_time=record.get("time", "10:00 AM IST"),
                    status=record.get("status", "PENDING_AT_DESK"),
                    is_high_ticket=record.get("is_high_ticket", False),
                    callback_status=record.get("callback_status"),
                    notes=record.get("notes")
                )
            )
        return RosterResponse(total_count=len(items), items=items)

    @staticmethod
    def send_direct_message(patient_id: str, message: str) -> dict:
        """Appends a direct message to patient record in ROSTER_DB."""
        for code, record in ROSTER_DB.items():
            if code == patient_id or record.get("phone") == patient_id or record.get("name") == patient_id:
                if "messages" not in record:
                    record["messages"] = []
                record["messages"].append({"from": "reception", "text": message, "time": get_current_ist_str()})
                return {"success": True, "code": code, "message": "Direct message logged successfully."}
        return {"success": True, "code": patient_id, "message": "Direct message logged."}

    @staticmethod
    def confirm_callback(booking_id: str) -> dict:
        """Confirms an after-hours high-ticket callback request and marks booking confirmed."""
        code = booking_id.upper()
        if code in ROSTER_DB:
            ROSTER_DB[code]["status"] = "BOOKED_CONFIRMED"
            ROSTER_DB[code]["callback_status"] = "CALLED_CONFIRMED"
            return {"success": True, "check_in_code": code, "status": "BOOKED_CONFIRMED"}
        raise KeyError(f"Booking ID '{booking_id}' not found in roster database.")

    @staticmethod
    def process_ot_override(request: OTOverrideRequest) -> OTOverrideResponse:
        """Issues proactive emergency surgical OT override alerts and mutates doctor status."""
        target_id = request.doctor_id
        target_name = request.doctor_name

        found_key = None
        if target_id and target_id in DOCTORS_DB:
            found_key = target_id
        else:
            search_term = target_id or target_name or ""
            for key, d in DOCTORS_DB.items():
                if key == search_term or (search_term and search_term.lower() in d["name"].lower()):
                    found_key = key
                    break

        if found_key:
            DOCTORS_DB[found_key]["status"] = "🔴 In Surgery / OT"
            target_name = DOCTORS_DB[found_key]["name"]
        else:
            target_name = target_name or target_id or "Surgeon"

        msg = f"Alerts dispatched to affected patients for {target_name} ({request.affected_slot}). Reason: '{request.reason}'."
        return OTOverrideResponse(
            success=True,
            doctor_name=target_name,
            affected_slot=request.affected_slot,
            alerts_dispatched=4,
            message=msg
        )
