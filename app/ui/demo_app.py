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
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Indian Standard Time Helper
IST = ZoneInfo("Asia/Kolkata")

def get_ist_time_str() -> str:
    return datetime.now(IST).strftime("%I:%M %p IST")

def get_ist_date_str() -> str:
    return datetime.now(IST).strftime("%d %b %Y, %I:%M %p IST")

# 3. DOCTORS DIRECTORY DATABASE
DOCTORS_DB = {
    "DOC_1": {
        "name": "Dr. Chinmay Hudedamani",
        "degree": "MDS — Oral & Maxillofacial Surgery",
        "exp": "14+ Years Experience",
        "specialty": "Dental Implants, Surgical Extractions, Jaw Reconstruction",
        "languages": "English, Kannada, Hindi, Telugu",
        "hours": "Mon–Sat: 09:00 AM – 02:00 PM IST",
        "rating": "4.9 ⭐ (320+ verified reviews)",
        "slots": ["10:00 AM IST", "11:30 AM IST", "01:00 PM IST"]
    },
    "DOC_2": {
        "name": "Dr. Ananya Rao",
        "degree": "MDS — Orthodontics & Dentofacial Orthopedics",
        "exp": "10+ Years Experience",
        "specialty": "Invisalign, Clear Aligners, Pediatric & Adult Braces",
        "languages": "English, Kannada, Hindi",
        "hours": "Mon–Sat: 02:30 PM – 08:30 PM IST",
        "rating": "4.95 ⭐ (285+ verified reviews)",
        "slots": ["03:00 PM IST", "04:30 PM IST", "06:00 PM IST", "07:30 PM IST"]
    },
    "DOC_3": {
        "name": "Dr. Vikramaditya Hegde",
        "degree": "MDS — Endodontics & Conservative Dentistry",
        "exp": "12+ Years Experience",
        "specialty": "Single-Visit Root Canal (RCT), Micro-Endodontics, Laser Dentistry",
        "languages": "English, Kannada, Hindi, Tulu",
        "hours": "Mon–Sun: 10:00 AM – 06:00 PM IST",
        "rating": "4.88 ⭐ (210+ verified reviews)",
        "slots": ["10:30 AM IST", "02:00 PM IST", "05:00 PM IST"]
    }
}

# 4. LOCATION & MAP DATA
CLINIC_LOCATION = {
    "branch": "Kasthuri Dental Clinic — Yelahanka Main Node",
    "address": "#42, Double Road, 4th Phase, Yelahanka New Town, Bengaluru, Karnataka 560064",
    "landmark": "Opposite BDA Complex, Near Major Unnikrishnan Road",
    "map_url": "https://maps.google.com/?q=Yelahanka+New+Town+Bengaluru",
    "hours": "Mon–Sat: 09:00 AM – 08:30 PM IST | Sun: 10:00 AM – 02:00 PM IST",
    "phone": "+91 98765 43210"
}

# 5. HIGH-CONTRAST LIGHT GLASSMORPHISM STYLING
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, li, td, th {
        color: #0f172a !important;
    }

    .wa-header {
        background: #ffffff !important;
        padding: 16px 22px;
        border-radius: 14px;
        border-left: 6px solid #00875a;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .wa-title {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a !important;
        margin: 0;
    }
    .wa-subtitle {
        font-size: 13px;
        color: #64748b !important;
        margin: 0;
    }

    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    .doc-card {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .doc-name {
        font-size: 18px;
        font-weight: 700;
        color: #00875a !important;
    }
    .doc-degree {
        font-size: 13px;
        font-weight: 600;
        color: #334155 !important;
    }

    .stButton > button {
        background: #ffffff !important;
        color: #00875a !important;
        border: 1.5px solid #00875a !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 8px 14px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: #00875a !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }

    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #00875a !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 6. SESSION STATE INITIALIZATION
if "active_tier" not in st.session_state:
    st.session_state.active_tier = "🟢 Tier 1: Essential"

if "booking_step" not in st.session_state:
    st.session_state.booking_step = "IDLE"  # IDLE -> SELECT_DOC -> SELECT_SLOT -> PATIENT_INFO -> CONFIRMATION

if "selected_doc_key" not in st.session_state:
    st.session_state.selected_doc_key = None

if "selected_slot" not in st.session_state:
    st.session_state.selected_slot = None

if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "sender": "assistant",
            "text": "Hello! I am **Copus Concierge** at Kasthuri Dental Clinic.\n\nHow can I assist you with your dental health today?",
            "time": get_ist_time_str()
        }
    ]

if "roster_db" not in st.session_state:
    st.session_state.roster_db = {
        "APX-4928": {"name": "Rahul Kumar", "doctor": "Dr. Chinmay Hudedamani", "phone": "+919876543210", "procedure": "Surgical Extraction", "time": "10:30 AM IST", "status": "PENDING_AT_DESK"},
        "APX-8237": {"name": "Priya Sharma", "doctor": "Dr. Ananya Rao", "phone": "+919876543211", "procedure": "Braces Consultation", "time": "03:00 PM IST", "status": "PENDING_AT_DESK"}
    }

# 7. SIDEBAR PITCH CONTROLLER
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
    st.session_state.booking_step = "IDLE"
    st.rerun()

if st.sidebar.button("🔄 Reset Chat Session", use_container_width=True):
    st.session_state.chat_history = [
        {
            "sender": "assistant",
            "text": "Hello! I am **Copus Concierge** at Kasthuri Dental Clinic.\n\nHow can I assist you with your dental health today?",
            "time": get_ist_time_str()
        }
    ]
    st.session_state.booking_step = "IDLE"
    st.session_state.selected_doc_key = None
    st.session_state.selected_slot = None
    st.session_state.patient_info = {}
    st.rerun()

with st.sidebar.expander("🔍 Session State Inspector"):
    st.write(f"**Active Tier**: {st.session_state.active_tier}")
    st.write(f"**Booking Step**: `{st.session_state.booking_step}`")
    st.write(f"**Selected Doctor**: `{st.session_state.selected_doc_key}`")
    st.write(f"**Selected Slot**: `{st.session_state.selected_slot}`")

# 8. MAIN APPLICATION TABS
tab_patient, tab_doctor, tab_reception = st.tabs([
    "💬 WhatsApp Patient View",
    "👨‍⚕️ Doctor Command Center",
    "👩‍💼 Receptionist Dashboard"
])

# ==========================================
# TAB 1: PATIENT CONCIERGE (PATIENT AGENCY FLOW)
# ==========================================
with tab_patient:
    # Clinic Header
    st.markdown(
        """
        <div class="wa-header">
            <div>
                <div class="wa-title">Kasthuri Dental Clinic <span style="color:#00875a; font-size:12px;">✔ Verified Business</span></div>
                <div class="wa-subtitle">Copus AI Concierge • <span style="color:#00875a; font-weight:700;">Online</span></div>
            </div>
            <div style="font-size:12px; color:#64748b; font-weight:600;">Yelahanka Node</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chat Log Stream
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["sender"]):
            st.markdown(f"**{msg['text']}**" if msg["sender"] == "user" else msg["text"])
            st.caption(f"<sub>{msg['time']}</sub>", unsafe_allow_html=True)

    st.divider()

    # --- STEP 1: INITIAL CONCIERGE OPTIONS ---
    if st.session_state.booking_step == "IDLE":
        st.subheader("📱 Tap an option below:")
        col1, col2, col3, col4, col5 = st.columns(5)

        if col1.button("👨‍⚕️ View Our Doctors"):
            st.session_state.chat_history.append({"sender": "user", "text": "View Our Doctors", "time": get_ist_time_str()})
            st.session_state.booking_step = "VIEW_DOCTORS"
            st.rerun()

        if col2.button("📍 Clinic Location & Map"):
            st.session_state.chat_history.append({"sender": "user", "text": "Clinic Location & Map", "time": get_ist_time_str()})
            reply = (
                f"📍 **{CLINIC_LOCATION['branch']}**\n\n"
                f"🏢 **Address**: {CLINIC_LOCATION['address']}\n"
                f"🚩 **Landmark**: {CLINIC_LOCATION['landmark']}\n"
                f"🕒 **Hours**: {CLINIC_LOCATION['hours']}\n"
                f"📞 **Phone**: {CLINIC_LOCATION['phone']}\n\n"
                f"🔗 [📍 Click Here to Open in Google Maps]({CLINIC_LOCATION['map_url']})"
            )
            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.rerun()

        if col3.button("💳 Cost & Pricing Sheet"):
            st.session_state.chat_history.append({"sender": "user", "text": "Cost Ranges & Pricing", "time": get_ist_time_str()})
            reply = (
                "💳 **Kasthuri Dental Standard Fee Structure**:\n"
                "• Consultation & X-Ray: ₹700\n"
                "• Root Canal Treatment (RCT): ₹4,500 – ₹7,500\n"
                "• Dental Crown (Zirconia/Ceramic): ₹6,000 – ₹12,000\n"
                "• Surgical Tooth Extraction: ₹1,500 – ₹3,500\n"
                "• Braces / Aligners: ₹35,000 – ₹90,000"
            )
            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.rerun()

        if col4.button("📅 Book Appointment"):
            st.session_state.chat_history.append({"sender": "user", "text": "I want to book an appointment", "time": get_ist_time_str()})
            reply = "Step 1 of 4: Please choose the specialist doctor you would like to consult with:"
            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.session_state.booking_step = "SELECT_DOC"
            st.rerun()

        if col5.button("🚨 Emergency Triage"):
            st.session_state.chat_history.append({"sender": "user", "text": "Emergency Triage", "time": get_ist_time_str()})
            reply = "🚨 **Dental Emergency**: Call our duty surgeon directly for immediate assistance:\n📞 **+91 98765 43210**"
            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.rerun()

    # --- VIEW DOCTORS LIST ---
    elif st.session_state.booking_step == "VIEW_DOCTORS":
        st.subheader("👨‍⚕️ Our Dental Specialists Directory:")
        for key, doc in DOCTORS_DB.items():
            with st.container():
                st.markdown(
                    f"""
                    <div class="doc-card">
                        <div class="doc-name">{doc['name']}</div>
                        <div class="doc-degree">{doc['degree']} • {doc['exp']}</div>
                        <div style="margin-top:6px; font-size:13px;"><b>Specialities</b>: {doc['specialty']}</div>
                        <div style="font-size:13px;"><b>Languages</b>: {doc['languages']}</div>
                        <div style="font-size:13px;"><b>Availability</b>: {doc['hours']}</div>
                        <div style="font-size:13px; color:#00875a; font-weight:700; margin-top:4px;">{doc['rating']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"📅 Book with {doc['name']}", key=f"btn_view_{key}"):
                    st.session_state.selected_doc_key = key
                    st.session_state.chat_history.append({"sender": "user", "text": f"Selected Doctor: {doc['name']}", "time": get_ist_time_str()})
                    st.session_state.booking_step = "SELECT_SLOT"
                    st.rerun()

        if st.button("⬅️ Back to Main Options"):
            st.session_state.booking_step = "IDLE"
            st.rerun()

    # --- STEP 2: PATIENT SELECTS DOCTOR ---
    elif st.session_state.booking_step == "SELECT_DOC":
        st.subheader("👨‍⚕️ Step 1: Select Your Preferred Doctor")
        for key, doc in DOCTORS_DB.items():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{doc['name']}** ({doc['degree']})\n\n*{doc['specialty']}* — `{doc['hours']}`")
            with col_b:
                if st.button(f"Select Doctor", key=f"sel_doc_{key}"):
                    st.session_state.selected_doc_key = key
                    st.session_state.chat_history.append({"sender": "user", "text": f"Selected {doc['name']}", "time": get_ist_time_str()})
                    reply = f"Great choice! Please pick an available time slot for **{doc['name']}**:"
                    st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
                    st.session_state.booking_step = "SELECT_SLOT"
                    st.rerun()
            st.divider()

    # --- STEP 3: PATIENT SELECTS SLOT FOR THAT SPECIFIC DOCTOR ---
    elif st.session_state.booking_step == "SELECT_SLOT":
        doc = DOCTORS_DB[st.session_state.selected_doc_key]
        st.subheader(f"⏰ Step 2: Available Slots for {doc['name']}")
        
        slot_cols = st.columns(len(doc["slots"]))
        for idx, slot in enumerate(doc["slots"]):
            if slot_cols[idx].button(f"⏰ {slot}", key=f"slot_btn_{idx}"):
                st.session_state.selected_slot = slot
                st.session_state.chat_history.append({"sender": "user", "text": f"Chosen Slot: {slot}", "time": get_ist_time_str()})
                reply = "Step 3 of 4: Please provide your registration details below to complete the booking:"
                st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
                st.session_state.booking_step = "PATIENT_INFO"
                st.rerun()

    # --- STEP 4: PATIENT ENTERS DETAILS ---
    elif st.session_state.booking_step == "PATIENT_INFO":
        st.subheader("📋 Step 3: Patient Information")
        with st.form("patient_registration_form"):
            name = st.text_input("Full Name:", placeholder="e.g. Chinmay Hudedamani")
            phone = st.text_input("Mobile Phone Number (+91):", placeholder="e.g. 9876543210")
            reason = st.selectbox("Reason for Visit:", ["General Consultation", "Toothache / Pain", "Root Canal Evaluation", "Braces / Aligners", "Cleaning & Scaling"])
            submitted = st.form_submit_button("Proceed to Final Confirmation ➡️")

            if submitted:
                if name.strip() == "" or phone.strip() == "":
                    st.error("Please enter your name and phone number.")
                else:
                    st.session_state.patient_info = {"name": name, "phone": phone, "reason": reason}
                    st.session_state.booking_step = "CONFIRMATION"
                    st.rerun()

    # --- STEP 5: PATIENT CONFIRMS BOOKING EXPLICITLY ---
    elif st.session_state.booking_step == "CONFIRMATION":
        doc = DOCTORS_DB[st.session_state.selected_doc_key]
        p = st.session_state.patient_info
        slot = st.session_state.selected_slot

        st.subheader("📄 Step 4: Confirm Your Appointment Summary")
        st.info(
            f"👤 **Patient**: {p['name']} (+91 {p['phone']})\n\n"
            f"👨‍⚕️ **Doctor**: {doc['name']} ({doc['degree']})\n\n"
            f"🕒 **Slot**: {slot} (Today, {get_ist_date_str()})\n\n"
            f"🦷 **Reason**: {p['reason']}\n\n"
            f"📍 **Location**: {CLINIC_LOCATION['branch']}"
        )

        col_c1, col_c2 = st.columns(2)
        if col_c1.button("✅ Confirm & Lock Appointment", use_container_width=True):
            code = f"APX-{secrets.token_hex(2).upper()}"
            final_reply = (
                f"🎉 **APPOINTMENT LOCKED & CONFIRMED!**\n\n"
                f"🎫 **Check-In Code**: `{code}`\n"
                f"👤 **Patient**: {p['name']}\n"
                f"👨‍⚕️ **Doctor**: {doc['name']}\n"
                f"🕒 **Confirmed Slot**: {slot}\n"
                f"💳 **Payment**: **Pay at Clinic Desk** upon arrival (Cash / UPI / Card)\n\n"
                f"📍 **Address**: {CLINIC_LOCATION['address']}\n"
                f"🔗 [📍 Open Location in Google Maps]({CLINIC_LOCATION['map_url']})\n\n"
                f"Please present check-in code `{code}` at the reception desk."
            )
            # Log to local roster database
            st.session_state.roster_db[code] = {
                "name": p["name"],
                "doctor": doc["name"],
                "phone": f"+91{p['phone']}",
                "procedure": p["reason"],
                "time": slot,
                "status": "PENDING_AT_DESK"
            }
            st.session_state.chat_history.append({"sender": "assistant", "text": final_reply, "time": get_ist_time_str()})
            st.session_state.booking_step = "IDLE"
            st.rerun()

        if col_c2.button("❌ Change Details / Restart", use_container_width=True):
            st.session_state.booking_step = "IDLE"
            st.rerun()

    # Freeform Prompt Input
    if "Tier 2.5" in st.session_state.active_tier or "Tier 3" in st.session_state.active_tier:
        user_input = st.chat_input("Type your question or symptom to Copus...")
        if user_input:
            st.session_state.chat_history.append({"sender": "user", "text": user_input, "time": get_ist_time_str()})
            reply = f"I have received your request: *\"{user_input}\"*. Let me help you find the right specialist."
            st.session_state.chat_history.append({"sender": "assistant", "text": reply, "time": get_ist_time_str()})
            st.session_state.booking_step = "VIEW_DOCTORS"
            st.rerun()

# ==========================================
# TAB 2: DOCTOR COMMAND CENTER
# ==========================================
with tab_doctor:
    st.title("👨‍⚕️ Doctor Command Center")

    if "Tier 1" in st.session_state.active_tier:
        st.warning("🔒 **Tier 2 Pro Upgrade Required**: Doctor OT Management and Roster Analytics require Tier 2, Tier 2.5, or Tier 3.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Today's Roster", f"{len(st.session_state.roster_db)} Patients")
        col2.metric("Confirmed Check-Ins", "2 Verified")
        col3.metric("Emergency Priority", "1 Acute")
        col4.metric("Revenue Protected", "₹48,500")

        st.divider()
        st.subheader("🚨 OT Emergency Schedule Override")
        with st.form("ot_override_form"):
            selected_doc = st.selectbox("Select Surgeon:", [doc["name"] for doc in DOCTORS_DB.values()])
            affected_slot = st.selectbox("Select OT Slot to Clear:", ["11:30 AM – 01:00 PM IST", "03:00 PM – 04:30 PM IST"])
            custom_reason = st.text_input("Override Reason:", "Emergency surgical intervention")
            submit = st.form_submit_button("⚡ Issue Proactive Reschedule Alerts")

            if submit:
                st.success(f"✅ Alerts dispatched to affected patients for {selected_doc} ({affected_slot}). Reason: '{custom_reason}'.")

# ==========================================
# TAB 3: RECEPTIONIST DASHBOARD
# ==========================================
with tab_reception:
    st.title("👩‍💼 Receptionist Desk & Check-In Verifier")

    if "Tier 1" in st.session_state.active_tier:
        st.warning("🔒 **Tier 2 Pro Upgrade Required**: Offline check-in code verification (`APX-XXXX`) requires Tier 2+.")
    else:
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
                    f"👨‍⚕️ **Doctor**: {record.get('doctor', 'Duty Surgeon')}\n"
                    f"🦷 **Procedure**: {record['procedure']}\n"
                    f"🕒 **Slot**: {record['time']}\n"
                    f"💰 **Status**: Marked as **PAID_AT_DESK** via {pay_method}"
                )
            else:
                st.error(f"❌ Check-in code '{code_input}' not found in today's local roster cache.")

        st.divider()
        st.subheader("📋 Today's Waiting Room Roster")
        for c_code, data in st.session_state.roster_db.items():
            status_color = "🟢 PAID" if "PAID" in data["status"] else "🟡 PENDING AT DESK"
            st.write(f"**`{c_code}`** | {data['name']} | **Doctor**: {data.get('doctor', 'General')} | {data['procedure']} | {data['time']} | `{status_color}`")