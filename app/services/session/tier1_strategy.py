# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Tier 1 Essential Strategy Handler

from datetime import datetime
from typing import Dict, Callable

from app.services.session.models import PatientSession, CommandResult, ActionType
from app.services.session.base_strategy import AbstractTierStrategy
from app.services.tier_config import SaaSPlanTier


class Tier1Strategy(AbstractTierStrategy):
    """Tier 1 Essential Strategy: 24/7 Digital Receptionist with Live Clock and Safety Rules."""

    def __init__(self):
        super().__init__(SaaSPlanTier.TIER_1)

    def _build_dispatcher_map(self) -> Dict[str, Callable[[PatientSession, str], CommandResult]]:
        return {
            "1. Doctor Details": self._handle_doctor_details,
            "2. Clinic Timings & Live Status": self._handle_timings_status,
            "3. Location & Valet Parking": self._handle_location_parking,
            "4. Cost Ranges & Pricing Sheet": self._handle_cost_ranges,
            "5. Sterilization & Safety Protocols": self._handle_sterilization,
            "6. Patient Reviews": self._handle_reviews,
            "7. 🚨 Dental Emergency (Call Now)": self._handle_emergency_call,
            "8. Exit Session": self._handle_exit
        }

    # --- Dispatcher Handler Methods ---

    def _handle_doctor_details(self, session: PatientSession, option_text: str) -> CommandResult:
        body = (
            "👨‍⚕️ *Lead Surgeon & Specialist*: Dr. Chinmay Hudedamani (MDS, Oral & Maxillofacial Surgery)\n"
            "• 12+ Years Clinical Excellence\n"
            "• Specialized in Microscopic RCT & Permanent Dental Implants\n"
            "• Yelahanka Node v0.2 & Koramangala Main Branch"
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_timings_status(self, session: PatientSession, option_text: str) -> CommandResult:
        # Dynamic IST Status Clock Calculation
        now = datetime.now()
        hour = now.hour
        is_open = 9 <= hour < 20  # Open 09:00 AM to 08:30 PM IST
        status_str = "🟢 OPEN NOW (Mon-Sat 09:00 AM - 08:30 PM)" if is_open else "🔴 CLOSED NOW (Reopens Mon 09:00 AM)"

        body = (
            f"🕒 *CLINIC LIVE STATUS*: {status_str}\n\n"
            f"• Mon-Sat: 09:00 AM – 08:30 PM\n"
            f"• Sunday: 10:00 AM – 02:00 PM (Emergency Only)"
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_location_parking(self, session: PatientSession, option_text: str) -> CommandResult:
        body = (
            "📍 *LOCATION & PARKING*:\n"
            "5th Phase, Yelahanka New Town, Bengaluru (near Major Sandeep Unnikrishnan Road).\n"
            "🚗 *Valet Parking*: Free Basement Valet Parking available on site!"
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_cost_ranges(self, session: PatientSession, option_text: str) -> CommandResult:
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

    def _handle_sterilization(self, session: PatientSession, option_text: str) -> CommandResult:
        body = (
            "🛡️ *STERILIZATION & SAFETY PROTOCOLS*:\n"
            "• Class-B German Autoclave 6-Step Sterilization\n"
            "• 100% Disinfected & Single-Use Disposable Pouch Kits\n"
            "• ISO 9001 Certified Clinical Environment"
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_reviews(self, session: PatientSession, option_text: str) -> CommandResult:
        body = (
            "⭐ *PATIENT REVIEWS & RATINGS*:\n"
            "• Google Rating: 4.9 / 5.0 (1,200+ Verified Patient Reviews)\n"
            "• 'Dr. Chinmay is incredibly gentle and painless!' — Ananya R."
        )
        return self._handle_informational_option(session, option_text, body)

    def _handle_emergency_call(self, session: PatientSession, option_text: str) -> CommandResult:
        msg = (
            "🚨 *24/7 DENTAL EMERGENCY LINE*\n"
            "Tap to call our emergency desk directly: tel:+919876543210\n"
            "Or head directly to Yelahanka New Town 5th Phase!"
        )
        return CommandResult(
            success=True,
            message=msg,
            action_type=ActionType.EMERGENCY,
            payload={"tel_uri": "tel:+919876543210"}
        )

    def _handle_exit(self, session: PatientSession, option_text: str) -> CommandResult:
        session.is_active = False
        return CommandResult(
            success=True,
            message="👋 Thank you for contacting APEX Dental. Session closed.",
            action_type=ActionType.NAVIGATION
        )
