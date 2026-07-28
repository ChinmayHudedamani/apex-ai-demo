# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Doctor & Location Pydantic V2 Schemas

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class DoctorSchema(BaseModel):
    """Pydantic V2 schema representing doctor details and slot availability."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    degree: str
    exp: str
    specialty: str
    languages: str
    hours: str
    rating: str
    slots: List[str]


class DoctorListResponse(BaseModel):
    """Container schema for returning doctor listings."""
    total_count: int
    doctors: List[DoctorSchema]


class ClinicLocationSchema(BaseModel):
    """Pydantic V2 schema for clinic node location details."""
    branch: str
    address: str
    landmark: str
    map_url: str
    hours: str
    phone: str


class ClinicalServiceItem(BaseModel):
    """Pydantic V2 schema for detailed service directory entries."""
    id: str
    title: str
    badge: str
    badge_bg: str
    fee: str
    tiers: List[str]
    duration: str
    included: List[str]
    indications: str


class ClinicalServicesResponse(BaseModel):
    """Response schema containing formatted directory markdown & structured list."""
    directory_markdown: str
    services: List[ClinicalServiceItem]
