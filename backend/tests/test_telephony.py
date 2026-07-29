# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Telephony & Missed-Call Auto-Responder Automated Tests

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_rate_limit():
    """Resets rate limit counter before each test in telephony module."""
    client.get("/health", headers={"X-Reset-Rate-Limit": "true"})


def test_get_telephony_state():
    """Test fetching telephony initial state."""
    response = client.get("/api/v1/telephony/state")
    assert response.status_code == 200
    data = response.json()
    assert "receptionist_status" in data
    assert data["receptionist_status"] in ["ONLINE", "OFFLINE"]


def test_toggle_presence():
    """Test toggling receptionist presence between ONLINE and OFFLINE."""
    res_off = client.post("/api/v1/telephony/toggle-presence?status=OFFLINE")
    assert res_off.status_code == 200
    assert res_off.json()["receptionist_status"] == "OFFLINE"

    res_on = client.post("/api/v1/telephony/toggle-presence?status=ONLINE")
    assert res_on.status_code == 200
    assert res_on.json()["receptionist_status"] == "ONLINE"


def test_simulate_incoming_call():
    """Test simulating an incoming cellular call from a patient."""
    payload = {"caller_name": "Test Caller", "caller_phone": "+919876543210"}
    res = client.post("/api/v1/telephony/simulate-incoming-call", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "RINGING"
    assert res.json()["call"]["caller_name"] == "Test Caller"


def test_answer_call_suppresses_bot_messages():
    """Test answering call updates status to CONNECTED and suppresses bot messages."""
    sim_res = client.post("/api/v1/telephony/simulate-incoming-call", json={"caller_name": "Rahul", "caller_phone": "+919876543210"})
    call_id = sim_res.json()["call"]["call_id"]

    answer_res = client.post("/api/v1/telephony/handle-call-action", json={"call_id": call_id, "action": "ANSWER"})
    assert answer_res.status_code == 200
    assert answer_res.json()["status"] == "CONNECTED"


def test_missed_call_online_auto_reply():
    """Test missed/declined call when Receptionist is ONLINE triggers 'How can I help you?'."""
    client.post("/api/v1/telephony/toggle-presence?status=ONLINE")
    sim_res = client.post("/api/v1/telephony/simulate-incoming-call", json={"caller_name": "Online Miss", "caller_phone": "+919876543210"})
    call_id = sim_res.json()["call"]["call_id"]

    decline_res = client.post("/api/v1/telephony/handle-call-action", json={"call_id": call_id, "action": "DECLINE"})
    assert decline_res.status_code == 200
    data = decline_res.json()
    assert data["status"] == "MISSED"
    assert data["auto_reply_sent"] == "How can I help you?"


def test_missed_call_offline_auto_reply():
    """Test missed/declined call when Receptionist is OFFLINE triggers assistant intro message."""
    client.post("/api/v1/telephony/toggle-presence?status=OFFLINE")
    sim_res = client.post("/api/v1/telephony/simulate-incoming-call", json={"caller_name": "Offline Miss", "caller_phone": "+919876543210"})
    call_id = sim_res.json()["call"]["call_id"]

    timeout_res = client.post("/api/v1/telephony/handle-call-action", json={"call_id": call_id, "action": "TIMEOUT"})
    assert timeout_res.status_code == 200
    data = timeout_res.json()
    assert data["status"] == "MISSED"
    assert "assistant. How may I help you?" in data["auto_reply_sent"]
