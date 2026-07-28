# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Doctor & Schedule Directory Business Logic Service

from typing import List, Optional
from app.core.config import (
    DOCTORS_DB,
    CLINIC_LOCATION,
    CLINICAL_SERVICES_DIRECTORY,
    CLINICAL_SERVICES_DATA
)
from app.schemas.doctor import (
    DoctorSchema,
    ClinicLocationSchema,
    ClinicalServiceItem,
    ClinicalServicesResponse
)


class DoctorService:
    """Encapsulates read operations and business logic for doctor and clinic metadata."""

    @staticmethod
    def get_all_doctors() -> List[DoctorSchema]:
        """Returns all configured dental specialists."""
        return [DoctorSchema(**doc_data) for doc_data in DOCTORS_DB.values()]

    @staticmethod
    def get_doctor_by_id(doc_id: str) -> Optional[DoctorSchema]:
        """Retrieves a single doctor by key ID (e.g. DOC_1)."""
        doc_data = DOCTORS_DB.get(doc_id)
        if not doc_data:
            return None
        return DoctorSchema(**doc_data)

    @staticmethod
    def get_clinic_location() -> ClinicLocationSchema:
        """Returns clinic node address, timings, and map URL metadata."""
        return ClinicLocationSchema(**CLINIC_LOCATION)

    @staticmethod
    def get_clinical_services() -> ClinicalServicesResponse:
        """Returns formatted Clinical Directory markdown text and structured procedure data."""
        services = [ClinicalServiceItem(**item) for item in CLINICAL_SERVICES_DATA]
        return ClinicalServicesResponse(
            directory_markdown=CLINICAL_SERVICES_DIRECTORY,
            services=services
        )
