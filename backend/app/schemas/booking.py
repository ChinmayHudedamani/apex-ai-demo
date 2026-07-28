# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Booking & OT Override Pydantic V2 Schemas with Field Validation

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BookingCreateRequest(BaseModel):
    """Request payload for locking an appointment slot."""
    model_config = ConfigDict(str_strip_whitespace=True)

    patient_name: str = Field(..., description="Full patient name (non-blank)")
    phone_number: str = Field(..., description="Mobile contact number (10-12 digits)")
    doctor_id: str = Field(..., description="Doctor identifier (e.g. DOC_1)")
    slot_time: str = Field(..., description="Chosen appointment slot time string")
    reason: Optional[str] = Field("General Consultation", description="Reason for clinical visit")

    @field_validator("patient_name")
    @classmethod
    def validate_patient_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Patient name cannot be blank or empty.")
        if len(cleaned) < 2:
            raise ValueError("Patient name must be at least 2 characters long.")
        return cleaned

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        # Strip spaces, hyphens, and optional leading +91
        raw_digits = re.sub(r"[^\d]", "", value)
        if value.startswith("+91") and len(raw_digits) == 12:
            digits = raw_digits[2:]
        elif value.startswith("91") and len(raw_digits) == 12:
            digits = raw_digits[2:]
        else:
            digits = raw_digits

        if not (10 <= len(digits) <= 12):
            raise ValueError(f"Phone number must contain between 10 and 12 digits. Provided: '{value}' ({len(digits)} digits)")
        return f"+91{digits[-10:]}"


class BookingResponse(BaseModel):
    """Response payload returned upon successfully locking an appointment."""
    model_config = ConfigDict(from_attributes=True)

    check_in_code: str = Field(..., description="Unique APX- prefixed check-in code")
    patient_name: str
    phone_number: str
    doctor_name: str
    slot_time: str
    booking_time: str
    status: str
    payment_status: str
    clinic_location: str

    @field_validator("check_in_code")
    @classmethod
    def validate_check_in_code(cls, value: str) -> str:
        if not value.startswith("APX-"):
            raise ValueError(f"Check-in code must start with 'APX-'. Provided: '{value}'")
        return value


class OTOverrideRequest(BaseModel):
    """Request payload for issuing an emergency surgical OT override."""
    model_config = ConfigDict(str_strip_whitespace=True)

    doctor_name: str = Field(..., description="Surgeon name affected by emergency override")
    affected_slot: str = Field(..., description="OT Slot string to clear")
    reason: str = Field(..., description="Clinical override reason")

    @field_validator("doctor_name", "affected_slot", "reason")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("OT Override fields cannot be blank or empty.")
        return cleaned


class OTOverrideResponse(BaseModel):
    """Response payload for OT override dispatch."""
    success: bool
    doctor_name: str
    affected_slot: str
    alerts_dispatched: int
    message: str
