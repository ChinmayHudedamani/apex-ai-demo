# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI Clinic Concierge ("Copus") — Frosted Glass & 3D Spline Bot Concierge

import os
import sys
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo

# 1. FIX PYTHON PATH (Prevents White-Screen Import Errors)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import streamlit.components.v1 as components

# 2. MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="APEX AI — Copus 3D Concierge",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Strict Indian Standard Time Utility
IST = ZoneInfo("Asia/Kolkata")

def get_ist_time_str() -> str:
    return datetime.now(IST).strftime("%I:%M %p IST")

def get_ist_date_str() -> str:
    return datetime.now(IST).strftime("%d %b %Y, %I:%M %p IST")

# 3. EMBED 3D SPLINE CANVAS (FIXED BACKGROUND LAYER)
SPLINE_HTML = """
<script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.72/build/spline-viewer.js"></script>
<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none; opacity: 0.40; background-color: #F8FAFC;">
    <spline-viewer url="https://prod.spline.design/kvUxzrHChHyEVfA5/scene.splinecode"></spline-viewer>
</div>
"""
components.html(SPLINE_HTML, height=0)

# 4. HIGH-CONTRAST LIGHT-MODE GLASSMORPHIC CSS
GLASSMORPHIC_CSS = """
<style>
    /* Global Canvas & Light Theme Base */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Primary Typography Enforcement */
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: #0F172A !important;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.04) !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #0F172A !important;
    }

    /* WhatsApp Header Bar */
    .wa-glass-header {
        background: rgba(7, 94, 84, 0.95);
        backdrop-filter: blur(12px);
        color: #ffffff !important;
        padding: 14px 20px;
        border-radius: 12px 12px 0 0;
        border-bottom: 1px solid #128C7E;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(7, 94, 84, 0.15);
    }
    .wa-glass-header * {
        color: #ffffff !important;
    }

    /* Frosted Glass Container Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05) !important;
    }

    /* Status Banners */
    .lock-banner {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(12px) !important;
        border-left: 6px solid #ff9800 !important;
        border-radius: 10px;
        padding: 18px;
        margin: 15px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        color: #c77700 !important;
    }
    .beta-banner {
        background: rgba(255, 248, 225, 0.92) !important;
        backdrop-filter: blur(12px) !important;
        border-left: 6px solid #f57c00 !important;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        color: #d97706 !important;
    }
    .prod-banner {
        background: rgba(238, 244, 255, 0.92) !important;
        backdrop-filter: blur(12px) !important;
        border-left: 6px solid #075E54 !important;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        color: #075E54 !important;
    }

    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #075E54 !important;
    }

    /* Glass Action Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.92) !important;
        color: #0F172A !important;
        border: 1px solid rgba(203, 213, 225, 0.9) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: rgba(7, 94, 84, 0.08) !important;
        border-color: #075E54 !important;
        color: #075E54 !important;
        transform: translateY(-1px) !important;
    }
</style>
"""
st.markdown(GLASSMORPHIC_CSS, unsafe_allow_html=True)

# 5. SAFE SESSION STATE INITIALIZATION
if "active_tier" not in st.session_state:
    st.session_state.active_tier = "🟢 Tier 1: Essential"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "sender": "assistant",
            "text": "👋 Welcome to **Kasthuri Dental Clinic**!\nI am Copus, your 24/7 AI Dental Assistant powered by APEX AI.\n\nHow can I assist you with your oral health today?",
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

# 6. SIDEBAR PITCH CONTROLLER
st.sidebar.title("⚙️ Pitch Admin Control")
selected_tier = st.sidebar.selectbox(
    "Select SaaS Subscription Plan:",
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

if st.sidebar.button("🔄 Reset Session History", use_container_width=True):
    st.session_state.chat_history = [
        {
            "sender": "assistant",
            "text": "👋 Welcome to **Kasthuri Dental Clinic**!\nI am Copus, your 24/7 AI Dental Assistant powered by APEX AI.\n\nHow can I assist you with your oral health today?",
            "time": get_ist_time_str()
        }
    ]
    st.session_state.hidden_options = set()
    st.rerun()

st.sidebar.divider()
st.sidebar.caption(f"**Mode**: {st.session_state.active_tier}")
st.sidebar.caption(f"**Timezone**: `Asia/Kolkata` (IST)")

with st.sidebar.expander("🔍 Session State Inspector"):
    st.write(f"**Active Tier**: {st.session_state.active_tier}")
    st.write(f"**Hidden Items**: {list(st.session_state.hidden_options)}")

# 7. MAIN APPLICATION TABS
tab_patient, tab_doctor, tab_reception = st.tabs([
    "💬 WhatsApp Patient View",
    "👨‍⚕️ Doctor Command Center",
    "👩‍💼 Receptionist Dashboard"
])

# ==========================================
# TAB 1: WHATSAPP PATIENT VIEW (FROSTED GLASS)
# ==========================================
with tab_patient:
    
    # Tier Status Callout Banners
    if "Tier 2.5" in st.session_state.active_tier:
        st.markdown(
            """
            <div class="beta-banner">
                <b>🧪 Tier 2.5 Beta Mode Active</b> — Local NLM Engine & Branch-and-Bound Decision Tree Fallback.
            </div>
            """,
            unsafe_allow_html=True
        )
    elif "Tier 3" in st.session_state.active_tier:
        st.markdown(
            """
            <div class="prod-banner">
                <b>🚀 Enterprise Mode Active (In Production)</b> — Multi-Branch Auto-Router, TPA Insurance Desk & Gated AI Sandwich.
            </div>
            """,
            unsafe_allow_html=True
        )

    # WhatsApp Header Bar
    st.markdown(
        """
        <div class="wa-glass-header">
            <div>
                <div style="font-size: 17px; font-weight: 700;">Kasthuri Dental Clinic <span style="color: #34b7f1;">☑️</span></div>
                <div style="font-size: 12px; opacity: 0.9;">Copus AI Concierge • <span style="color: #25d366; font-weight: 600;">online</span></div>
            </div>
            <div style="font-size: 12px; font-weight: 600; background: rgba(255, 255, 255, 0.2); padding: 4px 10px; border-radius: 12px;">
                WhatsApp Business Official
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render Chat Stream
    for msg in st.session_state.chat_history:
        avatar = "👤" if msg["sender"] == "user" else "🤖"
        with st.chat_message(msg["sender"], avatar=avatar):
            st.markdown(msg["text"])
            st.caption(f"<sub>{msg['time']}</sub>", unsafe_allow_html=True)

    st.divider()

    # Dynamic Menu Options Based on Active Tier
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

    # Filter out read-once options
    available_options = [opt for opt in master_options if opt not in st.session_state.hidden_options]

    # Freeform Chat Input for Tier 2.5 and Tier 3
    if "Tier 2.5" in st.session_state.active_tier or "Tier 3" in st.session_state.active_tier:
        user_input = st.chat_input("Type your message to Copus AI Concierge...")
        if user_input:
            st.session_state.chat_history.append({"sender": "user", "text": user_input, "time": get_ist_time_str()})
            
            # Intelligent Local Intent Classifier Fallback
            input_lower = user_input.lower()
            if any(k in input_lower for k in ["pain", "symptom", "triage", "toothache", "swelling"]):
                reply = "🩺 *Guided Clinical Pre-Triage*: Your symptoms indicate moderate dental inflammation. We recommend locking a priority slot today."
            elif any(k in input_lower for k in ["insurance", "tpa", "claim", "star health", "cashless"]):
                reply = "🏥 *Cashless TPA Desk*: We support Star Health, HDFC ERGO, and ICICI Lombard. Please present your policy card at reception."
            elif any(k in input_lower for k in ["care", "card", "post-op", "extraction"]):
                reply = "📋 *Digital Care Card Sandbox*: For post-extraction care: Soft food for 24h, avoid hot beverages, bite gently on gauze for 45 mins."
            else:
                reply = f"I've logged your query: *\"{user_input}\"*. Our concierge is resolving details for your session."

            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.rerun()

    # Interactive Quick Reply Buttons
    if not available_options:
        st.info("ℹ️ All informational choices viewed. Scroll up in WhatsApp to re-read details.")
    else:
        st.subheader("📱 Tap an Option below:")
        cols = st.columns(min(len(available_options), 3))
        
        for idx, option_text in enumerate(available_options):
            col = cols[idx % min(len(available_options), 3)]
            if col.button(f"👉 {option_text}", key=f"btn_{idx}_{option_text}"):
                st.session_state.chat_history.append({"sender": "user", "text": option_text, "time": get_ist_time_str()})

                # Strategy Response Dispatch
                if "Doctor Details" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = "👨‍⚕️ **Lead Surgeon**: Dr. Chinmay Hudedamani (MDS)\n📍 **Location**: Yelahanka Node, Double Road\n🕒 **Hours**: Mon–Sat: 09:00 AM – 08:30 PM IST | Sun: 10:00 AM – 02:00 PM IST"
                elif "Cost Ranges" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = "💳 **Pricing Sheet**:\n• Consultation: ₹700\n• Root Canal (RCT): ₹4,500 – ₹7,500\n• Extraction: ₹1,200 – ₹3,500"
                elif "Book Appointment" in option_text:
                    code = f"APX-{secrets.token_hex(2).upper()}"
                    reply = (
                        f"✅ **APPOINTMENT CONFIRMED!**\n\n"
                        f"🎫 **Check-In Code**: `{code}`\n"
                        f"📅 **Booked On**: {get_ist_date_str()}\n"
                        f"💳 **Payment**: **Pay at Clinic Desk** upon arrival (Cash / UPI / Card)\n\n"
                        f"Please show code `{code}` to the receptionist when you arrive."
                    )
                    st.session_state.roster_db[code] = {
                        "name": "Walk-in Patient", "phone": "+919876543210", "procedure": "General Consultation", "time": get_ist_time_str(), "status": "PENDING_AT_DESK"
                    }
                elif "Reviews" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = "⭐ **Patient Reviews**: Rated 4.9/5 stars across 500+ verified visits."
                elif "Emergency" in option_text:
                    reply = "🚨 **Dental Emergency**: Please call our direct duty surgeon immediately:\n📞 tel:+919876543210"
                elif "Pre-Triage" in option_text:
                    reply = "🩺 *Guided Clinical Pre-Triage (Beta)*:\nSelect your symptom severity:\n1. 🔴 Severe Toothache / Swelling (Priority Slot)\n2. 🟡 Moderate Sensitivity\n3. 🟢 Routine Consultation"
                elif "Care Cards" in option_text:
                    st.session_state.hidden_options.add(option_text)
                    reply = "📋 *Digital Care Card (Beta)*:\n**Tooth Extraction Post-Op Rules**:\n1. Rest for 24 hours\n2. Avoid warm/hot liquids\n3. Do not rinse vigorously today."
                else:
                    reply = f"Selected: **{option_text}**"

                st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
                st.rerun()

# ==========================================
# TAB 2: DOCTOR COMMAND CENTER
# ==========================================
with tab_doctor:
    st.title("👨‍⚕️ Doctor Command Center (Dr. Chinmay Hudedamani, MDS)")

    if "Tier 1" in st.session_state.active_tier:
        st.markdown(
            """
            <div class="lock-banner">
                <h3>🔒 Tier 2 Pro Upgrade Required</h3>
                <p>The Doctor Command Center, OT Emergency Override Tool, and Schedule Analytics require Tier 2 (Pro), Tier 2.5 (Beta), or Tier 3 (Enterprise).</p>
            </div>
            """,
            unsafe_allow_html=True
        )
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
                st.success(f"✅ Proactive alerts dispatched to patients for slot '{affected_slot}'. Reason logged: '{custom_reason}'. Time: {get_ist_time_str()}.")

# ==========================================
# TAB 3: RECEPTIONIST DASHBOARD
# ==========================================
with tab_reception:
    st.title("👩‍💼 Receptionist Operations Desk")

    if "Tier 1" in st.session_state.active_tier:
        st.markdown(
            """
            <div class="lock-banner">
                <h3>🔒 Tier 2 Pro Upgrade Required</h3>
                <p>Check-In Code verification (<code>APX-XXXX</code>) and waiting-room roster management require Tier 2, Tier 2.5, or Tier 3.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.subheader("⚡ Offline-First Check-In Code & On-the-Spot Payment Collector")
        
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
                st.error(f"❌ Check-in code '{code_input}' not found in today's local roster cache.")

        st.divider()
        st.subheader("📋 Today's Waiting Room Roster")
        for c_code, data in st.session_state.roster_db.items():
            status_color = "🟢" if "PAID" in data["status"] else "🟡"
            st.write(f"{status_color} **`{c_code}`** | {data['name']} | {data['procedure']} | {data['time']} | Status: `{data['status']}`")
