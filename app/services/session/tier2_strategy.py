# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Tier 2 Pro Strategy Handler (IST Native & Pay-at-Clinic Engine)

import secrets
import random
from typing import List, Set, Dict, Callable, Final, Optional

from app.services.session.models import PatientSession, CommandResult, ActionType, PriorityLevel
from app.services.session.base_strategy import AbstractTierStrategy
from app.services.tier_config import SaaSPlanTier
from app.utils.time_utils import get_current_ist, format_ist_time


class Tier2Strategy(AbstractTierStrategy):
    """Tier 2 Strategy: Instant Slot Lock + Pay-at-Clinic Protocol (IST Native)."""

    MASTER_MENU: Final[List[str]] = [
        "1. Doctor Details & Clinic Timings",
        "2. Cost Ranges & Pricing Sheet",
        "3. 📅 Book Appointment (Instant Lock)",
        "4. ⭐ Patient Reviews",
        "5. 🚨 Emergency Triage",
        "6. Exit Session",
    ]

    INFORMATIONAL_OPTIONS: Final[Set[str]] = {
        "1. Doctor Details & Clinic Timings",
        "1. Doctor Details",
        "2. Cost Ranges & Pricing Sheet",
        "4. ⭐ Patient Reviews",
    }

    def __init__(self) -> None:
        super().__init__(SaaSPlanTier.TIER_2)

    def _build_dispatcher_map(self) -> Dict[str, Callable[[PatientSession, str], CommandResult]]:
        """Polymorphic Dispatcher Map providing $O(1)$ constant-time lookup execution."""
        return {
            "1. Doctor Details & Clinic Timings": self._handle_doctor_timings,
            "1. Doctor Details": self._handle_doctor_timings,
            "2. Cost Ranges & Pricing Sheet": self._handle_pricing,
            "3. 📅 Book Appointment (Instant Lock)": self._handle_instant_booking,
            "4. 📅 Book Appointment (Live Slots)": self._handle_instant_booking,
            "4. ⭐ Patient Reviews": self._handle_reviews,
            "6. Patient Reviews": self._handle_reviews,
            "5. 🚨 Emergency Triage": self._handle_emergency,
            "7. 🚨 Emergency Triage": self._handle_emergency,
            "6. Exit Session": self._handle_exit,
            "8. Exit Session": self._handle_exit,
        }

    def get_menu(self, session: PatientSession) -> List[str]:
        return [item for item in self.MASTER_MENU if item not in session.hidden_options]

    def get_available_menu(self, session: PatientSession) -> List[str]:
        return self.get_menu(session)

    def process_selection(self, session: PatientSession, option_text: str) -> CommandResult:
        return self.process_option(session, option_text)

    # --- Choice Dispatch Handlers ---

    def _handle_doctor_timings(self, session: PatientSession, option_text: str) -> CommandResult:
        body = (
            "👨‍⚕️ *Lead Surgeon*: Dr. Chinmay Hudedamani (MDS - Oral Surgery)\n"
            "📍 *Location*: Yelahanka Node, Double Road\n"
            "🕒 *Hours*: Mon–Sat: 09:00 AM – 08:30 PM IST | Sun: 10:00 AM – 02:00 PM IST"
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_pricing(self, session: PatientSession, option_text: str) -> CommandResult:
        body = (
            "### 🏥 Kasthuri Dental — Clinical Services & Fee Directory\n"
            "*All treatments include painless digital local anesthesia and strict ISO-sterilization protocols.*\n\n"
            "---\n\n"
            "#### 1. 🔍 Comprehensive Diagnostic Consultation\n"
            "* **Fee**: **₹700**\n"
            "* **Duration**: 30 Minutes\n"
            "* **What's Included**:\n"
            "  * Full Intraoral Dental & Gum Health Examination\n"
            "  * High-Definition Digital RVG X-Rays (Zero-Radiation Digital Sensor)\n"
            "  * HD Intraoral Camera Imaging (See your tooth on screen)\n"
            "  * Personalized Written Treatment & Cost Estimate\n"
            "* **Best For**: Routine checkups, second opinions, initial pain evaluation.\n\n"
            "---\n\n"
            "#### 2. 🦷 Micro-Endodontic Root Canal Treatment (RCT)\n"
            "* **Fee**: **₹4,500 – ₹7,500** *(Based on tooth position)*\n"
            "  * *Anterior Tooth (Front)*: ₹4,500\n"
            "  * *Molar Tooth (Back)*: ₹6,000 – ₹7,500 (Complex Canal Navigation)\n"
            "* **Duration**: 45–60 Mins per session *(Single-Visit Option Available)*\n"
            "* **What's Included**:\n"
            "  * Computerized Apex Locator canal measurement\n"
            "  * Painless Rotary Endodontics (NiTi Flexible Files)\n"
            "  * Rubber Dam Isolation for 100% sterile procedure\n"
            "  * Temporary filling & post-treatment RVG confirmation X-ray\n"
            "* **Best For**: Severe throbbing pain, deep decay reaching the nerve, thermal sensitivity.\n\n"
            "---\n\n"
            "#### 3. 👑 CAD/CAM Ceramic & Premium Zirconia Crowns\n"
            "* **Fee**: **₹6,000 – ₹12,000** per tooth\n"
            "  * *Porcelain Fused Metal (PFM)*: ₹6,000 (5-Year Warranty)\n"
            "  * *Monolithic German Zirconia*: ₹12,000 (15-Year Card Warranty & Lifetime Breakage Guarantee)\n"
            "* **Duration**: 2 Visits (48-Hour Lab Turnaround)\n"
            "* **What's Included**:\n"
            "  * 3D Digital Intraoral Scanning (No messy traditional impressions)\n"
            "  * Custom Shade Matching with natural tooth translucency\n"
            "  * Permanent Dental Cementation & Bite Alignment Tuning\n"
            "* **Best For**: Post-RCT protection, fractured teeth, heavy chewing restoration.\n\n"
            "---\n\n"
            "#### 4. 🛠️ Atraumatic Tooth & Wisdom Extraction\n"
            "* **Fee**: **₹1,500 – ₹3,500**\n"
            "  * *Simple Tooth Extraction*: ₹1,500\n"
            "  * *Surgical / Impacted Wisdom Tooth*: ₹3,500\n"
            "* **Duration**: 30–45 Minutes\n"
            "* **What's Included**:\n"
            "  * Deep Local Nerve Block for complete pain relief\n"
            "  * Ultrasonic Bone-Preservation Technique\n"
            "  * Dissolvable Surgical Sutures (if required)\n"
            "  * Complimentary Post-Op Care & Prescription Kit\n"
            "* **Best For**: Irreparable decay, crowded teeth, impacted painful wisdom teeth.\n\n"
            "---\n\n"
            "#### 5. 🪞 Clear Aligners & Orthodontic Smile Alignment\n"
            "* **Fee**: **₹35,000 – ₹90,000**\n"
            "  * *Conventional Ceramic/Metal Braces*: ₹35,000 – ₹50,000\n"
            "  * *Invisible US-FDA Cleared Aligners*: ₹60,000 – ₹90,000\n"
            "* **Duration**: 6 to 18 Months Total Care\n"
            "* **What's Included**:\n"
            "  * 3D Simulation Preview (See your final smile before starting)\n"
            "  * Complete Set of Custom Aligner Trays\n"
            "  * All Monthly Progress Adjustments & Retainer Sets Included\n"
            "* **Best For**: Crooked teeth, gaps, overbites, discreet adult realignment.\n\n"
            "---\n\n"
            "> 💳 **Transparency Guarantee**: *No hidden charges. Full cost estimate provided prior to treatment. Flexible payment options (Cash, UPI, Credit Card, Direct Zero-Cost EMI) collected at the clinic desk after consultation.*"
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_instant_booking(self, session: PatientSession, option_text: str) -> CommandResult:
        """Instantly confirms slot and issues Check-In Code for Pay-at-Clinic arrival."""
        checkin_code = f"APX-{secrets.token_hex(2).upper()}"
        session.check_in_code = checkin_code
        booking_time_ist = format_ist_time(get_current_ist())

        return CommandResult(
            success=True,
            message=(
                f"✅ *APPOINTMENT CONFIRMED!*\n\n"
                f"🎫 *Check-In Code*: `{checkin_code}`\n"
                f"📅 *Booked On*: {booking_time_ist}\n"
                f"📍 *Location*: Kasthuri Dental Clinic, Yelahanka\n"
                f"💳 *Payment*: **Pay at Clinic Desk** upon arrival (Cash / UPI / Card)\n\n"
                f"📌 Please show code `{checkin_code}` to the receptionist when you arrive."
            ),
            action_type=ActionType.TRANSACTIONAL,
            payload={
                "check_in_code": checkin_code,
                "payment_status": "PENDING_AT_DESK",
                "booking_time_ist": booking_time_ist,
            }
        )

    def resolve_slot_conflict(
        self,
        appointment_id: str,
        requesting_priority: PriorityLevel = PriorityLevel.GENERAL_CONSULTATION,
        session: Optional[PatientSession] = None,
        assigned_code: Optional[str] = None
    ) -> CommandResult:
        """Surgical Priority Slot Resolution with Pay-at-Clinic Confirmation."""
        res = self._handle_instant_booking(session or PatientSession("SESS", "+91"), "3. 📅 Book Appointment (Instant Lock)")
        if assigned_code:
            res.payload["check_in_code"] = assigned_code
            if session:
                session.check_in_code = assigned_code
        return res

    def _handle_reviews(self, session: PatientSession, option_text: str) -> CommandResult:
        body = "⭐ *Verified Reviews*: Rated 4.9/5 stars across 500+ patient visits."
        return self._handle_informational_option(session, option_text, body)

    def _handle_emergency(self, session: PatientSession, option_text: str) -> CommandResult:
        return CommandResult(
            success=True,
            message="🚨 *Dental Emergency*: Tap below to call clinic directly:\n📞 tel:+919876543210",
            action_type=ActionType.EMERGENCY,
            payload={"tel_uri": "tel:+919876543210"}
        )

    def _handle_exit(self, session: PatientSession, option_text: str) -> CommandResult:
        session.is_active = False
        return CommandResult(
            success=True,
            message="👋 Thank you for contacting Kasthuri Dental Clinic.",
            action_type=ActionType.NAVIGATION
        )
