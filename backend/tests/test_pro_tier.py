# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Pro Tier Automated Integration Tests

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_high_ticket_leads():
    """Test fetching high-ticket leads list."""
    response = client.get("/api/v1/pro-tier/leads")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "patient_name" in data[0]
    assert "estimated_value" in data[0]


def test_create_and_confirm_high_ticket_lead():
    """Test creating a new high-ticket lead and marking callback confirmed."""
    payload = {
        "patient_name": "Test Patient",
        "patient_phone": "9876543999",
        "service_name": "Full Arch Dental Implants",
        "estimated_value": 120000.0,
        "requested_slot": "11:00 AM IST",
        "notes": "Interested in single-sitting protocol."
    }
    create_res = client.post("/api/v1/pro-tier/leads", json=payload)
    assert create_res.status_code == 201
    lead_data = create_res.json()
    assert lead_data["patient_name"] == "Test Patient"
    assert lead_data["status"] == "PENDING_MORNING_CALLBACK"
    lead_id = lead_data["id"]

    confirm_res = client.post(f"/api/v1/pro-tier/leads/{lead_id}/confirm")
    assert confirm_res.status_code == 200
    confirm_data = confirm_res.json()
    assert confirm_data["success"] is True
    assert confirm_data["status"] == "LOCKED"


def test_doctor_status_and_15min_cycle():
    """Test 15-minute doctor status retrieval, manual status update, and cycle trigger."""
    status_res = client.get("/api/v1/pro-tier/doctor-status")
    assert status_res.status_code == 200
    docs = status_res.json()["doctors"]
    assert len(docs) >= 3

    # Manual update doctor status
    update_res = client.post(
        "/api/v1/pro-tier/doctor-status/update",
        json={"doctor_id": "dr-ananya", "status": "IN_SURGERY", "est_completion_mins": 30}
    )
    assert update_res.status_code == 200
    assert update_res.json()["doctor"]["est_completion_mins"] == 30

    # Trigger 15-minute countdown cycle
    cycle_res = client.post("/api/v1/pro-tier/doctor-status/trigger-15min-cycle")
    assert cycle_res.status_code == 200
    updated_docs = cycle_res.json()["doctors"]
    ananya_doc = next(d for d in updated_docs if d["id"] == "dr-ananya")
    assert ananya_doc["est_completion_mins"] == 15


def test_morning_pdf_digest_generation():
    """Test generating and downloading ReportLab morning PDF digest binary content."""
    pdf_res = client.get("/api/v1/pro-tier/morning-digest/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert pdf_res.content.startswith(b"%PDF-")
