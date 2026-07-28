# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Pro Tier API Routes

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.pro_tier import HighTicketLead, DoctorStatusLog, ClinicSettings
from app.services.pdf_digest_service import generate_morning_pdf_digest
from app.services.doctor_status_engine import (
    get_all_doctor_statuses,
    update_doctor_status_manually,
    run_15min_status_update,
)

router = APIRouter(prefix="/pro-tier", tags=["Pro Tier SaaS"])


# Pydantic Schemas
class HighTicketLeadCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=100)
    patient_phone: str = Field(..., pattern=r"^[6-9]\d{9}$")
    service_name: str = Field(..., min_length=2)
    estimated_value: float = Field(..., gt=0)
    requested_slot: str = Field(...)
    notes: Optional[str] = None


class HighTicketLeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_name: str
    patient_phone: str
    service_name: str
    estimated_value: float
    requested_slot: str
    created_at: datetime
    status: str
    notes: Optional[str] = None


class DoctorStatusUpdatePayload(BaseModel):
    doctor_id: str
    status: str  # AVAILABLE, IN_SURGERY, ON_BREAK, OFF_DUTY
    est_completion_mins: int = 0


@router.get("/leads", response_model=List[HighTicketLeadResponse])
def get_high_ticket_leads(db: Session = Depends(get_db)):
    """Fetch all high-ticket leads requiring morning callback or locked."""
    leads = db.query(HighTicketLead).order_by(HighTicketLead.created_at.desc()).all()
    if not leads:
        # Seed default sample leads if table empty for seamless demo
        sample_leads = [
            HighTicketLead(id="HT-9821", patient_name="Rahul Kumar", patient_phone="9876543210", service_name="Invisible Aligners", estimated_value=45000.0, requested_slot="10:00 AM IST", status="PENDING_MORNING_CALLBACK"),
            HighTicketLead(id="HT-9822", patient_name="Priya Sharma", patient_phone="9876543211", service_name="Microscopic RCT", estimated_value=6500.0, requested_slot="11:30 AM IST", status="PENDING_MORNING_CALLBACK"),
            HighTicketLead(id="HT-9823", patient_name="Vikram Sen", patient_phone="9876543212", service_name="Teeth-in-a-Day Implant", estimated_value=85000.0, requested_slot="02:00 PM IST", status="PENDING_MORNING_CALLBACK"),
        ]
        db.add_all(sample_leads)
        db.commit()
        leads = db.query(HighTicketLead).order_by(HighTicketLead.created_at.desc()).all()
    return leads


@router.post("/leads", response_model=HighTicketLeadResponse, status_code=status.HTTP_201_CREATED)
def create_high_ticket_lead(payload: HighTicketLeadCreate, db: Session = Depends(get_db)):
    """Log new high-ticket lead during after-hours mode."""
    lead_id = f"HT-{datetime.utcnow().strftime('%M%S')}"
    new_lead = HighTicketLead(
        id=lead_id,
        patient_name=payload.patient_name,
        patient_phone=payload.patient_phone,
        service_name=payload.service_name,
        estimated_value=payload.estimated_value,
        requested_slot=payload.requested_slot,
        status="PENDING_MORNING_CALLBACK",
        notes=payload.notes
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead


@router.post("/leads/{lead_id}/confirm")
def confirm_high_ticket_lead(lead_id: str, db: Session = Depends(get_db)):
    """Confirm morning callback and lock slot for high-ticket lead."""
    lead = db.query(HighTicketLead).filter(HighTicketLead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail=f"Lead ID {lead_id} not found")
    lead.status = "LOCKED"
    db.commit()
    return {"success": True, "id": lead_id, "status": "LOCKED", "message": f"Lead {lead_id} marked called and slot locked."}


@router.get("/doctor-status")
def get_doctor_statuses():
    """Retrieve 15-minute dynamic doctor status list."""
    return {"doctors": get_all_doctor_statuses()}


@router.post("/doctor-status/update")
def update_doctor_status(payload: DoctorStatusUpdatePayload):
    """Manually update doctor status or trigger surgery countdown."""
    updated = update_doctor_status_manually(payload.doctor_id, payload.status, payload.est_completion_mins)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Doctor ID {payload.doctor_id} not found")
    return {"success": True, "doctor": updated}


@router.post("/doctor-status/trigger-15min-cycle")
def trigger_15min_cycle():
    """Manually trigger the 15-minute countdown cycle for demo testing."""
    run_15min_status_update()
    return {"success": True, "doctors": get_all_doctor_statuses()}


@router.get("/morning-digest/pdf")
def get_morning_pdf_digest(db: Session = Depends(get_db)):
    """Generate and return official 08:30 AM Morning Reception PDF Digest."""
    leads = db.query(HighTicketLead).all()
    lead_dicts = [
        {
            "id": l.id,
            "patient_name": l.patient_name,
            "patient_phone": f"+91{l.patient_phone}",
            "service_name": l.service_name,
            "estimated_value": l.estimated_value,
            "requested_slot": l.requested_slot,
        }
        for l in leads
    ]
    doctors = get_all_doctor_statuses()
    doc_dicts = [
        {
            "doctor_name": d["name"],
            "current_status": d["status"],
            "est_completion_mins": d["est_completion_mins"],
        }
        for d in doctors
    ]

    pdf_bytes = generate_morning_pdf_digest(high_ticket_leads=lead_dicts, doctor_statuses=doc_dicts)
    filename = f"Morning_Concierge_Digest_{datetime.now().strftime('%Y%m%d')}.pdf"
    headers = {"Content-Disposition": f"inline; filename={filename}"}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
