# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Doctors & Clinical Services API Endpoints

from fastapi import APIRouter, HTTPException, status
from app.schemas.doctor import (
    DoctorSchema,
    DoctorListResponse,
    ClinicLocationSchema,
    ClinicalServicesResponse
)
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors & Clinic Directory"])


@router.get("", response_model=DoctorListResponse, summary="Get list of all dental specialists")
def list_doctors() -> DoctorListResponse:
    """Retrieve directory listing of all doctors and available slots."""
    doctors = DoctorService.get_all_doctors()
    return DoctorListResponse(total_count=len(doctors), doctors=doctors)


@router.get("/location", response_model=ClinicLocationSchema, summary="Get clinic location & map details")
def get_clinic_location() -> ClinicLocationSchema:
    """Retrieve clinic node branch, address, hours, and map link."""
    return DoctorService.get_clinic_location()


@router.get("/services", response_model=ClinicalServicesResponse, summary="Get Clinical Service & Fee Directory")
def get_clinical_services() -> ClinicalServicesResponse:
    """Retrieve structured clinical procedure fees, duration, included diagnostics, and badges."""
    return DoctorService.get_clinical_services()


@router.get("/{doc_id}", response_model=DoctorSchema, summary="Get doctor details by ID")
def get_doctor_by_id(doc_id: str) -> DoctorSchema:
    """Retrieve single doctor profile by ID (e.g. DOC_1)."""
    doctor = DoctorService.get_doctor_by_id(doc_id.upper())
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID '{doc_id}' not found."
        )
    return doctor
