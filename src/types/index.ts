// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// APEX AI / Copus AI — React Lovable Frontend Data Models & Type Definitions

export interface Doctor {
  id: string;
  name: string;
  degree: string;
  exp: string;
  specialty: string;
  languages: string;
  hours: string;
  rating: string;
  slots: string[];
  status?: string;
}

export interface DoctorListResponse {
  total_count: number;
  doctors: Doctor[];
}

export interface ClinicLocation {
  branch: string;
  address: string;
  landmark: string;
  map_url: string;
  hours: string;
  phone: string;
}

export interface ClinicalServiceItem {
  id: string;
  title: string;
  badge: string;
  badge_bg: string;
  fee: string;
  tiers: string[];
  duration: string;
  included: string[];
  indications: string;
}

export interface ClinicalServicesResponse {
  directory_markdown: string;
  services: ClinicalServiceItem[];
}

export interface BookingPayload {
  patient_name: string;
  phone_number: string;
  doctor_id: string;
  slot_time: string;
  reason?: string;
}

export interface BookingResponse {
  check_in_code: string;
  patient_name: string;
  phone_number: string;
  doctor_name: string;
  slot_time: string;
  booking_time: string;
  status: string;
  payment_status: string;
  clinic_location: string;
}

export interface PaymentVerificationRequest {
  check_in_code: string;
  payment_method: string;
}

export interface PaymentVerificationResponse {
  success: boolean;
  check_in_code: string;
  patient_name: string;
  doctor_name: string;
  procedure: string;
  slot_time: string;
  status: string;
  verified_at: string;
}

export interface RosterItem {
  check_in_code: string;
  patient_name: string;
  phone_number: string;
  doctor_name: string;
  procedure: string;
  slot_time: string;
  status: string;
}

export interface RosterResponse {
  total_count: number;
  items: RosterItem[];
}

export interface OTOverridePayload {
  doctor_id?: string;
  doctor_name?: string;
  affected_slot: string;
  reason: string;
}

export interface OTOverrideResponse {
  success: boolean;
  doctor_name: string;
  affected_slot: string;
  alerts_dispatched: number;
  message: string;
}
