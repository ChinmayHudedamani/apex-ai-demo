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
        if not re.match(r"^[a-zA-Z\s]{2,50}$", cleaned):
            raise ValueError("Enter a valid name (letters only, min 2 characters).")
        return cleaned

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        cleaned = value.strip()
        digits = cleaned[3:].strip() if cleaned.startswith("+91") else cleaned.strip()
        if not re.match(r"^[6-9]\d{9}$", digits):
            raise ValueError("Enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.")
        return f"+91{digits}"


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

    doctor_id: Optional[str] = Field(None, description="Surgeon ID (e.g. DOC_1)")
    doctor_name: Optional[str] = Field(None, description="Surgeon name affected by emergency override")
    affected_slot: str = Field(..., description="OT Slot string to clear")
    reason: str = Field(..., description="Clinical override reason")

    @field_validator("affected_slot", "reason")
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
