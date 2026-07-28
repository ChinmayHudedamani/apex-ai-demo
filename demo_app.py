import os
import sys
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo

# 1. FIX PYTHON PATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

# 2. STREAMLIT PAGE CONFIGURATION
st.set_page_config(
    page_title="APEX AI — Copus Concierge",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Indian Standard Time Helper
IST = ZoneInfo("Asia/Kolkata")

def get_ist_time_str() -> str:
    return datetime.now(IST).strftime("%I:%M %p IST")

def get_ist_date_str() -> str:
    return datetime.now(IST).strftime("%d %b %Y, %I:%M %p IST")

# 3. CSP-SAFE NATIVE GLASSMORPHISM STYLING (Zero External Iframes)
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Native Animated Light Background (Bulletproof on Streamlit Cloud) */
    .stApp {
        background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    /* Strict High-Contrast Dark Typography */
    h1, h2, h3, h4, h5, h6, p, span, label, li, td, th {
        color: #0f172a !important;
    }

CLINICAL_SERVICES_DIRECTORY = """### 🏥 Kasthuri Dental — Clinical Services & Fee Directory
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

    /* Glassmorphic Frosted Containers */
    [data-testid="stChatMessage"], .glass-card {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }

    /* WhatsApp Header Bar */
    .wa-header {
        background: rgba(255, 255, 255, 0.96) !important;
        padding: 14px 20px;
        border-radius: 12px;
        border-left: 6px solid #075e54;
        border-bottom: 1px solid #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px;
    }
    .wa-title {
        font-size: 19px;
        font-weight: 700;
        color: #0f172a !important;
    }
    .wa-subtitle {
        font-size: 13px;
        color: #475569 !important;
    }
    .online-badge {
        color: #0d9488 !important;
        font-size: 12px;
        font-weight: 700;
    }

    /* High-Contrast Interactive Buttons */
    .stButton > button {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #075e54 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 18px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        background: #075e54 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(7, 94, 84, 0.25) !important;
        transform: translateY(-1px);
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid #cbd5e1 !important;
    }

    /* Metric Boxes */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0d9488 !important;
    }

    /* Status Badges */
    .badge-beta {
        background: #fff7ed;
        border-left: 4px solid #f97316;
        padding: 10px 14px;
        border-radius: 8px;
        color: #9a3412 !important;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .badge-prod {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 10px 14px;
        border-radius: 8px;
        color: #166534 !important;
        font-weight: 600;
        margin-bottom: 12px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 4. SESSION STATE INITIALIZATION
if "active_tier" not in st.session_state:
    st.session_state.active_tier = "🟢 Tier 1: Essential"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "sender": "assistant",
            "text": "Hello! I am **Copus**, your AI Concierge at Kasthuri Dental Clinic.\n\nHow can I assist you with your dental care today?",
            "time": get_ist_time_str()
        }
    ]

if "hidden_options" not in st.session_state:
    st.session_state.hidden_options = set()

if "roster_db" not in st.session_state:
    st.session_state.roster_db = {
        "APX-4928": {"name": "Rahul Kumar", "phone": "+919876543210", "procedure": "Surgical Extraction", "time": "10:30 AM IST", "status": "PENDING_AT_DESK"},
        "APX-8237": {"name": "Priya Sharma", "phone": "+919876543211", "procedure": "Root Canal (RCT)", "time": "11:30 AM IST", "status": "PENDING_AT_DESK"}
    }

# 5. SIDEBAR PITCH CONTROLLER
st.sidebar.title("⚙️ Pitch Admin Control")
selected_tier = st.sidebar.selectbox(
    "Select SaaS Tier Mode:",
    options=[
        "🟢 Tier 1: Essential",
        "🟡 Tier 2: Pro",
        "🧪 Tier 2.5: Beta Testing",
        "🔴 Tier 3: Enterprise (🚀 In Production)"
    ],
    index=0
)

if selected_tier != st.session_state.active_tier:
    st.session_state.active_tier = selected_tier
    st.rerun()

if st.sidebar.button("🔄 Reset Chat Session", use_container_width=True):
    st.session_state.chat_history = [
        {
            "sender": "assistant",
            "text": "Hello! I am **Copus**, your AI Concierge at Kasthuri Dental Clinic.\n\nHow can I assist you with your dental care today?",
            "time": get_ist_time_str()
        }
    ]
    st.session_state.hidden_options = set()
    st.rerun()

with st.sidebar.expander("🔍 Session State Inspector"):
    st.write(f"**Active Tier**: {st.session_state.active_tier}")
    st.write(f"**Timezone**: `Asia/Kolkata` (IST)")
    st.write(f"**Hidden Options**: {list(st.session_state.hidden_options)}")

# 6. MAIN MULTI-ROLE TABS
tab_patient, tab_doctor, tab_reception = st.tabs([
    "💬 WhatsApp Patient View",
    "👨‍⚕️ Doctor Command Center",
    "👩‍💼 Receptionist Dashboard"
])

# ==========================================
# TAB 1: WHATSAPP PATIENT VIEW
# ==========================================
with tab_patient:
    # Header Banner
    st.markdown(
        """
        <div class="wa-header">
            <div class="wa-title">Kasthuri Dental Clinic <span class="online-badge">✔ Verified Business</span></div>
            <div class="wa-subtitle">Copus AI Concierge • <span style="color:#0d9488; font-weight:600;">Online</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tier Banners
    if "Tier 2.5" in st.session_state.active_tier:
        st.markdown('<div class="badge-beta">🧪 <b>Tier 2.5 Sandbox Active</b> — Testing Local NLM Machine Learning & Branch-and-Bound Fallback.</div>', unsafe_allow_html=True)
    elif "Tier 3" in st.session_state.active_tier:
        st.markdown('<div class="badge-prod">🚀 <b>Enterprise Mode Active</b> — Multi-Branch Auto-Router, TPA Insurance Desk & Gated AI Sandwich.</div>', unsafe_allow_html=True)

    # Render Chat Log
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["sender"]):
            st.markdown(f"**{msg['text']}**" if msg["sender"] == "user" else msg["text"])
            st.caption(f"<sub>{msg['time']}</sub>", unsafe_allow_html=True)

    st.divider()

    # Dynamic Menu Options
    master_options = [
        "1. Doctor Details & Clinic Timings",
        "2. Cost Ranges & Pricing Sheet",
        "3. 📅 Book Appointment (Instant Lock)",
        "4. ⭐ Patient Reviews",
        "5. 🚨 Emergency Triage"
    ]

    if "Tier 2.5" in st.session_state.active_tier:
        master_options.insert(3, "🩺 🧪 Guided Pre-Triage Tree (Beta)")
        master_options.insert(4, "📋 🧪 Digital Care Cards (Beta)")
    elif "Tier 3" in st.session_state.active_tier:
        master_options.insert(3, "📍 Select Clinic Branch (Multi-Node)")
        master_options.insert(4, "🏥 Cashless TPA Insurance Desk")

    available_options = [opt for opt in master_options if opt not in st.session_state.hidden_options]

    # Freeform Input for Tiers 2.5 & 3
    if "Tier 2.5" in st.session_state.active_tier or "Tier 3" in st.session_state.active_tier:
        user_input = st.chat_input("Ask Copus anything about appointments, costs, or symptoms...")
        if user_input:
            st.session_state.chat_history.append({"sender": "user", "text": user_input, "time": get_ist_time_str()})
            
            if any(k in user_input.lower() for k in ["pain", "symptom", "triage", "toothache"]):
                reply = "🩺 **Clinical Pre-Triage Assessment**: Your symptoms indicate moderate sensitivity. We recommend scheduling an evaluation with Dr. Chinmay."
            elif any(k in user_input.lower() for k in ["insurance", "tpa", "claim", "star health"]):
                reply = "🏥 **Cashless TPA Desk**: We support Star Health, HDFC ERGO, and ICICI Lombard. Please present your policy ID at check-in."
            else:
                reply = f"Thank you! I have logged your request: *\"{user_input}\"*. How else can I assist you?"

            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.rerun()

    # Quick Reply Action Buttons
    if not available_options:
        st.info("ℹ️ All informational choices viewed. Scroll up in WhatsApp to review past details.")
    else:
        st.subheader("📱 Tap an option below:")
        cols = st.columns(min(len(available_options), 3))
        
        for idx, option_text in enumerate(available_options):
            col = cols[idx % min(len(available_options), 3)]
            if col.button(option_text, key=f"btn_{idx}_{option_text}"):
                st.session_state.chat_history.append({"sender": "user", "text": option_text, "time": get_ist_time_str()})

                if "Doctor Details" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = "👨‍⚕️ **Lead Surgeon**: Dr. Chinmay Hudedamani (MDS)\n📍 **Location**: Yelahanka Node, Double Road\n🕒 **Hours**: Mon–Sat: 09:00 AM – 08:30 PM IST"
                elif "Cost Ranges" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = CLINICAL_SERVICES_DIRECTORY
                elif "Book Appointment" in option_text:
                    code = f"APX-{secrets.token_hex(2).upper()}"
                    reply = (
                        f"✅ **APPOINTMENT CONFIRMED!**\n\n"
                        f"🎫 **Check-In Code**: `{code}`\n"
                        f"📅 **Booked On**: {get_ist_date_str()}\n"
                        f"💳 **Payment**: **Pay at Clinic Desk** upon arrival (Cash / UPI / Card)\n\n"
                        f"Please present code `{code}` to the receptionist when you arrive."
                    )
                    st.session_state.roster_db[code] = {
                        "name": "Walk-in Patient", "phone": "+919876543210", "procedure": "General Consultation", "time": get_ist_time_str(), "status": "PENDING_AT_DESK"
                    }
                elif "Reviews" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = "⭐ **Patient Reviews**: Rated 4.9/5 stars across 500+ verified visits."
                elif "Emergency" in option_text:
                    reply = "🚨 **Dental Emergency**: Call our duty surgeon immediately:\n📞 **+91 98765 43210**"
                else:
                    reply = f"Selected: **{option_text}**"

                st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
                st.rerun()

# ==========================================
# TAB 2: DOCTOR COMMAND CENTER
# ==========================================
with tab_doctor:
    st.title("👨‍⚕️ Doctor Command Center")
    st.caption("Dr. Chinmay Hudedamani (MDS) — Lead Dental Surgeon")

    if "Tier 1" in st.session_state.active_tier:
        st.warning("🔒 **Tier 2 Pro Upgrade Required**: The Doctor Command Center and OT Emergency Override tools require Tier 2, Tier 2.5, or Tier 3.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Today's Roster", f"{len(st.session_state.roster_db)} Patients")
        col2.metric("Confirmed Check-Ins", "2 Verified")
        col3.metric("Emergency Priority", "1 Acute")
        col4.metric("Revenue Protected", "₹48,500")

        st.divider()
        st.subheader("🚨 Proactive OT Emergency Schedule Override")
        with st.form("ot_override_form"):
            affected_slot = st.selectbox("Select OT Slot to Clear", ["11:30 AM – 01:00 PM IST (Surgical)", "03:00 PM – 04:30 PM IST (Implants)"])
            custom_reason = st.text_input("Reason for Override", "Dr. Chinmay called into urgent OT surgery")
            submit = st.form_submit_button("⚡ Issue Proactive Reschedule Alerts")

            if submit:
                st.success(f"✅ Alerts dispatched to patients for slot '{affected_slot}'. Reason logged: '{custom_reason}'.")

# ==========================================
# TAB 3: RECEPTIONIST DASHBOARD
# ==========================================
with tab_reception:
    st.title("👩‍💼 Receptionist Operations Desk")

    if "Tier 1" in st.session_state.active_tier:
        st.warning("🔒 **Tier 2 Pro Upgrade Required**: Check-In Code verification (`APX-XXXX`) and waiting room management require Tier 2, Tier 2.5, or Tier 3.")
    else:
        st.subheader("⚡ Offline Check-In Code & Payment Collector")
        
        col_in1, col_in2 = st.columns([2, 1])
        with col_in1:
            code_input = st.text_input("Enter Patient Check-In Code (`APX-XXXX`):", placeholder="APX-4928").strip().upper()
        with col_in2:
            pay_method = st.selectbox("Payment Method Collected:", ["UPI (GPay/PhonePe)", "Cash", "Credit/Debit Card"])

        if st.button("Verify Arriving Patient & Collect Payment"):
            if code_input in st.session_state.roster_db:
                record = st.session_state.roster_db[code_input]
                record["status"] = f"PAID_AT_DESK ({pay_method})"
                st.success(
                    f"✅ **CHECK-IN & PAYMENT VERIFIED!**\n\n"
                    f"👤 **Patient**: {record['name']}\n"
                    f"🦷 **Procedure**: {record['procedure']}\n"
                    f"🕒 **Slot**: {record['time']}\n"
                    f"💰 **Status**: Marked as **PAID_AT_DESK** via {pay_method}"
                )
            else:
                st.error(f"❌ Code '{code_input}' not found in today's local roster cache.")

        st.divider()
        st.subheader("📋 Today's Waiting Room Roster")
        for c_code, data in st.session_state.roster_db.items():
            status_badge = "🟢 PAID" if "PAID" in data["status"] else "🟡 PENDING AT DESK"
            st.write(f"**`{c_code}`** | {data['name']} | {data['procedure']} | {data['time']} | Status: `{status_badge}`")