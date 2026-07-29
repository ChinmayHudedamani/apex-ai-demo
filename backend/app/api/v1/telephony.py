# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Telephony & Live Call Simulator Router

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

router = APIRouter(prefix="/telephony", tags=["Telephony & Call Simulation"])

# In-memory demo state store (persists for demo duration)
DEMO_STATE: Dict = {
    "clinic_name": "Conus Clinic",
    "receptionist_status": "ONLINE",  # "ONLINE" or "OFFLINE"
    "active_call": None,  # None or dict with call info
    "call_logs": [],
    "chat_messages": []
}


class InitiateCallRequest(BaseModel):
    caller_name: str = Field(default="Rahul Sharma")
    caller_phone: str = Field(default="+919876543210")
    call_type: str = Field(default="CELLULAR")  # "CELLULAR" or "WHATSAPP"


class CallActionRequest(BaseModel):
    call_id: str
    action: str  # "ANSWER", "DECLINE", "TIMEOUT"


@router.get("/state")
async def get_telephony_state():
    """Returns real-time call state, presence status, and simulated chat logs."""
    return DEMO_STATE


@router.post("/toggle-presence")
async def toggle_presence(status: str):
    """Toggles Receptionist status between ONLINE and OFFLINE."""
    clean_status = status.upper().strip()
    if clean_status in ["ONLINE", "OFFLINE"]:
        DEMO_STATE["receptionist_status"] = clean_status
        return {"status": "SUCCESS", "receptionist_status": DEMO_STATE["receptionist_status"]}
    raise HTTPException(status_code=400, detail="Status must be ONLINE or OFFLINE")


@router.post("/simulate-incoming-call")
async def simulate_incoming_call(req: InitiateCallRequest):
    """Simulates a patient calling the clinic line."""
    call_id = f"CALL-{int(datetime.now().timestamp())}"
    call_data = {
        "call_id": call_id,
        "caller_name": req.caller_name,
        "caller_phone": req.caller_phone,
        "call_type": req.call_type,
        "status": "RINGING",
        "started_at": datetime.now().strftime("%I:%M:%S %p")
    }
    DEMO_STATE["active_call"] = call_data
    return {"status": "RINGING", "call": call_data}


@router.post("/handle-call-action")
async def handle_call_action(req: CallActionRequest):
    """Processes Receptionist response (Answer, Decline, or Timeout)."""
    active_call = DEMO_STATE.get("active_call")
    if not active_call or active_call["call_id"] != req.call_id:
        # Fallback if call was already processed
        return {"status": "PROCESSED", "message": "Call action recorded."}

    action_upper = req.action.upper().strip()

    if action_upper == "ANSWER":
        active_call["status"] = "CONNECTED"
        DEMO_STATE["call_logs"].append(active_call)
        DEMO_STATE["active_call"] = None
        return {"status": "CONNECTED", "message": "Call answered by receptionist."}

    elif action_upper in ["DECLINE", "TIMEOUT"]:
        active_call["status"] = "MISSED"
        DEMO_STATE["call_logs"].append(active_call)
        DEMO_STATE["active_call"] = None

        # Determine auto-reply message based on Receptionist presence
        is_online = DEMO_STATE["receptionist_status"] == "ONLINE"
        clinic_name = DEMO_STATE["clinic_name"]

        if is_online:
            auto_reply = "How can I help you?"
        else:
            auto_reply = f"Hello, I am {clinic_name}'s assistant. How may I help you?"

        # Append auto-response to chat stream
        msg_payload = {
            "id": f"MSG-{int(datetime.now().timestamp())}",
            "sender": "BOT",
            "text": auto_reply,
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "trigger": f"MISSED_CALL ({action_upper})"
        }
        DEMO_STATE["chat_messages"].append(msg_payload)

        return {
            "status": "MISSED",
            "auto_reply_sent": auto_reply,
            "receptionist_was_online": is_online
        }

    raise HTTPException(status_code=400, detail="Invalid action. Must be ANSWER, DECLINE, or TIMEOUT.")
