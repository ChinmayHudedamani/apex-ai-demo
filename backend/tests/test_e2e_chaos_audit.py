# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# End-to-End System Integration Test & Chaos Audit Suite

import sys
from pathlib import Path
from fastapi.testclient import TestClient

backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

client = TestClient(app)


def test_scenario_1_full_patient_to_receptionist_flow():
    """Scenario 1: Complete booking in patient view -> appears in roster -> verified by receptionist with UPI payment."""
    # Step 1: Create booking for Dr. Chinmay Hudedamani (DOC_1)
    booking_payload = {
        "patient_name": "Karthik Subramanian",
        "phone_number": "9876543210",
        "doctor_id": "DOC_1",
        "slot_time": "10:00 AM IST",
        "reason": "Micro-Endodontic Root Canal Evaluation"
    }
    booking_res = client.post("/api/v1/bookings", json=booking_payload)
    assert booking_res.status_code == 201, f"Booking failed: {booking_res.text}"
    booking_data = booking_res.json()
    check_in_code = booking_data["check_in_code"]
    assert check_in_code.startswith("APX-")

    # Step 2: Verify immediate appearance under waiting room roster as PENDING_AT_DESK
    roster_res = client.get("/api/v1/reception/roster")
    assert roster_res.status_code == 200
    roster_items = roster_res.json()["items"]
    patient_record = next((item for item in roster_items if item["check_in_code"] == check_in_code), None)
    assert patient_record is not None, f"Code {check_in_code} not found in roster"
    assert patient_record["status"] == "PENDING_AT_DESK"

    # Step 3: Receptionist enters check-in code and selects "UPI (GPay/PhonePe)"
    verify_payload = {
        "check_in_code": check_in_code.lower(),  # Verify auto-cleansing/normalization
        "payment_method": "UPI (GPay/PhonePe)"
    }
    verify_res = client.post("/api/v1/reception/verify", json=verify_payload)
    assert verify_res.status_code == 200, f"Verification failed: {verify_res.text}"
    verify_data = verify_res.json()
    assert verify_data["success"] is True
    assert "PAID_AT_DESK" in verify_data["status"]

    # Step 4: Re-query roster and confirm status badge updated to PAID_AT_DESK (UPI)
    roster_res_after = client.get("/api/v1/reception/roster")
    assert roster_res_after.status_code == 200
    updated_record = next((item for item in roster_res_after.json()["items"] if item["check_in_code"] == check_in_code), None)
    assert updated_record is not None
    assert updated_record["status"] == "PAID_AT_DESK (UPI (GPay/PhonePe))"


def test_scenario_2_doctor_emergency_override_state_propagation():
    """Scenario 2: Trigger OT Override in Command Center -> State propagates to Doctor directory view."""
    # Step 1: Trigger OT Emergency Override for DOC_1
    override_payload = {
        "doctor_id": "DOC_1",
        "doctor_name": "Dr. Chinmay Hudedamani",
        "affected_slot": "11:30 AM – 01:00 PM IST",
        "reason": "Acute Surgical Emergency Intervention"
    }
    override_res = client.post("/api/v1/bookings/ot-override", json=override_payload)
    assert override_res.status_code == 200, f"OT Override failed: {override_res.text}"
    assert override_res.json()["success"] is True

    # Step 2: Query single doctor details for DOC_1
    doc_res = client.get("/api/v1/doctors/DOC_1")
    assert doc_res.status_code == 200
    doc_data = doc_res.json()
    assert doc_data["status"] == "🔴 In Surgery / OT"

    # Step 3: Query all doctors list and verify DOC_1 reflects status mutation
    all_docs_res = client.get("/api/v1/doctors")
    assert all_docs_res.status_code == 200
    doc_1_item = next((d for d in all_docs_res.json()["doctors"] if d["id"] == "DOC_1"), None)
    assert doc_1_item is not None
    assert doc_1_item["status"] == "🔴 In Surgery / OT"


def test_scenario_3_multi_tier_validation_and_resilience():
    """Scenario 3: Validate schema edge cases and unexpected input resiliency."""
    # 1. Blank patient name fails with HTTP 422
    invalid_name_res = client.post("/api/v1/bookings", json={
        "patient_name": "   ",
        "phone_number": "9876543210",
        "doctor_id": "DOC_1",
        "slot_time": "10:00 AM IST"
    })
    assert invalid_name_res.status_code == 422

    # 2. Invalid phone number fails with HTTP 422
    invalid_phone_res = client.post("/api/v1/bookings", json={
        "patient_name": "Valid Name",
        "phone_number": "invalid-phone",
        "doctor_id": "DOC_1",
        "slot_time": "10:00 AM IST"
    })
    assert invalid_phone_res.status_code == 422

    # 3. Non-existent check-in code verification fails with HTTP 404
    invalid_code_res = client.post("/api/v1/reception/verify", json={
        "check_in_code": "APX-0000",
        "payment_method": "Cash"
    })
    assert invalid_code_res.status_code == 404
