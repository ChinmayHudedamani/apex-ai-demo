# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise Backend API Stress & Edge Case Test Suite

import sys
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure backend directory is in sys.path
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

client = TestClient(app)


# ==============================================================================
# 1. SCHEMA INVALIDATION ATTACKS
# ==============================================================================

def test_booking_whitespace_patient_name_fails():
    """Attempt booking with whitespace-only patient name -> Expect HTTP 422."""
    payload = {
        "patient_name": "     ",
        "phone_number": "9876543210",
        "doctor_id": "DOC_1",
        "slot_time": "10:00 AM IST",
        "reason": "Routine Checkup"
    }
    response = client.post("/api/v1/bookings", json=payload)
    assert response.status_code == 422, f"Expected 422 Unprocessable Entity, got {response.status_code}: {response.text}"


def test_booking_malformed_phone_number_fails():
    """Attempt booking with malformed phone number ('abc-12') -> Expect HTTP 422."""
    payload = {
        "patient_name": "Rahul Sharma",
        "phone_number": "abc-12",
        "doctor_id": "DOC_1",
        "slot_time": "11:30 AM IST",
        "reason": "Scaling"
    }
    response = client.post("/api/v1/bookings", json=payload)
    assert response.status_code == 422, f"Expected 422 Unprocessable Entity, got {response.status_code}: {response.text}"


def test_booking_non_existent_doctor_id_fails():
    """Attempt booking with non-existent doctor_id ('DOC_999') -> Expect HTTP 404."""
    payload = {
        "patient_name": "Priya Singh",
        "phone_number": "9876543210",
        "doctor_id": "DOC_999",
        "slot_time": "01:00 PM IST",
        "reason": "Consultation"
    }
    response = client.post("/api/v1/bookings", json=payload)
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}: {response.text}"


# ==============================================================================
# 2. VERIFICATION RESILIENCE
# ==============================================================================

def test_verification_messy_lowercase_code_normalizes_success():
    """Verify lowercase messy check-in code ('  apx-4928 ') -> Must auto-cleanse, normalize, and return HTTP 200."""
    payload = {
        "check_in_code": "  apx-4928 ",
        "payment_method": "Cash"
    }
    response = client.post("/api/v1/reception/verify", json=payload)
    assert response.status_code == 200, f"Expected 200 OK for normalized code, got {response.status_code}: {response.text}"
    data = response.json()
    assert data["success"] is True
    assert data["check_in_code"] == "APX-4928"
    assert "PAID_AT_DESK" in data["status"]


def test_verification_invalid_prefix_fails():
    """Verify invalid code prefix ('INVALID123') -> Expect HTTP 422."""
    payload = {
        "check_in_code": "INVALID123",
        "payment_method": "UPI"
    }
    response = client.post("/api/v1/reception/verify", json=payload)
    assert response.status_code == 422, f"Expected 422 Unprocessable Entity, got {response.status_code}: {response.text}"


def test_verification_code_not_in_roster_fails():
    """Verify code that doesn't exist in roster ('APX-9999') -> Expect HTTP 404."""
    payload = {
        "check_in_code": "APX-9999",
        "payment_method": "Credit/Debit Card"
    }
    response = client.post("/api/v1/reception/verify", json=payload)
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}: {response.text}"


# ==============================================================================
# 3. ROSTER STATE MUTATIONS
# ==============================================================================

def test_booking_creation_and_payment_roster_mutations():
    """Ensure a successful booking instantly appears in roster and payment updates status."""
    # 1. Create a fresh booking
    booking_payload = {
        "patient_name": "Ananya Hegde",
        "phone_number": "9123456789",
        "doctor_id": "DOC_2",
        "slot_time": "04:30 PM IST",
        "reason": "Clear Aligners Consultation"
    }
    booking_res = client.post("/api/v1/bookings", json=booking_payload)
    assert booking_res.status_code == 201, f"Booking failed: {booking_res.text}"
    booking_data = booking_res.json()
    check_in_code = booking_data["check_in_code"]
    assert check_in_code.startswith("APX-")

    # 2. Check roster contains the new booking
    roster_res1 = client.get("/api/v1/reception/roster")
    assert roster_res1.status_code == 200
    roster_items1 = roster_res1.json()["items"]
    matched_items1 = [item for item in roster_items1 if item["check_in_code"] == check_in_code]
    assert len(matched_items1) == 1
    assert matched_items1[0]["status"] == "PENDING_AT_DESK"

    # 3. Verify payment at desk
    verify_payload = {
        "check_in_code": check_in_code,
        "payment_method": "UPI (GPay/PhonePe)"
    }
    verify_res = client.post("/api/v1/reception/verify", json=verify_payload)
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "PAID_AT_DESK (UPI (GPay/PhonePe))"

    # 4. Check roster reflects updated status
    roster_res2 = client.get("/api/v1/reception/roster")
    assert roster_res2.status_code == 200
    roster_items2 = roster_res2.json()["items"]
    matched_items2 = [item for item in roster_items2 if item["check_in_code"] == check_in_code]
    assert len(matched_items2) == 1
    assert matched_items2[0]["status"] == "PAID_AT_DESK (UPI (GPay/PhonePe))"


# ==============================================================================
# 4. OT EMERGENCY OVERRIDE
# ==============================================================================

def test_ot_emergency_override_mutates_doctor_status():
    """Trigger OT override for DOC_1 -> Verify doctor status updates to '🔴 In Surgery / OT'."""
    override_payload = {
        "doctor_id": "DOC_1",
        "doctor_name": "Dr. Chinmay Hudedamani",
        "affected_slot": "11:30 AM – 01:00 PM IST",
        "reason": "Acute Surgical Emergency Intervention"
    }
    override_res = client.post("/api/v1/bookings/ot-override", json=override_payload)
    assert override_res.status_code == 200, f"OT Override failed: {override_res.text}"
    override_data = override_res.json()
    assert override_data["success"] is True

    # Verify doctor profile reflects status mutation
    doc_res = client.get("/api/v1/doctors/DOC_1")
    assert doc_res.status_code == 200
    doc_data = doc_res.json()
    assert doc_data["status"] == "🔴 In Surgery / OT"
