// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// APEX AI / Copus AI — FastAPI Backend Service Client Abstraction Layer

import { showToast } from "./toast";
import {
  Doctor,
  DoctorListResponse,
  ClinicLocation,
  ClinicalServicesResponse,
  BookingPayload,
  BookingResponse,
  PaymentVerificationResponse,
  RosterResponse,
  OTOverridePayload,
  OTOverrideResponse
} from "../types";

const API_BASE_URL = "http://localhost:8000/api/v1";

/**
  * Generic helper to execute fetch requests with automated JSON error handling & toast dispatching.
  */
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status} ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (typeof errorData.detail === "string") {
          errorMessage = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map((e: any) => `${e.loc?.join(".")}: ${e.msg}`).join("; ");
        } else if (errorData.detail) {
          errorMessage = JSON.stringify(errorData.detail);
        }
      } catch {
        // Fallback to default response status text
      }

      showToast("error", `API Error (${response.status})`, errorMessage);
      throw new Error(errorMessage);
    }

    return (await response.json()) as T;
  } catch (err: any) {
    if (err.name === "TypeError" && err.message.includes("fetch")) {
      const connErr = "Unable to connect to FastAPI backend at http://localhost:8000. Is Uvicorn server running?";
      showToast("error", "Connection Failed", connErr);
      throw new Error(connErr);
    }
    throw err;
  }
}

/**
 * Fetch all configured doctors & available slots.
 * GET /api/v1/doctors
 */
export async function fetchDoctors(): Promise<Doctor[]> {
  const res = await apiFetch<DoctorListResponse>("/doctors");
  return res.doctors;
}

/**
 * Fetch single doctor details by ID.
 * GET /api/v1/doctors/{doc_id}
 */
export async function fetchDoctorById(docId: string): Promise<Doctor> {
  return await apiFetch<Doctor>(`/doctors/${docId}`);
}

/**
 * Fetch clinic branch location, hours, and map metadata.
 * GET /api/v1/doctors/location
 */
export async function fetchClinicLocation(): Promise<ClinicLocation> {
  return await apiFetch<ClinicLocation>("/doctors/location");
}

/**
 * Fetch Clinical Services Directory & structured fee tiers.
 * GET /api/v1/doctors/services
 */
export async function fetchClinicalServices(): Promise<ClinicalServicesResponse> {
  return await apiFetch<ClinicalServicesResponse>("/doctors/services");
}

/**
 * Lock an appointment slot and generate an un-guessable APX- check-in code.
 * POST /api/v1/bookings
 */
export async function createBooking(payload: BookingPayload): Promise<BookingResponse> {
  const res = await apiFetch<BookingResponse>("/bookings", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  showToast("success", "Appointment Locked!", `Check-In Code: ${res.check_in_code}`);
  return res;
}

/**
 * Verify arriving patient's check-in code and mark desk payment.
 * POST /api/v1/reception/verify
 */
export async function verifyCheckin(
  code: string,
  payMethod: string
): Promise<PaymentVerificationResponse> {
  const payload = { check_in_code: code, payment_method: payMethod };
  const res = await apiFetch<PaymentVerificationResponse>("/reception/verify", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  showToast("success", "Payment Verified", `Code ${res.check_in_code} marked as ${res.status}`);
  return res;
}

/**
 * Fetch live waiting room patient roster.
 * GET /api/v1/reception/roster
 */
export async function fetchRoster(): Promise<RosterResponse> {
  return await apiFetch<RosterResponse>("/reception/roster");
}

/**
 * Issue proactive emergency surgical OT override alerts.
 * POST /api/v1/bookings/ot-override
 */
export async function triggerOTOverride(
  doctorId: string,
  slot: string,
  reason: string
): Promise<OTOverrideResponse> {
  const payload: OTOverridePayload = {
    doctor_id: doctorId,
    affected_slot: slot,
    reason: reason,
  };
  const res = await apiFetch<OTOverrideResponse>("/bookings/ot-override", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  showToast("info", "OT Override Dispatched", res.message);
  return res;
}
