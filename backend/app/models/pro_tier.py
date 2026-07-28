# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Pro Tier SQLAlchemy Models

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class HighTicketLead(Base):
    __tablename__ = "high_ticket_leads"

    id = Column(String(50), primary_key=True)  # e.g. HT-9821
    patient_name = Column(String(100), nullable=False)
    patient_phone = Column(String(15), nullable=False)
    service_name = Column(String(150), nullable=False)  # e.g. Clear Aligners / Microscopic RCT
    estimated_value = Column(Float, nullable=False)  # e.g. 15000.0
    requested_slot = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default="PENDING_MORNING_CALLBACK")  # PENDING_MORNING_CALLBACK, LOCKED, CANCELLED
    notes = Column(Text, nullable=True)


class DoctorStatusLog(Base):
    __tablename__ = "doctor_status_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(String(50), nullable=False)
    doctor_name = Column(String(100), nullable=False)
    current_status = Column(String(50), nullable=False)  # AVAILABLE, IN_SURGERY, ON_BREAK, OFF_DUTY
    est_completion_mins = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)


class ClinicSettings(Base):
    __tablename__ = "clinic_settings"

    id = Column(Integer, primary_key=True, default=1)
    clinic_name = Column(String(100), default="Apex Dental Center - Yelahanka")
    reception_email = Column(String(100), default="reception.apex@gmail.com")
    reception_whatsapp = Column(String(20), default="+919876543210")
