import streamlit as st
import numpy as np
import random
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AgriSense", layout="wide")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("⚙️ Settings")

language = st.sidebar.selectbox(
    "🌐 Language",
    ["English", "Hindi", "Marathi", "Tamil", "Gujarati", "Odia", "Malayalam"]
)

view_mode = st.sidebar.radio(
    "📱 View Mode",
    ["Desktop View", "Mobile View"]
)

crop_age = st.sidebar.number_input(
    "🌱 Crop Age (Days after sowing)",
    min_value=0,
    max_value=300,
    value=90
)

# --------------------------------------------------
# COLOR PALETTES (POWER BI INSPIRED)
# --------------------------------------------------
C = {
    "bg": "#0e1117",
    "card": "#020617",
    "border": "#1f2937",
    "text": "#e5e7eb",
    "muted": "#9ca3af",
    "accent": "#60a5fa"
}

# --------------------------------------------------
# CSS (FINAL – INCLUDING BASEWEB PORTAL FIX)
# --------------------------------------------------
st.markdown(f"""
<style>

/* GLOBAL */
html, body, .stApp {{
    background-color: {C['bg']} !important;
    color: {C['text']} !important;
    font-family: Inter, system-ui, sans-serif;
}}

p, span, div, label, h1, h2, h3, h4 {{
    color: {C['text']} !important;
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background-color: {C['card']} !important;
    border-right: 1px solid {C['border']};
}}

section[data-testid="stSidebar"] label {{
    color: {C['muted']} !important;
}}

/* INPUT FIELDS */
div[data-baseweb="select"] > div,
input {{
    background-color: {C['card']} !important;
    color: {C['text']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 8px !important;
}}

div[data-baseweb="select"] span {{
    color: {C['text']} !important;
}}

/* --------- DROPDOWN MENU (THE REAL FIX) --------- */
div[role="listbox"],
div[data-baseweb="menu"] {{
    background-color: {C['card']} !important;
    border: 1px solid {C['border']} !important;
}}

div[role="option"] {{
    background-color: {C['card']} !important;
    color: {C['text']} !important;
    font-size: 14px;
}}

div[role="option"]:hover,
div[aria-selected="true"] {{
    background-color: {C['accent']} !important;
    color: #ffffff !important;
}}

/* HEADER */
.header {{
    display: flex;
    align-items: center;
    gap: 14px;
    background-color: {C['card']};
    padding: 16px 22px;
    border-radius: 14px;
    border: 1px solid {C['border']};
    margin-bottom: 28px;
}}

.logo {{
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background-color: {C['accent']};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}}

.title {{
    font-size: 22px;
    font-weight: 600;
}}

.subtitle {{
    font-size: 13px;
    color: {C['muted']} !important;
}}

/* KPI CARDS */
[data-testid="metric-container"] {{
    background-color: {C['card']} !important;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid {C['border']};
}}

[data-testid="metric-container"] label {{
    color: {C['muted']} !important;
    font-size: 13px;
}}

[data-testid="metric-container"] div {{
    color: {C['text']} !important;
    font-size: 34px;
    font-weight: 600;
}}

/* DIVIDER */
hr {{
    border: none;
    height: 1px;
    background-color: {C['border']};
    margin: 36px 0;
}}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LANGUAGE STRINGS
# --------------------------------------------------
LANG = {
    "English": {
        "title": "AgriSense",
        "subtitle": "AI & IoT Based Smart Agriculture Dashboard",
        "soil": "Soil Moisture (%)",
        "temp": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "irrigation": "Irrigation Status",
        "stress": "Crop Stress Level",
        "harvest": "Harvest Status",
        "connectivity": "Sensor Connectivity",
        "required": "REQUIRED",
        "not_required": "NOT REQUIRED",
        "normal": "NORMAL",
        "warning": "WARNING",
        "critical": "CRITICAL",
        "not_ready": "NOT READY",
        "almost_ready": "ALMOST READY",
        "ready": "READY FOR HARVEST"
    },
    "Hindi": {
        "title": "एग्रीसेंस",
        "subtitle": "AI व IoT आधारित कृषि डैशबोर्ड",
        "soil": "मिट्टी की नमी (%)",
        "temp": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "irrigation": "सिंचाई स्थिति",
        "stress": "फसल तनाव",
        "harvest": "कटाई स्थिति",
        "connectivity": "सेंसर कनेक्टिविटी",
        "required": "आवश्यक",
        "not_required": "आवश्यक नहीं",
        "normal": "सामान्य",
        "warning": "चेतावनी",
        "critical": "गंभीर",
        "not_ready": "तैयार नहीं",
        "almost_ready": "लगभग तैयार",
        "ready": "कटाई के लिए तैयार"
    },
    "Marathi": {
        "title": "अ‍ॅग्रीसेन्स",
        "subtitle": "AI व IoT आधारित स्मार्ट शेती डॅशबोर्ड",
        "soil": "मातीतील आर्द्रता (%)",
        "temp": "तापमान (°C)",
        "humidity": "हवेतील आर्द्रता (%)",
        "irrigation": "सिंचन स्थिती",
        "stress": "पीक ताण",
        "harvest": "कापणी स्थिती",
        "connectivity": "सेन्सर कनेक्टिव्हिटी",
        "required": "आवश्यक",
        "not_required": "आवश्यक नाही",
        "normal": "सामान्य",
        "warning": "इशारा",
        "critical": "गंभीर",
        "not_ready": "तयार नाही",
        "almost_ready": "लवकरच तयार",
        "ready": "कापणीसाठी तयार"
    }
}

T = LANG.get(language, LANG["English"])

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(f"""
<div class="header">
    <div class="logo">🌾</div>
    <div>
        <div class="title">{T['title']}</div>
        <div class="subtitle">{T['subtitle']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SENSOR DATA
# --------------------------------------------------
soil = np.random.randint(20, 80)
temp = np.random.randint(25, 40)
humidity = np.random.randint(30, 75)
signal = random.choice(["CONNECTED", "WEAK", "DISCONNECTED"])

# --------------------------------------------------
# AI LOGIC
# --------------------------------------------------
irrigation_text = T["required"] if soil < 35 else T["not_required"]

stress_text = (
    T["critical"] if soil < 30 or temp > 37
    else T["warning"] if soil < 45 or temp > 33
    else T["normal"]
)

harvest_text = (
    T["not_ready"] if crop_age < 60
    else T["almost_ready"] if crop_age < 90
    else T["ready"]
)

# --------------------------------------------------
# UI
# --------------------------------------------------
if view_mode == "Mobile View":
    st.metric(f"💧 {T['soil']}", soil)
    st.metric(f"🌡️ {T['temp']}", temp)
    st.metric(f"💨 {T['humidity']}", humidity)
    st.metric(f"🚿 {T['irrigation']}", irrigation_text)
    st.metric(f"🌿 {T['stress']}", stress_text)
    st.metric(f"🌾 {T['harvest']}", harvest_text)
    st.metric(f"📡 {T['connectivity']}", signal)
else:
    c1, c2, c3 = st.columns(3)
    c1.metric(f"💧 {T['soil']}", soil)
    c2.metric(f"🌡️ {T['temp']}", temp)
    c3.metric(f"💨 {T['humidity']}", humidity)

    st.divider()

    c4, c5 = st.columns(2)
    c4.metric(f"🚿 {T['irrigation']}", irrigation_text)
    c4.metric(f"🌿 {T['stress']}", stress_text)
    c5.metric(f"🌾 {T['harvest']}", harvest_text)
    c5.metric(f"📡 {T['connectivity']}", signal)

# --------------------------------------------------
# AUTO REFRESH
# --------------------------------------------------
time.sleep(3)
st.rerun()
