# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Global Backend Core Configuration & Metadata

import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any, List, Optional

# Load .env / .env.local file if present on server side
try:
    from dotenv import load_dotenv
    env_local = Path(__file__).resolve().parent.parent.parent / ".env.local"
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_local.exists():
        load_dotenv(env_local)
    elif env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass

# Timezone Standardization
IST_TIMEZONE = ZoneInfo("Asia/Kolkata")


class Settings:
    PROJECT_NAME: str = "APEX AI — Copus Medical Engine"
    API_V1_STR: str = "/api/v1"
    TIMEZONE: ZoneInfo = ZoneInfo("Asia/Kolkata")

    # SERVER-SIDE ONLY SECRET KEYS (Never exposed to client bundles)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "apex_ai_super_secret_jwt_key_2026_server_only")
    ADMIN_API_TOKEN: str = os.getenv("ADMIN_API_TOKEN", "apex_admin_secret_token_secure")

    CLINIC_LOCATION: Dict[str, Any] = {
        "branch": "Kasthuri Dental Clinic — Yelahanka Main Node",
        "address": "#42, Double Road, 4th Phase, Yelahanka New Town, Bengaluru, Karnataka 560064",
        "landmark": "Opposite BDA Complex, Near Major Unnikrishnan Road",
        "map_url": "https://maps.google.com/?q=Yelahanka+New+Town+Bengaluru",
        "hours": "Mon–Sat: 09:00 AM – 08:30 PM IST | Sun: 10:00 AM – 02:00 PM IST",
        "phone": "+91 98765 43210"
    }


settings = Settings()


def get_current_ist_str() -> str:
    """Returns current IST formatted time string."""
    return datetime.now(IST_TIMEZONE).strftime("%I:%M %p IST")


def get_current_ist_date_str() -> str:
    """Returns current IST formatted date and time string."""
    return datetime.now(IST_TIMEZONE).strftime("%d %b %Y, %I:%M %p IST")


# Clinic Location & Operational Metadata
CLINIC_LOCATION: Dict[str, str] = settings.CLINIC_LOCATION

# Doctors Directory Database
DOCTORS_DB: Dict[str, Dict[str, Any]] = {
    "DOC_1": {
        "id": "DOC_1",
        "name": "Dr. Chinmay Hudedamani",
        "degree": "MDS — Oral & Maxillofacial Surgery",
        "exp": "14+ Years Experience",
        "specialty": "Dental Implants, Surgical Extractions, Jaw Reconstruction",
        "languages": "English, Kannada, Hindi, Telugu",
        "hours": "Mon–Sat: 09:00 AM – 02:00 PM IST",
        "rating": "4.9 ⭐ (320+ verified reviews)",
        "slots": ["10:00 AM IST", "11:30 AM IST", "01:00 PM IST"],
        "daily_slots": [
            {"time": "09:30 AM IST", "available": True},
            {"time": "10:30 AM IST", "available": False, "reason": "BOOKED"},
            {"time": "11:30 AM IST", "available": True},
            {"time": "02:00 PM IST", "available": False, "reason": "SURGERY"},
            {"time": "04:30 PM IST", "available": True},
            {"time": "05:30 PM IST", "available": False, "reason": "BOOKED"},
        ]
    },
    "DOC_2": {
        "id": "DOC_2",
        "name": "Dr. Ananya Rao",
        "degree": "MDS — Orthodontics & Dentofacial Orthopedics",
        "exp": "10+ Years Experience",
        "specialty": "Invisalign, Clear Aligners, Pediatric & Adult Braces",
        "languages": "English, Kannada, Hindi",
        "hours": "Mon–Sat: 02:30 PM – 08:30 PM IST",
        "rating": "4.95 ⭐ (285+ verified reviews)",
        "slots": ["03:00 PM IST", "04:30 PM IST", "06:00 PM IST", "07:30 PM IST"],
        "daily_slots": [
            {"time": "02:30 PM IST", "available": True},
            {"time": "03:30 PM IST", "available": False, "reason": "BOOKED"},
            {"time": "04:30 PM IST", "available": True},
            {"time": "05:30 PM IST", "available": True},
            {"time": "06:30 PM IST", "available": False, "reason": "BOOKED"},
        ]
    },
    "DOC_3": {
        "id": "DOC_3",
        "name": "Dr. Vikramaditya Hegde",
        "degree": "MDS — Endodontics & Conservative Dentistry",
        "exp": "12+ Years Experience",
        "specialty": "Single-Visit Root Canal (RCT), Micro-Endodontics, Laser Dentistry",
        "languages": "English, Kannada, Hindi, Tulu",
        "hours": "Mon–Sun: 10:00 AM – 06:00 PM IST",
        "rating": "4.88 ⭐ (210+ verified reviews)",
        "slots": ["10:30 AM IST", "02:00 PM IST", "05:00 PM IST"],
        "daily_slots": [
            {"time": "10:00 AM IST", "available": True},
            {"time": "11:30 AM IST", "available": False, "reason": "BOOKED"},
            {"time": "02:00 PM IST", "available": True},
            {"time": "03:30 PM IST", "available": False, "reason": "SURGERY"},
            {"time": "05:00 PM IST", "available": True},
        ]
    }
}

# Clinical Services & Fee Directory Text
CLINICAL_SERVICES_DIRECTORY: str = """### 🏥 Kasthuri Dental — Clinical Services & Fee Directory
*All treatments include painless digital local anesthesia and strict ISO-sterilization protocols.*

---

#### 1. 🔍 Comprehensive Diagnostic Consultation
* **Fee**: **₹700**
* **Duration**: 30 Minutes
* **What's Included**:
  * Full Intraoral Dental & Gum Health Examination
  * High-Definition Digital RVG X-Rays (Zero-Radiation Digital Sensor)
  * HD Intraoral Camera Imaging (See your tooth on screen)
  * Personalized Written Treatment & Cost Estimate
* **Best For**: Routine checkups, second opinions, initial pain evaluation.

---

#### 2. 🦷 Micro-Endodontic Root Canal Treatment (RCT)
* **Fee**: **₹4,500 – ₹7,500** *(Based on tooth position)*
  * *Anterior Tooth (Front)*: ₹4,500
  * *Molar Tooth (Back)*: ₹6,000 – ₹7,500 (Complex Canal Navigation)
* **Duration**: 45–60 Mins per session *(Single-Visit Option Available)*
* **What's Included**:
  * Computerized Apex Locator canal measurement
  * Painless Rotary Endodontics (NiTi Flexible Files)
  * Rubber Dam Isolation for 100% sterile procedure
  * Temporary filling & post-treatment RVG confirmation X-ray
* **Best For**: Severe throbbing pain, deep decay reaching the nerve, thermal sensitivity.

---

#### 3. 👑 CAD/CAM Ceramic & Premium Zirconia Crowns
* **Fee**: **₹6,000 – ₹12,000** per tooth
  * *Porcelain Fused Metal (PFM)*: ₹6,000 (5-Year Warranty)
  * *Monolithic German Zirconia*: ₹12,000 (15-Year Card Warranty & Lifetime Breakage Guarantee)
* **Duration**: 2 Visits (48-Hour Lab Turnaround)
* **What's Included**:
  * 3D Digital Intraoral Scanning (No messy traditional impressions)
  * Custom Shade Matching with natural tooth translucency
  * Permanent Dental Cementation & Bite Alignment Tuning
* **Best For**: Post-RCT protection, fractured teeth, heavy chewing restoration.

---

#### 4. 🛠️ Atraumatic Tooth & Wisdom Extraction
* **Fee**: **₹1,500 – ₹3,500**
  * *Simple Tooth Extraction*: ₹1,500
  * *Surgical / Impacted Wisdom Tooth*: ₹3,500
* **Duration**: 30–45 Minutes
* **What's Included**:
  * Deep Local Nerve Block for complete pain relief
  * Ultrasonic Bone-Preservation Technique
  * Dissolvable Surgical Sutures (if required)
  * Complimentary Post-Op Care & Prescription Kit
* **Best For**: Irreparable decay, crowded teeth, impacted painful wisdom teeth.

---

#### 5. 🪞 Clear Aligners & Orthodontic Smile Alignment
* **Fee**: **₹35,000 – ₹90,000**
  * *Conventional Ceramic/Metal Braces*: ₹35,000 – ₹50,000
  * *Invisible US-FDA Cleared Aligners*: ₹60,000 – ₹90,000
* **Duration**: 6 to 18 Months Total Care
* **What's Included**:
  * 3D Simulation Preview (See your final smile before starting)
  * Complete Set of Custom Aligner Trays
  * All Monthly Progress Adjustments & Retainer Sets Included
* **Best For**: Crooked teeth, gaps, overbites, discreet adult realignment.

---

> 💳 **Transparency Guarantee**: *No hidden charges. Full cost estimate provided prior to treatment. Flexible payment options (Cash, UPI, Credit Card, Direct Zero-Cost EMI) collected at the clinic desk after consultation.*"""

# Structured Clinical Services Data
CLINICAL_SERVICES_DATA: List[Dict[str, Any]] = [
    {
        "id": "diag",
        "title": "🔍 Comprehensive Diagnostic Consultation",
        "badge": "Zero-Radiation Digital",
        "badge_bg": "#0284c7",
        "fee": "₹700",
        "tiers": ["Standard Consultation & Examination: ₹700"],
        "duration": "30 Minutes | Single Visit",
        "included": [
            "Full Intraoral Dental & Gum Health Examination",
            "High-Definition Digital RVG X-Rays (Zero-Radiation Digital Sensor)",
            "HD Intraoral Camera Imaging (See your tooth on screen)",
            "Personalized Written Treatment & Cost Estimate"
        ],
        "indications": "Routine checkups, second opinions, initial pain evaluation."
    },
    {
        "id": "rct",
        "title": "🦷 Micro-Endodontic Root Canal Treatment (RCT)",
        "badge": "Single-Visit Option",
        "badge_bg": "#00875a",
        "fee": "₹4,500 – ₹7,500",
        "tiers": [
            "Anterior Tooth (Front): ₹4,500",
            "Molar Tooth (Back): ₹6,000 – ₹7,500 (Complex Canal Navigation)"
        ],
        "duration": "45–60 Mins per session | Single or 2-Visit Option",
        "included": [
            "Computerized Apex Locator canal measurement",
            "Painless Rotary Endodontics (NiTi Flexible Files)",
            "Rubber Dam Isolation for 100% sterile procedure",
            "Temporary filling & post-treatment RVG confirmation X-ray"
        ],
        "indications": "Severe throbbing pain, deep decay reaching the nerve, thermal sensitivity."
    },
    {
        "id": "crown",
        "title": "👑 CAD/CAM Ceramic & Premium Zirconia Crowns",
        "badge": "15-Year Warranty",
        "badge_bg": "#7c3aed",
        "fee": "₹6,000 – ₹12,000 per tooth",
        "tiers": [
            "Porcelain Fused Metal (PFM): ₹6,000 (5-Year Warranty)",
            "Monolithic German Zirconia: ₹12,000 (15-Year Card Warranty & Lifetime Breakage Guarantee)"
        ],
        "duration": "2 Visits (48-Hour Lab Turnaround)",
        "included": [
            "3D Digital Intraoral Scanning (No messy traditional impressions)",
            "Custom Shade Matching with natural tooth translucency",
            "Permanent Dental Cementation & Bite Alignment Tuning"
        ],
        "indications": "Post-RCT protection, fractured teeth, heavy chewing restoration."
    },
    {
        "id": "extraction",
        "title": "🛠️ Atraumatic Tooth & Wisdom Extraction",
        "badge": "Pain-Free Protocol",
        "badge_bg": "#d97706",
        "fee": "₹1,500 – ₹3,500",
        "tiers": [
            "Simple Tooth Extraction: ₹1,500",
            "Surgical / Impacted Wisdom Tooth: ₹3,500"
        ],
        "duration": "30–45 Minutes | Single Session",
        "included": [
            "Deep Local Nerve Block for complete pain relief",
            "Ultrasonic Bone-Preservation Technique",
            "Dissolvable Surgical Sutures (if required)",
            "Complimentary Post-Op Care & Prescription Kit"
        ],
        "indications": "Irreparable decay, crowded teeth, impacted painful wisdom teeth."
    },
    {
        "id": "aligners",
        "title": "🪞 Clear Aligners & Orthodontic Smile Alignment",
        "badge": "US-FDA Cleared",
        "badge_bg": "#2563eb",
        "fee": "₹35,000 – ₹90,000",
        "tiers": [
            "Conventional Ceramic/Metal Braces: ₹35,000 – ₹50,000",
            "Invisible US-FDA Cleared Aligners: ₹60,000 – ₹90,000"
        ],
        "duration": "6 to 18 Months Total Care",
        "included": [
            "3D Simulation Preview (See your final smile before starting)",
            "Complete Set of Custom Aligner Trays",
            "All Monthly Progress Adjustments & Retainer Sets Included"
        ],
        "indications": "Crooked teeth, gaps, overbites, discreet adult realignment."
    }
]
