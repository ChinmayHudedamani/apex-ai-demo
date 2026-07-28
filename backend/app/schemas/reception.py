# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Reception & Verification Pydantic V2 Schemas

from typing import List, Set
from pydantic import BaseModel, Field, field_validator, ConfigDict

ALLOWED_PAYMENT_METHODS: Set[str] = {
    "Cash",
    "UPI",
    "Credit/Debit Card",
    "Credit / Debit Card",
    "UPI (GPay/PhonePe)",
    "UPI (GPay / PhonePe)",
    "Credit Card",
    "Debit Card",
    "Direct Zero-Cost EMI"
}


class PaymentVerificationRequest(BaseModel):
    """Payload sent by receptionist to verify arrival and record desk payment."""
    model_config = ConfigDict(str_strip_whitespace=True)

    check_in_code: str = Field(..., description="Check-in code formatted as APX-XXXX")
    payment_method: str = Field(..., description="Method of payment collected at desk")

    @field_validator("check_in_code")
    @classmethod
    def validate_code_prefix(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if not cleaned.startswith("APX-"):
            raise ValueError(f"Check-in code must start with 'APX-'. Provided: '{value}'")
        return cleaned

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value: str) -> str:
        cleaned = value.strip()
        normalized = cleaned.replace(" / ", "/")
        if cleaned in ALLOWED_PAYMENT_METHODS or normalized in ALLOWED_PAYMENT_METHODS:
            return cleaned

        raise ValueError(
            f"Invalid payment method '{cleaned}'. Allowed options: {sorted(list(ALLOWED_PAYMENT_METHODS))}"
        )


class PaymentVerificationResponse(BaseModel):
    """Response returned upon successful payment verification."""
    success: bool
    check_in_code: str
    patient_name: str
    doctor_name: str
    procedure: str
    slot_time: str
    status: str
    verified_at: str

    @field_validator("check_in_code")
    @classmethod
    def validate_check_in_code(cls, value: str) -> str:
        if not value.startswith("APX-"):
            raise ValueError(f"Check-in code must start with 'APX-'. Provided: '{value}'")
        return value


class RosterItem(BaseModel):
    """Pydantic V2 schema representing a patient check-in record in today's roster."""
    check_in_code: str
    patient_name: str
    phone_number: str
    doctor_name: str
    procedure: str
    slot_time: str
    status: str


class RosterResponse(BaseModel):
    """Container schema for returning the active waiting room roster."""
    total_count: int
    items: List[RosterItem]
