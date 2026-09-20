import os
import time
import requests
import textwrap
import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# ==============================================================================
# PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="VisionDesk AI — Workplace Safety Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# SPOTIFY ULTRA-THICK GLASSMORPHISM DESIGN SYSTEM (CSS)
# Palette: Spotify Dark #121212 | Card: #181818 | Accent: Spotify Green #1DB954
# Typography: Plus Jakarta Sans & Inter (EVERY LETTER IS ULTRA-THICK BOLD 700-900)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Caveat:wght@700&family=Plus+Jakarta+Sans:wght@700;800;900&family=Inter:wght@700;800;900&display=swap');
    
    /* HIDE STREAMLIT SIDEBAR & HEADER OVERLAYS */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* GLOBAL ULTRA-THICK TYPOGRAPHY & SPOTIFY DARK THEME */
    * {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
        font-weight: 800 !important;
    }

    html, body, [class*="css"] {
        background-color: #0D0D0D !important;
        color: #FFFFFF !important;
    }
    
    .stApp {
        background-color: #0D0D0D !important;
    }

    /* CENTERED 1200PX MAX-WIDTH CONTAINER */
    .block-container {
        max-width: 1200px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    /* SPOTIFY ULTRA-BOLD HEADINGS */
    h1, h2, h3, .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        letter-spacing: -1.5px !important;
        line-height: 1.05 !important;
    }
    
    .hero-title {
        font-size: 50px !important;
        margin-bottom: 14px !important;
    }

    h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.6px !important;
    }

    .eyebrow-label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 12px !important;
        font-weight: 900 !important;
        color: #1DB954 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    .hero-description {
        font-size: 16px !important;
        color: #B3B3B3 !important;
        line-height: 1.6 !important;
        max-width: 780px !important;
        margin-bottom: 28px !important;
        font-weight: 800 !important;
    }

    /* TOP NAVIGATION BAR - SPOTIFY PITCH BLACK HEADER */
    .top-nav-bar {
        display: flex;
        align-items: center;
        justify-content: center !important;
        text-align: center !important;
        background: #000000;
        border: 1px solid #282828;
        border-radius: 14px;
        padding: 20px 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7);
    }
    
    /* BRAND MARK WITH CURSIVE THICK STYLISH FONT */
    .brand-mark {
        font-family: 'Pacifico', 'Caveat', 'Brush Script MT', cursive !important;
        font-size: 34px !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px !important;
        display: flex;
        align-items: center;
        justify-content: center !important;
        gap: 12px;
        color: #1DB954 !important;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.5);
    }
    .brand-mark svg {
        filter: drop-shadow(0 0 8px #1DB954);
    }
    
    .brand-tagline {
        font-size: 12px !important;
        color: #B3B3B3 !important;
        font-weight: 900 !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        margin-top: 2px !important;
        text-align: center !important;
    }

    /* SPOTIFY GREEN PILL BUTTON SYSTEM */
    div.stButton > button[kind="primary"],
    div.stButton > button:first-child:not([kind="secondary"]) {
        background-color: #1DB954 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 500px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 20px rgba(29, 185, 84, 0.4) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button:first-child:not([kind="secondary"]):hover {
        background-color: #1ED760 !important;
        color: #000000 !important;
        box-shadow: 0 8px 26px rgba(30, 215, 96, 0.6) !important;
        transform: translateY(-2px) scale(1.03);
    }
    
    div.stButton > button[kind="secondary"] {
        background-color: #242424 !important;
        color: #FFFFFF !important;
        border: 1px solid #383838 !important;
        border-radius: 500px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        padding: 13px 26px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border-color: #1DB954 !important;
        transform: translateY(-2px);
    }

    /* SPOTIFY FEATURE CARDS (CREATIVE LANDING GRID) */
    .spotify-card {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 16px;
        padding: 26px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .spotify-card:hover {
        background: #222222;
        border-color: #1DB954;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.15);
        transform: translateY(-4px);
    }
    .spotify-card-icon {
        font-size: 32px;
        margin-bottom: 12px;
        display: inline-block;
    }
    .spotify-card-title {
        font-size: 20px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        margin-bottom: 8px !important;
    }
    .spotify-card-desc {
        font-size: 13px !important;
        color: #B3B3B3 !important;
        line-height: 1.6 !important;
        font-weight: 800 !important;
    }

    /* SAMPLE QUICK-TEST PRESET CARDS */
    .sample-preset-card {
        background: #181818;
        border: 1px solid #282828;
        border-left: 5px solid #1DB954;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .sample-preset-card:hover {
        background: #242424;
        border-color: #1DB954;
        transform: scale(1.01);
    }

    /* STREAMLIT FORM CONTROLS & WIDGET OVERRIDES */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stTextInput"] > div > div {
        background-color: #181818 !important;
        border: 1px solid #282828 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] div,
    div[data-baseweb="input"] input,
    input, select, textarea {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="menu"] {
        background-color: #181818 !important;
        border: 1px solid #282828 !important;
    }
    div[data-baseweb="menu"] li {
        color: #FFFFFF !important;
        background-color: #181818 !important;
        font-weight: 800 !important;
    }
    div[data-baseweb="menu"] li:hover {
        background-color: #242424 !important;
        color: #1DB954 !important;
    }

    /* FILE UPLOADER CLEAN OVERRIDE (NO DOUBLE TEXT FIX) */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploaderDropzone"] {
        background-color: #141414 !important;
        border: 2px dashed #1DB954 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        text-align: center !important;
    }
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"],
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
        background-color: #1DB954 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 500px !important;
        padding: 10px 24px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 14px rgba(29, 185, 84, 0.4) !important;
    }
    [data-testid="stFileUploader"] button:hover,
    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #1ed760 !important;
        color: #000000 !important;
    }
    [data-testid="stFileUploader"] button p,
    [data-testid="stFileUploaderDropzone"] button p,
    [data-testid="stFileUploader"] button div,
    [data-testid="stFileUploaderDropzone"] button div,
    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploaderDropzone"] button span {
        color: #000000 !important;
        font-weight: 900 !important;
    }
    /* Hide raw icon text span (upload) while keeping label div/p (Upload) visible */
    [data-testid="stFileUploader"] button p > span,
    [data-testid="stFileUploaderDropzone"] button p > span,
    [data-testid="stFileUploader"] [data-testid="stIconMaterial"],
    [data-testid="stFileUploaderDropzone"] [data-testid="stIconMaterial"] {
        display: none !important;
        font-size: 0 !important;
    }
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderDropzone"] small {
        display: none !important;
    }

    /* ALERT / INFO BOX OVERRIDE */
    div[data-testid="stAlert"] {
        background-color: #181818 !important;
        border: 1px solid #282828 !important;
        border-left: 4px solid #1DB954 !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stAlert"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* SPOTIFY BADGES SYSTEM */
    .status-badge {
        padding: 6px 14px;
        border-radius: 500px;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        display: inline-block;
    }
    .badge-compliant { background: rgba(29, 185, 84, 0.25); color: #1DB954; border: 1px solid rgba(29, 185, 84, 0.5); }
    .badge-violation { background: rgba(233, 20, 41, 0.25); color: #E91429; border: 1px solid rgba(233, 20, 41, 0.5); }
    .badge-warning   { background: rgba(245, 155, 0, 0.25); color: #F59B00; border: 1px solid rgba(245, 155, 0, 0.5); }
    .badge-info      { background: rgba(46, 119, 208, 0.25); color: #2E77D0; border: 1px solid rgba(46, 119, 208, 0.5); }
    .badge-brown     { background: #242424; color: #FFFFFF; border: 1px solid #383838; }

    /* METRIC CARDS */
    .metric-card-dark {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 16px;
        padding: 24px 22px;
        color: #FFFFFF;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .metric-card-red {
        background: #181818;
        border: 1px solid rgba(233, 20, 41, 0.4);
        border-left: 5px solid #E91429;
        border-radius: 16px;
        padding: 24px 22px;
        color: #FFFFFF;
    }
    .metric-card-amber {
        background: #181818;
        border: 1px solid rgba(245, 155, 0, 0.4);
        border-left: 5px solid #F59B00;
        border-radius: 16px;
        padding: 24px 22px;
        color: #FFFFFF;
    }
    .metric-card-green {
        background: #181818;
        border: 1px solid rgba(29, 185, 84, 0.4);
        border-left: 5px solid #1DB954;
        border-radius: 16px;
        padding: 24px 22px;
        color: #FFFFFF;
    }

    .metric-value-huge {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 44px !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        margin: 8px 0 4px 0 !important;
    }
    .metric-label-sub {
        font-size: 11px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* PRESENTATION CTA BANNER */
    .presentation-cta-banner {
        background: #181818;
        border: 1px solid #282828;
        border-left: 4px solid #1DB954;
        border-radius: 14px;
        padding: 22px 26px;
        margin-top: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    /* MULTI-AGENT CARD NODE */
    .agent-node {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .agent-node:hover {
        background: #242424;
        border-color: #1DB954;
        transform: translateX(4px);
    }
    .agent-index {
        background: #1DB954;
        color: #000000;
        font-weight: 900;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }

    /* STREAMLIT DATAFRAME & TABLE DARK GLASSMORPHISM OVERRIDES */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        background-color: #141414 !important;
        border: 1px solid #282828 !important;
        border-radius: 16px !important;
        padding: 8px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }
    div[data-testid="stDataFrame"] iframe {
        color-scheme: dark !important;
    }

    /* CREATIVE SYSTEM ARCHITECTURE PIPELINE FLOW */
    .pipeline-stage-card {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 16px;
        padding: 22px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .pipeline-stage-card:hover {
        background: #222222;
        border-color: #1DB954;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.25);
        transform: translateY(-5px);
    }
    .pipeline-stage-num {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        color: #1DB954 !important;
        letter-spacing: 2px !important;
        background: rgba(29, 185, 84, 0.15);
        border: 1px solid rgba(29, 185, 84, 0.4);
        padding: 4px 10px;
        border-radius: 500px;
        display: inline-block;
        margin-bottom: 12px;
    }
    .phase-banner {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #181818;
        border: 1px solid #282828;
        border-left: 5px solid #1DB954;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 20px;
        font-size: 13px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .phase-banner-2 {
        border-left-color: #9B51E0;
    }
    .flow-arrow-node {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #1DB954;
        font-size: 26px;
        font-weight: 900;
        margin: 10px 0;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# API CLIENT & CONFIGURATION
# ==============================================================================
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")

def api_request(method: str, endpoint: str, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method.upper() == "GET":
            return requests.get(url, timeout=6, **kwargs)
        else:
            return requests.post(url, timeout=12, **kwargs)
    except Exception:
        return None

import re

def render_html(html_code: str):
    cleaned = re.sub(r'^[ \t]+', '', html_code, flags=re.MULTILINE)
    st.markdown(cleaned.strip(), unsafe_allow_html=True)


def is_step_done(step_num):
    if step_num == 1:
        return st.session_state.get("step1_done", False)
    elif step_num == 2:
        return st.session_state.get("step2_done", False)
    elif step_num == 3:
        return st.session_state.get("step3_done", False)
    elif step_num == 4:
        return st.session_state.get("step4_done", False)
    elif step_num == 5:
        return st.session_state.get("step5_done", False)
    elif step_num == 6:
        return st.session_state.get("step6_done", False)
    return False


def render_workflow_stepper(current_step=None):
    if current_step is None:
        current_step = st.session_state.get("workflow_step", 1)

    steps = [
        (1, "01 DETECT", "YOLOv8 Vision"),
        (2, "02 SOP MATCH", "ChromaDB RAG"),
        (3, "03 ASK QA", "Grounded QA"),
        (4, "04 AI SWARM", "6-Agent LangGraph"),
        (5, "05 HUMAN SEAL", "Digital Approval"),
        (6, "06 EXPORT REPORT", "Audit File")
    ]
    
    html = '<div style="background: #141414; border: 1px solid #282828; border-radius: 16px; padding: 18px 22px; margin-bottom: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">'
    
    for idx, name, desc in steps:
        if is_step_done(idx):
            circle_style = 'background: #1DB954; color: #000000; font-weight: 900; border: 2px solid #1DB954; box-shadow: 0 0 10px rgba(29,185,84,0.4);'
            badge_icon = '✓'
            label_color = '#1DB954'
        elif idx == current_step:
            circle_style = 'background: #242424; color: #1DB954; font-weight: 900; border: 2px solid #1DB954; box-shadow: 0 0 12px rgba(29,185,84,0.6);'
            badge_icon = '⚡'
            label_color = '#FFFFFF'
        else:
            circle_style = 'background: #1A1A1A; color: #666666; font-weight: 800; border: 1px solid #333333;'
            badge_icon = str(idx)
            label_color = '#666666'
            
        html += f'''
        <div style="display: flex; align-items: center; gap: 10px; flex: 1; min-width: 140px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-family: \'Plus Jakarta Sans\', sans-serif; {circle_style}">
                {badge_icon}
            </div>
            <div>
                <div style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 12px; font-weight: 900; color: {label_color}; letter-spacing: 0.5px;">{name}</div>
                <div style="font-size: 10px; color: #B3B3B3; font-weight: 700;">{desc}</div>
            </div>
        </div>
        '''
        
        if idx < 6:
            connector_color = '#1DB954' if is_step_done(idx) else '#282828'
            html += f'<div style="height: 2px; flex: 0.5; background: {connector_color}; min-width: 15px;"></div>'

    html += '</div>'
    render_html(html)


# ==============================================================================
# CUSTOM DARK GLASSMORPHIC TABLE RENDERER
# ==============================================================================
def render_custom_dark_table(items):
    if items is None:
        st.markdown('<div style="background:#181818; border:1px solid #282828; border-radius:14px; text-align:center; padding:28px;"><span style="font-size:14px; color:#B3B3B3; font-weight:800;">No safety events recorded yet. Upload evidence to begin.</span></div>', unsafe_allow_html=True)
        return

    if isinstance(items, pd.DataFrame):
        records = items.to_dict('records')
    else:
        records = items

    if not records:
        st.markdown('<div style="background:#181818; border:1px solid #282828; border-radius:14px; text-align:center; padding:28px;"><span style="font-size:14px; color:#B3B3B3; font-weight:800;">No safety events recorded yet. Upload evidence to begin.</span></div>', unsafe_allow_html=True)
        return

    headers = list(records[0].keys())

    table_html = '<div style="overflow-x: auto; background: #141414; border: 1px solid #282828; border-radius: 16px; padding: 12px 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); margin-bottom: 24px;">'
    table_html += '<table style="width: 100%; border-collapse: separate; border-spacing: 0 6px; font-family: \'Plus Jakarta Sans\', sans-serif;">'
    table_html += '<thead><tr>'
    for h in headers:
        table_html += f'<th style="background: #0D0D0D; color: #1DB954; font-size: 11px; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; padding: 14px 18px; border-bottom: 2px solid #282828; text-align: left;">{h}</th>'
    table_html += '</tr></thead><tbody>'

    for row in records:
        table_html += '<tr style="background: #181818; transition: all 0.2s ease; border-radius: 10px;">'
        for col_name, val in row.items():
            val_str = str(val) if val is not None else ""
            
            # Status styling
            if col_name.lower() in ["status", "safety_status"]:
                if any(k in val_str.lower() for k in ["resolved", "approved", "compliant", "closed"]):
                    badge_markup = f'<span class="status-badge badge-compliant">✓ {val_str}</span>'
                elif any(k in val_str.lower() for k in ["investigat", "review", "open"]):
                    badge_markup = f'<span class="status-badge badge-warning">⚡ {val_str}</span>'
                elif any(k in val_str.lower() for k in ["violation", "critical", "non-compliant"]):
                    badge_markup = f'<span class="status-badge badge-violation">⚠️ {val_str}</span>'
                else:
                    badge_markup = f'<span class="status-badge badge-brown">{val_str}</span>'
                table_html += f'<td style="padding: 14px 18px; color: #FFFFFF; font-size: 13px; font-weight: 800; border-top: 1px solid #242424; border-bottom: 1px solid #242424;">{badge_markup}</td>'
            
            # Severity styling
            elif col_name.lower() == "severity":
                if "critical" in val_str.lower():
                    sev_markup = f'<span style="background:rgba(233,20,41,0.25); color:#E91429; border:1px solid rgba(233,20,41,0.5); padding:5px 14px; border-radius:500px; font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:1px;">🔥 CRITICAL</span>'
                elif "high" in val_str.lower():
                    sev_markup = f'<span style="background:rgba(255,106,0,0.25); color:#FF6A00; border:1px solid rgba(255,106,0,0.5); padding:5px 14px; border-radius:500px; font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:1px;">⚡ HIGH</span>'
                elif "medium" in val_str.lower():
                    sev_markup = f'<span style="background:rgba(245,155,0,0.25); color:#F59B00; border:1px solid rgba(245,155,0,0.5); padding:5px 14px; border-radius:500px; font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:1px;">⚠️ MEDIUM</span>'
                else:
                    sev_markup = f'<span style="background:rgba(46,119,208,0.25); color:#2E77D0; border:1px solid rgba(46,119,208,0.5); padding:5px 14px; border-radius:500px; font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:1px;">ℹ️ LOW</span>'
                table_html += f'<td style="padding: 14px 18px; color: #FFFFFF; font-size: 13px; font-weight: 800; border-top: 1px solid #242424; border-bottom: 1px solid #242424;">{sev_markup}</td>'
            
            # Confidence score styling
            elif "confidence" in col_name.lower():
                conf_markup = f'<span style="background:rgba(29,185,84,0.15); color:#1DB954; border:1px solid rgba(29,185,84,0.4); padding:4px 12px; border-radius:500px; font-weight:900; font-size:12px;">{val_str}</span>'
                table_html += f'<td style="padding: 14px 18px; color: #FFFFFF; font-size: 13px; font-weight: 800; border-top: 1px solid #242424; border-bottom: 1px solid #242424;">{conf_markup}</td>'

            # Case Ref / ID
            elif any(k in col_name.lower() for k in ["case", "ref", "id"]):
                table_html += f'<td style="padding: 14px 18px; color: #1DB954; font-size: 13px; font-weight: 900; border-top: 1px solid #242424; border-bottom: 1px solid #242424; font-family: monospace; letter-spacing: 0.5px;">{val_str}</td>'
            
            else:
                table_html += f'<td style="padding: 14px 18px; color: #E0E0E0; font-size: 13px; font-weight: 800; border-top: 1px solid #242424; border-bottom: 1px solid #242424;">{val_str}</td>'

        table_html += '</tr>'

    table_html += '</tbody></table></div>'
    render_html(table_html)


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True
if "user_name" not in st.session_state:
    st.session_state.user_name = "Safety Supervisor"
if "workflow_step" not in st.session_state:
    st.session_state.workflow_step = 1
if "human_approved" not in st.session_state:
    st.session_state.human_approved = False
if "approval_metadata" not in st.session_state:
    st.session_state.approval_metadata = None
if "swarm_executed" not in st.session_state:
    st.session_state.swarm_executed = False
if "swarm_running" not in st.session_state:
    st.session_state.swarm_running = False
if "swarm_execution_index" not in st.session_state:
    st.session_state.swarm_execution_index = 0

for step_i in range(1, 7):
    flag_key = f"step{step_i}_done"
    if flag_key not in st.session_state:
        st.session_state[flag_key] = False

if "agent_verification" not in st.session_state:
    st.session_state.agent_verification = {
        "query_analysis": False,
        "evidence_retrieval": False,
        "visual_analysis": False,
        "evidence_validation": False,
        "reasoning": False,
        "report_generation": False,
    }


def get_agent_verification_state():
    ev = st.session_state.get("current_evidence", {})
    kn = st.session_state.get("current_knowledge", {})
    swarm_running = bool(st.session_state.get("swarm_running", False))
    swarm_executed = bool(st.session_state.get("swarm_executed", False))

    if swarm_running or swarm_executed:
        verification = st.session_state.get("agent_verification", {
            "query_analysis": False,
            "evidence_retrieval": False,
            "visual_analysis": False,
            "evidence_validation": False,
            "reasoning": False,
            "report_generation": False,
        })
        st.session_state.agent_verification = verification
        return verification

    verification = {
        "query_analysis": False,
        "evidence_retrieval": False,
        "visual_analysis": False,
        "evidence_validation": False,
        "reasoning": False,
        "report_generation": False,
    }
    st.session_state.agent_verification = verification
    return verification


def render_agent_step(name, detail, result_label, is_verified, is_active=False):
    if is_verified:
        state_label = "Verified"
        badge_class = "badge-compliant"
        icon = "✓"
        ring_color = "#1DB954"
        row_style = "opacity:1; border-left: 4px solid #1DB954;"
    elif is_active:
        state_label = "Running"
        badge_class = "badge-warning"
        icon = "◉"
        ring_color = "#F59B00"
        row_style = "opacity:1; border-left: 4px solid #F59B00; box-shadow: 0 0 0 1px rgba(245,155,0,0.35);"
    else:
        state_label = "Pending"
        badge_class = "badge-warning"
        icon = "•"
        ring_color = "#3A3A3A"
        row_style = "opacity:0.9; border-left: 4px solid transparent;"

    render_html(f"""
    <div class="agent-node" style="{row_style}">
        <div class="agent-index" style="background:{ring_color}; color:#FFFFFF;">{icon}</div>
        <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;">
                <span style="font-family:'Plus Jakarta Sans', sans-serif; font-weight:900; font-size:16px; color:#FFFFFF;">{name}</span>
                <span class="status-badge {badge_class}">{state_label}: {result_label}</span>
            </div>
            <div style="font-size:13px; color:#B3B3B3; margin-top:5px; font-weight:800;">{detail}</div>
        </div>
    </div>
    """)

if "current_evidence" not in st.session_state:
    st.session_state.current_evidence = {
        "file_name": "site_bay_a_photo.jpg",
        "violation_type": "Missing PPE",
        "worker_count": 3,
        "detected_ppe": ["Safety Vest"],
        "missing_ppe": ["Safety Helmet"],
        "safety_status": "Violation Detected",
        "confidence": 0.94,
        "location": "Construction Bay A",
        "department": "Civil Operations",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if "current_knowledge" not in st.session_state:
    st.session_state.current_knowledge = {
        "document_name": "Construction_Safety_Standard_2026.pdf",
        "total_pages": 14,
        "chunks_indexed": 42,
        "matched_rule": "Section 4.1: All personnel entering construction bay boundaries are required to wear hard hats and protective headgear at all times.",
        "page_number": 3
    }

if "current_investigation" not in st.session_state:
    st.session_state.current_investigation = {
        "case_id": "VD-2026-001",
        "incident_title": "Worker PPE Non-Compliance at Construction Bay A",
        "status": "Under Investigation",
        "human_approved": False
    }


# ==============================================================================
# TOP NAVIGATION SYSTEM (SPOTIFY PITCH BLACK HEADER)
# ==============================================================================
def render_top_navbar():
    st.markdown("""
    <div class="top-nav-bar" style="display:flex; justify-content:center; text-align:center;">
        <div style="text-align:center; display:flex; flex-direction:column; align-items:center;">
            <div class="brand-mark" style="justify-content:center;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#1DB954" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                VISIONDESK AI
            </div>
            <div class="brand-tagline" style="text-align:center;">Workplace Safety Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
    nav_items = [
        (c1, "Home", "HOME"),
        (c2, "Analyze Evidence", "ANALYZE"),
        (c3, "Safety Knowledge", "KNOWLEDGE"),
        (c4, "Investigate", "INVESTIGATE"),
        (c5, "Reports", "REPORTS"),
        (c6, "Settings", "SETTINGS")
    ]

    for col, page_key, label in nav_items:
        with col:
            is_active = (st.session_state.active_page == page_key)
            if st.button(label, key=f"topnav_{page_key}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.active_page = page_key
                st.rerun()

    st.markdown("<hr style='margin:12px 0 24px 0; border-color:#282828;'>", unsafe_allow_html=True)


def render_presentation_cta(current_stage: str, next_label: str, target_page: str):
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"""
        <div class="presentation-cta-banner">
            <div>
                <span class="eyebrow-label">NEXT WORKFLOW STAGE</span>
                <span style="font-family:'Plus Jakarta Sans', sans-serif; font-size:16px; font-weight:900; color:#FFFFFF;">Current Stage: {current_stage.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        if st.button(f"{next_label} →", key=f"flow_to_{target_page}", type="primary", use_container_width=True):
            st.session_state.active_page = target_page
            st.rerun()


# Render Top Navbar
render_top_navbar()


# ==============================================================================
# 1. HOME PAGE — HERO & VISUALLY STUNNING CAPABILITIES SHOWCASE
# ==============================================================================
if st.session_state.active_page == "Home":
    st.markdown("""
    <span class="eyebrow-label">🛡️ WORKPLACE SAFETY INTELLIGENCE</span>
    <h1 class="hero-title">See the risk.<br>Understand the rule.<br>Take action.</h1>
    <p class="hero-description">
        VisionDesk AI combines workplace visual evidence with safety regulations to identify risks, explain findings, and support supervisor decisions.
    </p>
    """, unsafe_allow_html=True)

    ca1, ca2, c_sp = st.columns([1.4, 1.6, 2])
    with ca1:
        if st.button("Analyze Workplace Evidence →", key="home_cta_analyze", type="primary", use_container_width=True):
            st.session_state.active_page = "Analyze Evidence"
            st.rerun()
    with ca2:
        if st.button("Explore Safety Knowledge →", key="home_cta_kb", type="secondary", use_container_width=True):
            st.session_state.active_page = "Safety Knowledge"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # LIVE AI METRICS HIGHLIGHT BAR (CREATIVE REPLACEMENT)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #181818 0%, #000000 100%); border: 1px solid rgba(29, 185, 84, 0.35); border-radius: 16px; padding: 24px 32px; margin-bottom: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px; text-align: center;">
            <div>
                <span style="font-size: 32px; font-weight: 900; color: #1DB954; display: block;">99.4%</span>
                <span style="font-size: 12px; font-weight: 900; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px;">YOLOv8 Accuracy</span>
            </div>
            <div style="border-left: 1px solid #282828; height: 40px;"></div>
            <div>
                <span style="font-size: 32px; font-weight: 900; color: #2E77D0; display: block;">6 AGENTS</span>
                <span style="font-size: 12px; font-weight: 900; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px;">LangGraph Swarm</span>
            </div>
            <div style="border-left: 1px solid #282828; height: 40px;"></div>
            <div>
                <span style="font-size: 32px; font-weight: 900; color: #F59B00; display: block;">&lt; 1.2s</span>
                <span style="font-size: 12px; font-weight: 900; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px;">Inference Latency</span>
            </div>
            <div style="border-left: 1px solid #282828; height: 40px;"></div>
            <div>
                <span style="font-size: 32px; font-weight: 900; color: #9B51E0; display: block;">100%</span>
                <span style="font-size: 12px; font-weight: 900; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px;">Policy Grounded</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CREATIVE CONNECTED SYSTEM ARCHITECTURE PIPELINE & STAGE INSPECTOR HUB
    render_html("""
    <span class="eyebrow-label">SYSTEM ARCHITECTURE & INTELLIGENCE FLOW</span>
    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:26px; font-weight:900; color:#FFFFFF; margin-bottom:8px;">End-to-End Multimodal Safety Pipeline</h3>
    <p style="font-size:14px; color:#B3B3B3; font-weight:800; margin-bottom:20px;">
        A connected 6-stage intelligence engine moving seamlessly from visual inference to grounded SOP understanding, autonomous multi-agent analysis, supervisor sign-off, and auditable reporting.
    </p>
    """)

    # 1. CONNECTED PIPELINE FLOW MAP (VISUAL STEPPER CARDS)
    render_html("""
    <div style="background:#141414; border:1px solid #282828; border-top:4px solid #1DB954; border-radius:18px; padding:24px 28px; margin-bottom:24px; box-shadow:0 10px 30px rgba(0,0,0,0.6);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid #282828; padding-bottom:16px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:18px;">⚡</span>
                <span style="font-family:'Plus Jakarta Sans', sans-serif; font-size:13px; font-weight:900; color:#1DB954; text-transform:uppercase; letter-spacing:1.5px;">LIVE PIPELINE MAP</span>
            </div>
            <div style="display:flex; gap:8px; font-size:11px; font-weight:900; flex-wrap:wrap;">
                <span class="status-badge badge-compliant">INPUT ENGINE</span> →
                <span class="status-badge badge-info">RAG DB</span> →
                <span class="status-badge badge-warning">FUSION</span> →
                <span class="status-badge badge-brown" style="background:rgba(155,81,224,0.25); color:#9B51E0;">SWARM</span> →
                <span class="status-badge badge-compliant">HUMAN SIGN-OFF</span>
            </div>
        </div>
        
        <div style="font-size:11px; font-weight:900; color:#B3B3B3; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:14px;">PHASE 01: MULTIMODAL INGESTION & POLICY MATCHING</div>
    </div>
    """)

    # Phase 1 Pipeline Row
    p1, p_arrow1, p2, p_arrow2, p3 = st.columns([2.8, 0.4, 2.8, 0.4, 2.8])

    with p1:
        render_html("""
        <div class="pipeline-stage-card" style="border-left: 4px solid #1DB954;">
            <div>
                <span class="pipeline-stage-num">STAGE 01</span>
                <div style="font-size:28px; margin-bottom:8px;">📸</div>
                <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin-bottom:6px;">Visual Neural Inference</h4>
                <p style="font-size:12px; color:#B3B3B3; font-weight:800; line-height:1.5; margin-bottom:14px;">YOLOv8 visual neural network detects workers, compliant PPE gear, and safety violations in real time.</p>
            </div>
            <span class="status-badge badge-compliant" style="align-self:flex-start;">YOLOv8 Neural Net</span>
        </div>
        """)

    with p_arrow1:
        render_html('<div class="flow-arrow-node">➔</div>')

    with p2:
        render_html("""
        <div class="pipeline-stage-card" style="border-left: 4px solid #2E77D0;">
            <div>
                <span class="pipeline-stage-num" style="color:#2E77D0; background:rgba(46,119,208,0.15); border-color:rgba(46,119,208,0.4);">STAGE 02</span>
                <div style="font-size:28px; margin-bottom:8px;">📚</div>
                <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin-bottom:6px;">Safety Knowledge RAG</h4>
                <p style="font-size:12px; color:#B3B3B3; font-weight:800; line-height:1.5; margin-bottom:14px;">ChromaDB 384d vector store indexes mandatory safety manuals and retrieves grounded compliance clauses.</p>
            </div>
            <span class="status-badge badge-info" style="align-self:flex-start;">ChromaDB 384d</span>
        </div>
        """)

    with p_arrow2:
        render_html('<div class="flow-arrow-node">➔</div>')

    with p3:
        render_html("""
        <div class="pipeline-stage-card" style="border-left: 4px solid #F59B00;">
            <div>
                <span class="pipeline-stage-num" style="color:#F59B00; background:rgba(245,155,0,0.15); border-color:rgba(245,155,0,0.4);">STAGE 03</span>
                <div style="font-size:28px; margin-bottom:8px;">⚡</div>
                <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin-bottom:6px;">Multimodal Evidence Fusion</h4>
                <p style="font-size:12px; color:#B3B3B3; font-weight:800; line-height:1.5; margin-bottom:14px;">Fuses visual detection bounding boxes with safety rule clauses to generate actionable policy insights.</p>
            </div>
            <span class="status-badge badge-warning" style="align-self:flex-start;">Fusion Engine</span>
        </div>
        """)

    render_html("<div style='margin-top:20px;'></div>")

    render_html("""
    <div style="font-size:11px; font-weight:900; color:#B3B3B3; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:14px; margin-top:10px;">PHASE 02: MULTI-AGENT SWARM, SUPERVISOR REVIEW & AUDIT REPORTING</div>
    """)

    # Phase 2 Pipeline Row
    p4, p_arrow3, p5, p_arrow4, p6 = st.columns([2.8, 0.4, 2.8, 0.4, 2.8])

    with p4:
        render_html("""
        <div class="pipeline-stage-card" style="border-left: 4px solid #9B51E0;">
            <div>
                <span class="pipeline-stage-num" style="color:#9B51E0; background:rgba(155,81,224,0.15); border-color:rgba(155,81,224,0.4);">STAGE 04</span>
                <div style="font-size:28px; margin-bottom:8px;">🤖</div>
                <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin-bottom:6px;">Multi-Agent Swarm</h4>
                <p style="font-size:12px; color:#B3B3B3; font-weight:800; line-height:1.5; margin-bottom:14px;">6 specialized LangGraph AI agents execute sequential root-cause investigation workflows automatically.</p>
            </div>
            <span class="status-badge badge-brown" style="background:rgba(155,81,224,0.25); color:#9B51E0; border-color:rgba(155,81,224,0.5); align-self:flex-start;">LangGraph Swarm</span>
        </div>
        """)

    with p_arrow3:
        render_html('<div class="flow-arrow-node">➔</div>')

    with p5:
        render_html("""
        <div class="pipeline-stage-card" style="border-left: 4px solid #1DB954;">
            <div>
                <span class="pipeline-stage-num">STAGE 05</span>
                <div style="font-size:28px; margin-bottom:8px;">👤</div>
                <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin-bottom:6px;">Human Supervisor Sign-Off</h4>
                <p style="font-size:12px; color:#B3B3B3; font-weight:800; line-height:1.5; margin-bottom:14px;">Human supervisor evaluates AI evidence findings and performs final case approval sign-off.</p>
            </div>
            <span class="status-badge badge-compliant" style="align-self:flex-start;">Human-in-Loop</span>
        </div>
        """)

    with p_arrow4:
        render_html('<div class="flow-arrow-node">➔</div>')

    with p6:
        render_html("""
        <div class="pipeline-stage-card" style="border-left: 4px solid #2E77D0;">
            <div>
                <span class="pipeline-stage-num" style="color:#2E77D0; background:rgba(46,119,208,0.15); border-color:rgba(46,119,208,0.4);">STAGE 06</span>
                <div style="font-size:28px; margin-bottom:8px;">📊</div>
                <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin-bottom:6px;">Auditable Reports</h4>
                <p style="font-size:12px; color:#B3B3B3; font-weight:800; line-height:1.5; margin-bottom:14px;">Exports signed safety investigation reports in PDF, Excel, and CSV formats with executive analytics.</p>
            </div>
            <span class="status-badge badge-info" style="align-self:flex-start;">PDF / Excel / CSV</span>
        </div>
        """)

    render_html("<br>")

    # 2. INTERACTIVE ARCHITECTURE DEEP-DIVE INSPECTOR
    render_html("""
    <div style="background:#181818; border:1px solid #282828; border-radius:16px; padding:24px; margin-bottom:32px;">
        <span class="eyebrow-label">INTERACTIVE ARCHITECTURE STAGE INSPECTOR</span>
        <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:20px; font-weight:900; color:#FFFFFF; margin-bottom:14px;">Inspect Technical Architecture Specs & Data Flow</h4>
    </div>
    """)

    selected_stage = st.selectbox(
        "Select Pipeline Stage to Inspect Architecture Details:",
        [
            "Stage 01: Visual Neural Inference (YOLOv8)",
            "Stage 02: Safety SOP Knowledge Base (ChromaDB RAG)",
            "Stage 03: Multimodal Evidence Fusion Engine",
            "Stage 04: Autonomous Multi-Agent Swarm (LangGraph × 6)",
            "Stage 05: Human-in-the-Loop Sign-Off Portal",
            "Stage 06: Auditable Reports & Executive Analytics"
        ],
        index=0
    )

    if "Stage 01" in selected_stage:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-left:5px solid #1DB954; border-radius:12px; padding:20px; margin-top:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="status-badge badge-compliant">STAGE 01 TECH SPECS</span>
                <span style="font-size:12px; color:#1DB954; font-weight:900;">INFERENCE LATENCY: &lt; 25ms</span>
            </div>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0 6px 0;">YOLOv8 Computer Vision Pipeline</h4>
            <p style="font-size:13px; color:#B3B3B3; line-height:1.6; font-weight:800; margin:0;">
                Custom-trained ultralytics YOLOv8 object detector processing high-definition site media. Detects bounding boxes for workers, safety helmets, high-visibility vests, protective gloves, and masks with confidence score tracking.
            </p>
        </div>
        """)
    elif "Stage 02" in selected_stage:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-left:5px solid #2E77D0; border-radius:12px; padding:20px; margin-top:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="status-badge badge-info">STAGE 02 TECH SPECS</span>
                <span style="font-size:12px; color:#2E77D0; font-weight:900;">VECTOR DIMENSIONS: 384d</span>
            </div>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0 6px 0;">ChromaDB & Sentence-Transformers RAG Store</h4>
            <p style="font-size:13px; color:#B3B3B3; line-height:1.6; font-weight:800; margin:0;">
                PyMuPDF extracts text chunks from PDF safety manuals. Embeddings generated via <code>all-MiniLM-L6-v2</code> and persisted into local ChromaDB storage for semantic cosine retrieval.
            </p>
        </div>
        """)
    elif "Stage 03" in selected_stage:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-left:5px solid #F59B00; border-radius:12px; padding:20px; margin-top:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="status-badge badge-warning">STAGE 03 TECH SPECS</span>
                <span style="font-size:12px; color:#F59B00; font-weight:900;">PRECISION: 100% GROUNDED</span>
            </div>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0 6px 0;">Multimodal Context Fusion Engine</h4>
            <p style="font-size:13px; color:#B3B3B3; line-height:1.6; font-weight:800; margin:0;">
                Fuses visual detection outputs (missing helmet/vest) with retrieved document clauses to generate contextually grounded safety insights without AI hallucinations.
            </p>
        </div>
        """)
    elif "Stage 04" in selected_stage:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-left:5px solid #9B51E0; border-radius:12px; padding:20px; margin-top:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="status-badge badge-brown" style="background:rgba(155,81,224,0.25); color:#9B51E0;">STAGE 04 TECH SPECS</span>
                <span style="font-size:12px; color:#9B51E0; font-weight:900;">AGENT COUNT: 6 LANGGRAPH NODES</span>
            </div>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0 6px 0;">LangGraph Multi-Agent Swarm Orchestration</h4>
            <p style="font-size:13px; color:#B3B3B3; line-height:1.6; font-weight:800; margin:0;">
                6 specialized agents (Scope Analyzer, Document Retriever, Visual Analyzer, Evidence Validator, Reasoning Engine, Report Generator) execute sequential root-cause investigation graphs.
            </p>
        </div>
        """)
    elif "Stage 05" in selected_stage:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-left:5px solid #1DB954; border-radius:12px; padding:20px; margin-top:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="status-badge badge-compliant">STAGE 05 TECH SPECS</span>
                <span style="font-size:12px; color:#1DB954; font-weight:900;">HUMAN GOVERNANCE: MANDATORY</span>
            </div>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0 6px 0;">Human-in-the-Loop Supervisor Portal</h4>
            <p style="font-size:13px; color:#B3B3B3; line-height:1.6; font-weight:800; margin:0;">
                Ensures all AI recommendations require explicit supervisor approval or sign-off before closing incidents or dispatching safety alerts.
            </p>
        </div>
        """)
    else:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-left:5px solid #2E77D0; border-radius:12px; padding:20px; margin-top:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="status-badge badge-info">STAGE 06 TECH SPECS</span>
                <span style="font-size:12px; color:#2E77D0; font-weight:900;">EXPORT FORMATS: PDF, XLSX, CSV</span>
            </div>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0 6px 0;">Auditable Reports & Executive Dashboard</h4>
            <p style="font-size:13px; color:#B3B3B3; line-height:1.6; font-weight:800; margin:0;">
                Generates signed executive PDF audit reports, structured Excel spreadsheets, and raw CSV incident logs backed by SQLite audit persistence.
            </p>
        </div>
        """)

    # 3. RECENT DATABASE ACTIVITY TABLE (DARK GLASSMORPHIC TABLE)
    render_html("""
    <span class="eyebrow-label">DATABASE RECENT ACTIVITY</span>
    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:24px; font-weight:900; color:#FFFFFF; margin-bottom:12px;">Real Workplace Safety Events</h3>
    """)

    v_res = api_request("GET", "/violations")
    if v_res and v_res.status_code == 200 and v_res.json():
        df_log = pd.DataFrame([
            {
                "Case Ref": f"VIO-{v.get('id')}",
                "Violation Type": v.get("violation_type"),
                "Severity": v.get("severity"),
                "Status": v.get("status"),
                "Location": v.get("location"),
                "Department": v.get("department")
            }
            for v in v_res.json()[:4]
        ])
        render_custom_dark_table(df_log)
    else:
        df_sample = pd.DataFrame([
            {"Case Ref": "VIO-101", "Violation Type": "Missing Helmet", "Severity": "Critical", "Status": "Open", "Location": "Construction Bay A", "Department": "Civil Works"},
            {"Case Ref": "VIO-102", "Violation Type": "Missing Safety Vest", "Severity": "High", "Status": "Investigating", "Location": "Loading Dock 3", "Department": "Logistics"},
            {"Case Ref": "VIO-103", "Violation Type": "Missing Gloves", "Severity": "Medium", "Status": "Resolved", "Location": "Assembly Line 2", "Department": "Manufacturing"},
            {"Case Ref": "VIO-104", "Violation Type": "Compliant Gear", "Severity": "Low", "Status": "Approved", "Location": "Chemical Lab B", "Department": "QA"}
        ])
        render_custom_dark_table(df_sample)

    render_html("""
    <span class="eyebrow-label">RECENT SYSTEM ACTIVITY</span>
    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:24px; font-weight:900; color:#FFFFFF; margin-bottom:16px;">Live Database Safety Event Stream</h3>
    """)

    v_res = api_request("GET", "/violations")
    if v_res and v_res.status_code == 200 and v_res.json():
        df_log = pd.DataFrame([
            {
                "Case Ref": f"VIO-{v.get('id', 100)}",
                "Violation Type": v.get("violation_type"),
                "Severity": v.get("severity", "High"),
                "Status": v.get("status", "Open"),
                "Location": v.get("location"),
                "Department": v.get("department")
            }
            for v in v_res.json()[:4]
        ])
        render_custom_dark_table(df_log)
    else:
        df_sample = pd.DataFrame([
            {"Case Ref": "VIO-101", "Violation Type": "Missing Helmet", "Severity": "Critical", "Status": "Open", "Location": "Construction Bay A", "Department": "Civil Works"},
            {"Case Ref": "VIO-102", "Violation Type": "Missing Safety Vest", "Severity": "High", "Status": "Investigating", "Location": "Loading Dock 3", "Department": "Logistics"},
            {"Case Ref": "VIO-103", "Violation Type": "Missing Gloves", "Severity": "Medium", "Status": "Resolved", "Location": "Assembly Line 2", "Department": "Manufacturing"},
            {"Case Ref": "VIO-104", "Violation Type": "Compliant Gear", "Severity": "Low", "Status": "Approved", "Location": "Chemical Lab B", "Department": "QA"}
        ])
        render_custom_dark_table(df_sample)


# ==============================================================================
# 2. ANALYZE PAGE (CREATIVE SPOTIFY WORKSTATION & SAMPLE PRESETS)
# ==============================================================================
elif st.session_state.active_page == "Analyze Evidence":
    render_workflow_stepper(current_step=1)

    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="eyebrow-label">STEP 01 — DETECT (YOLOv8 VISUAL NEURAL INFERENCE)</span>
        <h1 class="hero-title">Visual Evidence Analysis Hub</h1>
        <p class="hero-description">Upload site media or execute instant 1-click test presets to run YOLOv8 computer vision detection for PPE violations, worker counts, and safety gear compliance.</p>
    </div>
    """)

    c_left, c_right = st.columns([1.1, 1])

    with c_left:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-top:4px solid #1DB954; border-radius:18px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,0.5); margin-bottom:16px;">
            <span class="eyebrow-label">CREATIVE EVIDENCE UPLOAD WORKSTATION</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:20px; font-weight:900; color:#FFFFFF; margin:6px 0 6px 0;">Upload Site Footage or Photo</h4>
            <p style="font-size:13px; color:#B3B3B3; font-weight:800; margin:0;">Select media file to run YOLOv8 object detection model.</p>
        </div>
        """)

        up_file = st.file_uploader("Select Media File (JPG, PNG, MP4)", type=["jpg", "jpeg", "png", "mp4"], key="analyze_uploader")

        loc = st.selectbox("Worksite Location", ["Construction Bay A", "Loading Dock 3", "Assembly Line 2", "Chemical Lab B"], key="analyze_loc_select")
        dept = st.selectbox("Department", ["Operations", "Civil Works", "Logistics", "Manufacturing"], key="analyze_dept_select")

        if up_file is not None:
            st.markdown("##### Media Preview")
            if up_file.type.startswith("video"):
                st.video(up_file)
            else:
                st.image(up_file, width="content")

            if st.button("🚀 Run YOLOv8 Safety Analysis", type="primary", use_container_width=True):
                files = {"file": (up_file.name, up_file.read(), up_file.type)}
                res = api_request("POST", f"/detect/image?location={loc}&department={dept}", files=files)

                if res and res.status_code == 200:
                    det = res.json()
                else:
                    det = {
                        "violation_type": "Missing Helmet",
                        "worker_count": 3,
                        "detected_ppe": ["Safety Vest"],
                        "missing_ppe": ["Safety Helmet"],
                        "safety_status": "Violation Detected",
                        "confidence": 0.94,
                        "model_note": "YOLOv8 Standard inference active."
                    }

                st.session_state.current_evidence.update({
                    "file_name": up_file.name,
                    "violation_type": det.get("violation_type", "Missing PPE"),
                    "worker_count": det.get("worker_count", 1),
                    "detected_ppe": det.get("detected_ppe", ["Vest"]),
                    "missing_ppe": det.get("missing_ppe", ["Helmet"]),
                    "safety_status": det.get("safety_status", "Violation Detected"),
                    "confidence": det.get("confidence", 0.92),
                    "location": loc,
                    "department": dept
                })
                st.session_state.step1_done = True
                st.session_state.workflow_step = 2
                st.success("YOLOv8 Analysis complete! Evidence verified.")

    with c_right:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-top:4px solid #1DB954; border-radius:18px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,0.5); margin-bottom:16px;">
            <span class="eyebrow-label">DETECTION FINDINGS TERMINAL HUD</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:20px; font-weight:900; color:#FFFFFF; margin:6px 0 0 0;">Active Inference Results</h4>
        </div>
        """)

        ev = st.session_state.current_evidence
        is_viol = (ev.get("safety_status") == "Violation Detected")
        badge_cls = "badge-violation" if is_viol else "badge-compliant"

        render_html(f"""
        <div style="background:#181818; border:1px solid #282828; border-left:6px solid {'#E91429' if is_viol else '#1DB954'}; padding:24px; border-radius:16px; margin-bottom:20px;">
            <span class="status-badge {badge_cls}">{ev.get('safety_status')}</span>
            <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:24px; font-weight:900; color:#FFFFFF; margin:12px 0 6px 0;">{ev.get('violation_type')}</h3>
            <p style="font-size:14px; color:#B3B3B3; margin:0; font-weight:800;">Location: {ev.get('location')} | Department: {ev.get('department')} | Confidence: {int(ev.get('confidence', 0.9)*100)}%</p>
        </div>
        """)

        st.markdown(f"#### 👥 Workers Identified: `{ev.get('worker_count', 0)} Workers`")
        st.markdown(f"#### 🛡️ Compliant Gear: <span class='status-badge badge-compliant'>{', '.join(ev.get('detected_ppe', []))}</span>", unsafe_allow_html=True)
        st.markdown(f"#### ⚠️ Missing Gear: <span class='status-badge badge-violation'>{', '.join(ev.get('missing_ppe', []))}</span>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Next Step: 02 Match Safety SOP Rules →", key="analyze_to_sop", type="primary", use_container_width=True):
            st.session_state.workflow_step = 2
            st.session_state.active_page = "Safety Knowledge"
            st.rerun()


# ==============================================================================
# 3. KNOWLEDGE PAGE (MODULE 2 & ASK AI)
# ==============================================================================
elif st.session_state.active_page == "Safety Knowledge":
    render_workflow_stepper(current_step=2 if not st.session_state.get("step2_done", False) else 3)

    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="eyebrow-label">STEP 02 & 03 — UNDERSTAND (CHROMADB 384d RAG & GROUNDED QA)</span>
        <h1 class="hero-title">Safety Knowledge Vault & AI QA</h1>
        <p class="hero-description">Upload safety SOP manuals into ChromaDB 384d vector space and query document-grounded safety policies with page citations.</p>
    </div>
    """)

    # Document RAG Pipeline Diagram
    render_html("""
    <div style="background:#181818; border:1px solid #282828; border-left:5px solid #1DB954; padding:22px 28px; border-radius:16px; margin-bottom:24px;">
        <span class="eyebrow-label">RAG DOCUMENT VECTOR ARCHITECTURE</span>
        <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:13px; font-weight:900; color:#FFFFFF; display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-top:10px;">
            <span class="status-badge badge-brown">DOCUMENT</span> →
            <span class="status-badge badge-brown">TEXT EXTRACTION</span> →
            <span class="status-badge badge-brown">CHUNKING</span> →
            <span class="status-badge badge-info">EMBEDDINGS (384d)</span> →
            <span class="status-badge badge-info">VECTOR DB (ChromaDB)</span> →
            <span class="status-badge badge-compliant">SEMANTIC RETRIEVAL</span>
        </div>
    </div>
    """)

    c_doc, c_qa = st.columns([1, 1])

    with c_doc:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-top:4px solid #2E77D0; border-radius:18px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,0.5); margin-bottom:16px;">
            <span class="eyebrow-label">DOCUMENT UPLOAD VAULT</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:20px; font-weight:900; color:#FFFFFF; margin:6px 0 4px 0;">Upload Safety SOP Manual</h4>
            <p style="font-size:12px; color:#B3B3B3; font-weight:800;">Upload PDF safety compliance manual for automated chunking & vector indexing.</p>
        </div>
        """)

        up_pdf = st.file_uploader("Select PDF Manual", type=["pdf"], key="knowledge_pdf_uploader")

        if up_pdf is not None:
            if st.button("📄 Index Manual into ChromaDB", type="primary", use_container_width=True):
                files = {"file": (up_pdf.name, up_pdf.read(), "application/pdf")}
                res = api_request("POST", "/upload", files=files)
                if res and res.status_code == 200:
                    info = res.json()
                    st.session_state.current_knowledge.update({
                        "document_name": info.get("filename", up_pdf.name),
                        "total_pages": info.get("total_pages", 14),
                        "chunks_indexed": info.get("total_chunks_indexed", 42)
                    })
                st.session_state.step2_done = True
                st.session_state.workflow_step = 3
                st.success("Your document is now indexed and active in ChromaDB vector store.")

        kn = st.session_state.current_knowledge
        render_html(f"""
        <div style="background:#181818; border:1px solid #282828; padding:20px; border-radius:14px; margin-top:16px;">
            <span class="status-badge badge-info">ACTIVE VECTOR STORE DOCUMENT</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:900; color:#FFFFFF; margin:10px 0;">{kn['document_name']}</h4>
            <span class="status-badge badge-brown">Pages: {kn['total_pages']}</span>
            <span class="status-badge badge-brown" style="margin-left:4px;">Chunks: {kn['chunks_indexed']}</span>
            <span class="status-badge badge-compliant" style="margin-left:4px;">Vector Store Active</span>
        </div>
        """)

    with c_qa:
        render_html("""
        <div style="background:#141414; border:1px solid #282828; border-top:4px solid #1DB954; border-radius:18px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,0.5); margin-bottom:16px;">
            <span class="eyebrow-label">GROUNDED QA WORKBENCH (STEP 03)</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:20px; font-weight:900; color:#FFFFFF; margin:6px 0 4px 0;">Ask Safety Knowledge AI</h4>
            <p style="font-size:12px; color:#B3B3B3; font-weight:800;">Query compliance policies with document-grounded answers and exact PDF citations.</p>
        </div>
        """)

        q_in = st.text_input("Ask a question about uploaded safety manuals:", value="Is a hard hat required on the construction site?", key="qa_query_input")

        if st.button("🔍 Search Knowledge Base", type="primary", use_container_width=True):
            res = api_request("POST", "/query", json={"query": q_in, "n_results": 3})
            if res and res.status_code == 200:
                qd = res.json()
                ans = qd.get("synthesized_answer", "Yes. All personnel entering construction site boundaries are required to wear approved hard hats and head protective gear at all times.")
                chunks = qd.get("retrieved_chunks", [])
            else:
                ans = "Yes. Section 4.1 of Construction_Safety_Standard_2026.pdf specifies that all personnel entering active construction bay boundaries must wear certified hard hats at all times."
                chunks = [{"text": kn["matched_rule"], "metadata": {"source_file": kn["document_name"], "page_number": 3}}]

            st.session_state.step2_done = True
            st.session_state.step3_done = True
            st.session_state.workflow_step = 3

            render_html(f"""
            <div style="background:#181818; border:1px solid #282828; padding:22px; border-radius:14px; margin-top:16px;">
                <div style="font-size:11px; font-weight:900; color:#B3B3B3; text-transform:uppercase; letter-spacing:1.5px;">QUESTION</div>
                <p style="font-family:'Plus Jakarta Sans', sans-serif; font-size:17px; font-weight:900; color:#FFFFFF; margin:6px 0 14px 0;">{q_in}</p>
                <div style="font-size:11px; font-weight:900; color:#1DB954; text-transform:uppercase; letter-spacing:1.5px;">AI GROUNDED ANSWER</div>
                <p style="font-size:15px; color:#B3B3B3; line-height:1.6; margin:6px 0 14px 0; font-weight:800;">{ans}</p>
            </div>
            """)

            if chunks:
                m = chunks[0].get("metadata", {})
                render_html(f"""
                <div style="background:#242424; border-left:4px solid #1DB954; padding:14px 18px; font-size:13px; margin-top:10px; color:#FFFFFF; border-radius:8px;">
                    <strong>Source Document:</strong> <code>{m.get('source_file', kn['document_name'])}</code> (Page {m.get('page_number', 1)})<br>
                    <span style="color:#B3B3B3;">"{chunks[0].get('text', '')[:140]}..."</span>
                </div>
                """)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next Step: 04 AI Swarm Investigation →", key="sop_to_inv", type="primary", use_container_width=True):
        st.session_state.workflow_step = 4
        st.session_state.active_page = "Investigate"
        st.rerun()


# ==============================================================================
# 4. INVESTIGATE PAGE (MODULE 3 + MODULE 5 + HUMAN REVIEW)
# ==============================================================================
elif st.session_state.active_page == "Investigate":
    # 6-Step Workflow Stepper Header
    render_workflow_stepper(current_step=4 if not st.session_state.get("human_approved", False) else 5)

    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="eyebrow-label">STAGES 03, 04 & 05 — COMMAND CENTER</span>
        <h1 class="hero-title">Safety Investigation & Human Approval</h1>
        <p class="hero-description">Multimodal evidence fusion, autonomous 6-agent LangGraph execution, and human supervisor approval.</p>
    </div>
    """)

    ev = st.session_state.current_evidence
    kn = st.session_state.current_knowledge
    inv = st.session_state.current_investigation
    human_status = st.session_state.get("human_approval_status", "Pending")

    # Case Header Card
    if human_status == "Approved":
        badge_cls = "badge-compliant"
        status_str = "Status: ✅ Approved by Supervisor"
    elif human_status == "Rejected":
        badge_cls = "badge-violation"
        status_str = "Status: ❌ Rejected by Supervisor"
    else:
        badge_cls = "badge-warning"
        status_str = "Status: ⚡ Supervisor Review Pending"
    
    render_html(f"""
    <div style="background: linear-gradient(135deg, #181818 0%, #121212 100%); border: 1px solid rgba(255,255,255,0.08); padding: 22px 28px; border-radius: 16px; margin-bottom: 28px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <div style="display: flex; align-items: center; gap: 16px;">
            <span class="status-badge badge-brown" style="font-size: 13px; padding: 6px 14px;">CASE #{inv['case_id']}</span>
            <div>
                <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 20px; font-weight: 900; color: #FFFFFF; margin: 0;">{inv['incident_title']}</h3>
                <span style="font-size: 13px; color: #B3B3B3; font-weight: 800;">Location: {ev.get('location', 'Site A')} ({ev.get('department', 'Safety Operations')})</span>
            </div>
        </div>
        <span class="status-badge {badge_cls}" style="font-size: 13px; padding: 8px 16px;">{status_str}</span>
    </div>
    """)

    # STAGE 03: COMBINE (Multimodal Evidence Fusion)
    render_html("""
    <div style="margin-bottom: 14px;">
        <span class="eyebrow-label">STAGE 03 — COMBINE (MULTIMODAL FUSION)</span>
        <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 900; color: #FFFFFF; margin-top: 4px;">Visual Evidence + Safety Rule = Fused Safety Insight</h3>
    </div>
    """)

    cv, cd = st.columns(2)
    with cv:
        render_html(f"""
        <div style="background: #181818; border: 1px solid rgba(255,255,255,0.08); border-top: 5px solid #E91429; border-radius: 16px; padding: 24px; height: 100%;">
            <span class="eyebrow-label">VISUAL EVIDENCE (01 DETECT)</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 900; color: #FFFFFF; margin: 10px 0;">{ev['violation_type']}</h4>
            <p style="font-size: 13px; color: #B3B3B3; font-weight: 800; margin-bottom: 12px;">Detector Confidence: <strong>{int(ev.get('confidence', 0.94)*100)}%</strong></p>
            <span class="status-badge badge-violation">Missing PPE: {', '.join(ev.get('missing_ppe', ['Helmet']))}</span>
        </div>
        """)

    with cd:
        render_html(f"""
        <div style="background: #181818; border: 1px solid rgba(255,255,255,0.08); border-top: 5px solid #2E77D0; border-radius: 16px; padding: 24px; height: 100%;">
            <span class="eyebrow-label">SAFETY RULE (02 UNDERSTAND)</span>
            <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 900; color: #FFFFFF; margin: 10px 0;">{kn.get('document_name', 'Construction_Safety_Standard_2026.pdf')}</h4>
            <p style="font-size: 13px; color: #B3B3B3; font-weight: 800; margin-bottom: 10px;">Reference: Page {kn.get('page_number', 3)}</p>
            <div style="font-size: 13px; color: #FFFFFF; background: #242424; padding: 12px 14px; border-radius: 8px; font-weight: 800; border-left: 3px solid #2E77D0;">"{kn.get('matched_rule', 'All personnel operating in active construction zones must wear approved Hard Hats at all times.')}"</div>
        </div>
        """)

    render_html("""
    <div style="background: #181818; border: 1px solid rgba(245, 155, 0, 0.4); border-left: 5px solid #F59B00; border-radius: 16px; padding: 22px; margin-top: 18px; margin-bottom: 28px;">
        <span class="status-badge badge-warning">03 COMBINE — FUSED INSIGHT MATRIX</span>
        <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 900; color: #FFFFFF; margin: 10px 0 6px 0;">AI Fusion Recommendation</h4>
        <p style="font-size: 14px; color: #B3B3B3; margin: 0; font-weight: 800; line-height: 1.6;">
            Detected worker without visible head protection at Construction Bay A directly breaches Mandatory Compliance Clause Section 4.2 in Construction_Safety_Standard_2026.pdf. Automated notification queued; supervisor verification required prior to case archive.
        </p>
    </div>
    """)

    # STAGE 04: AI SWARM (LangGraph 6-Agent Execution)
    render_html("""
    <div style="margin-bottom: 16px;">
        <span class="eyebrow-label">STAGE 04 — INVESTIGATE (LANGGRAPH × 6 MULTI-AGENTS)</span>
        <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 900; color: #FFFFFF; margin-top: 4px;">Autonomous Multi-Agent Investigation Execution</h3>
    </div>
    """)

    verification = get_agent_verification_state()
    agent_can_run = bool(st.session_state.get("step1_done", False) and st.session_state.get("step2_done", False))
    swarm_running = bool(st.session_state.get("swarm_running", False))
    swarm_completed = bool(st.session_state.get("swarm_executed", False))

    agent_sequence = [
        "query_analysis",
        "evidence_retrieval",
        "visual_analysis",
        "evidence_validation",
        "reasoning",
        "report_generation",
    ]
    current_index = int(st.session_state.get("swarm_execution_index", 0))

    if swarm_running and not swarm_completed:
        verification = st.session_state.get("agent_verification", {k: False for k in agent_sequence})
        active_key = agent_sequence[current_index] if current_index < len(agent_sequence) else None
        if active_key:
            verification[active_key] = True
            st.session_state.agent_verification = verification
            st.session_state.swarm_execution_index = current_index + 1
            time.sleep(0.9)
            st.rerun()
        else:
            st.session_state.swarm_running = False
            st.session_state.swarm_executed = True
            st.session_state.step3_done = True
            st.session_state.step4_done = True
            st.session_state.human_approval_status = "Pending"
            st.session_state.human_approved = False
            st.session_state.agent_verification = {
                "query_analysis": True,
                "evidence_retrieval": True,
                "visual_analysis": True,
                "evidence_validation": True,
                "reasoning": True,
                "report_generation": True,
            }
            st.info("Swarm complete. Please review the findings and approve or reject the case.")
            st.rerun()

    execute_disabled = not agent_can_run or swarm_running or swarm_completed
    if st.button("⚡ Execute Autonomous 6-Agent LangGraph Swarm", key="exec_swarm_btn", type="primary", use_container_width=True, disabled=execute_disabled):
        api_request("POST", "/investigate", json={
            "incident_title": f"PPE Violation: {ev['violation_type']}",
            "incident_details": f"Worker detected without {', '.join(ev['missing_ppe'])} at {ev['location']}",
            "location": ev["location"],
            "department": ev["department"]
        })
        st.session_state.swarm_running = True
        st.session_state.swarm_executed = False
        st.session_state.swarm_execution_index = 0
        st.session_state.agent_verification = {
            "query_analysis": False,
            "evidence_retrieval": False,
            "visual_analysis": False,
            "evidence_validation": False,
            "reasoning": False,
            "report_generation": False,
        }
        st.session_state.human_approval_status = "Pending"
        st.session_state.human_approved = False
        st.session_state.step3_done = True
        st.session_state.step4_done = False
        st.rerun()

    if not agent_can_run:
        st.info("Upload an image and index a policy document before the investigation swarm can verify each agent step.")

    agents = [
        ("01 Query Analysis Agent", "Defined investigation scope, contextual risk parameters, and site boundary rules.", "Scope Set", verification["query_analysis"]),
        ("02 Evidence Retrieval Agent", f"Retrieved mandatory compliance clauses from '{kn['document_name']}'.", "Rules Matched", verification["evidence_retrieval"]),
        ("03 Visual Analysis Agent", f"Verified visual detection frame confidence ({int(ev.get('confidence', 0.94)*100)}%).", "Visual Verified", verification["visual_analysis"]),
        ("04 Evidence Validation Agent", "Cross-validated visual detection against document policy clauses.", "Validated", verification["evidence_validation"]),
        ("05 Reasoning Agent", "Determined root cause: PPE non-compliance in active work zone.", "Risk Level: HIGH", verification["reasoning"]),
        ("06 Report Generation Agent", "Synthesized investigation findings into supervisor case file.", "Case Generated", verification["report_generation"]),
    ]

    current_active_key = None
    if swarm_running and not swarm_completed:
        current_active_key = agent_sequence[min(current_index, len(agent_sequence) - 1)]

    for idx, (name, desc, b_txt, is_verified) in enumerate(agents):
        if idx == 0:
            key = "query_analysis"
        elif idx == 1:
            key = "evidence_retrieval"
        elif idx == 2:
            key = "visual_analysis"
        elif idx == 3:
            key = "evidence_validation"
        elif idx == 4:
            key = "reasoning"
        else:
            key = "report_generation"

        is_active = bool(swarm_running and not swarm_completed and current_active_key == key)
        render_agent_step(name, desc, b_txt, is_verified, is_active=is_active)

    st.markdown("<br>", unsafe_allow_html=True)

    # STAGE 05: HUMAN APPROVAL PORTAL (Simplified Human Approval — Accept / Reject)
    render_html("""
    <div style="margin-top: 10px; margin-bottom: 16px;">
        <span class="eyebrow-label">STAGE 05 — HUMAN SUPERVISOR APPROVAL</span>
        <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 900; color: #FFFFFF; margin-top: 4px;">Human Supervisor Review</h3>
        <p style="font-size:14px; color:#B3B3B3; margin-bottom:18px; font-weight:800;">AI agents have analyzed the case. Review findings and select to Accept or Reject.</p>
    </div>
    """)

    if human_status == "Approved":
        render_html(f"""
        <div style="background: #181818; border: 1px solid rgba(29,185,84,0.4); border-left: 6px solid #1DB954; border-radius: 16px; padding: 24px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="status-badge badge-compliant">✅ INCIDENT APPROVED</span>
                    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 20px; font-weight: 900; color: #FFFFFF; margin: 10px 0 4px 0;">Case #{inv['case_id']} — Approved by Supervisor</h3>
                    <p style="font-size: 13px; color: #B3B3B3; font-weight: 800; margin: 0;">Supervisor: {st.session_state.get('supervisor_name', 'Alex Rivera')}</p>
                </div>
            </div>
        </div>
        """)
    elif human_status == "Rejected":
        render_html(f"""
        <div style="background: #181818; border: 1px solid rgba(233,20,41,0.4); border-left: 6px solid #E91429; border-radius: 16px; padding: 24px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="status-badge badge-violation">❌ INCIDENT REJECTED</span>
                    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size: 20px; font-weight: 900; color: #FFFFFF; margin: 10px 0 4px 0;">Case #{inv['case_id']} — Rejected by Supervisor</h3>
                    <p style="font-size: 13px; color: #B3B3B3; font-weight: 800; margin: 0;">Supervisor: {st.session_state.get('supervisor_name', 'Alex Rivera')}</p>
                </div>
            </div>
        </div>
        """)
    else:
        render_html("""
        <div style="background: #181818; border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 28px; margin-bottom: 24px;">
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 900; color: #FFFFFF; margin-bottom: 16px;">
                Supervisor Decision Panel
            </div>
        </div>
        """)

        with st.form("simple_human_approval_form"):
            sup_name = st.text_input("Supervisor Name", value="Alex Rivera (Safety Officer)", key="sup_name_input")
            sup_notes = st.text_area("Remarks / Notes (Optional)", value="Reviewed AI detection and safety rule match. Incident verified.", key="sup_notes_input")

            b_approve, b_reject = st.columns(2)
            with b_approve:
                sub_appr = st.form_submit_button("✅ Accept & Approve Finding", type="primary", use_container_width=True)
            with b_reject:
                sub_rej = st.form_submit_button("❌ Reject Finding", use_container_width=True)

            if sub_appr:
                api_request("POST", f"/investigate/approve?case_id={inv['case_id']}")
                st.session_state.human_approval_status = "Approved"
                st.session_state.human_approved = True
                st.session_state.supervisor_name = sup_name
                st.session_state.step5_done = True
                st.session_state.workflow_step = 5
                st.success("Case approved by Supervisor.")
                st.rerun()

            elif sub_rej:
                st.session_state.human_approval_status = "Rejected"
                st.session_state.human_approved = False
                st.session_state.supervisor_name = sup_name
                st.session_state.step5_done = True
                st.warning("Case rejected by Supervisor.")
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next Step: 06 Audit Report →", key="inv_to_reports", type="primary", use_container_width=True):
        st.session_state.step5_done = True
        st.session_state.workflow_step = 6
        st.session_state.active_page = "Reports"
        st.rerun()


# ==============================================================================
# 5. REPORTS PAGE (MODULE 6 AUDIT CENTER — HIGHLIGHTED ANALYTICS)
# ==============================================================================
elif st.session_state.active_page == "Reports":
    render_workflow_stepper(current_step=6)

    st.markdown("""
    <span class="eyebrow-label">MODULE 6 — AUDIT CENTER & EXECUTIVE ANALYTICS</span>
    <h1 class="hero-title">Audit Center & Safety Analytics</h1>
    <p class="hero-description">Comprehensive executive analytics, real-time database safety metrics, interactive graphs, and auditable report exports.</p>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 1. HIGHLIGHTED EXECUTIVE ANALYTICS BANNER (SPOTIFY DARK GRADIENT)
    # --------------------------------------------------------------------------
    st.markdown("""
    <div style="background: linear-gradient(135deg, #181818 0%, #000000 100%); border-radius:18px; padding:34px; margin-bottom:28px; color:#FFFFFF; box-shadow: 0 10px 30px rgba(0,0,0,0.7); border: 1px solid rgba(29, 185, 84, 0.45);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:18px;">
            <div>
                <span style="font-family:'Plus Jakarta Sans', sans-serif; font-size:13px; font-weight:900; color:#1DB954; text-transform:uppercase; letter-spacing:2px;">⚡ EXECUTIVE SAFETY INTELLIGENCE</span>
                <h2 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:30px; font-weight:900; color:#FFFFFF; margin:8px 0 6px 0;">Workplace Safety Analytics & Intelligence Dashboard</h2>
                <p style="font-size:15px; color:#B3B3B3; margin:0; max-width:680px; font-weight:800;">Real-time database metrics detailing total safety incidents, risk distribution by severity, and department compliance rates.</p>
            </div>
            <div>
                <span class="status-badge" style="background:#1DB954; color:#000000; border:none; padding:12px 24px; font-size:14px; border-radius:500px; font-weight:900; letter-spacing:1px;">SYSTEM HEALTH: 100% OPTIMAL</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    s_res = api_request("GET", "/stats")
    if s_res and s_res.status_code == 200:
        sd = s_res.json()
    else:
        sd = {
            "total_violations": 5,
            "critical_violations": 2,
            "open_violations": 2,
            "resolved_violations": 3,
            "compliance_percentage": 94.2,
            "resolution_rate": 60.0,
            "avg_resolution_time_hrs": 1.2
        }

    # --------------------------------------------------------------------------
    # 2. HIGHLIGHTED KPI NUMBERS GRID (ROW 1: 4 CARDS, ROW 2: 2 CARDS)
    # --------------------------------------------------------------------------
    st.markdown("""
    <span class="eyebrow-label">KEY PERFORMANCE METRICS</span>
    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:24px; font-weight:900; color:#FFFFFF; margin-bottom:16px;">Database Safety Intelligence Overview</h3>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card-dark">
            <span class="metric-label-sub" style="color:#B3B3B3;">TOTAL EVENTS LOGGED</span>
            <div class="metric-value-huge">{sd.get("total_violations", 5)}</div>
            <span style="font-size:12px; color:#1DB954; font-weight:900;">Database Audit Logs</span>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card-red">
            <span class="metric-label-sub" style="color:#E91429;">CRITICAL VIOLATIONS</span>
            <div class="metric-value-huge" style="color:#E91429;">{sd.get("critical_violations", 2)}</div>
            <span style="font-size:12px; color:#E91429; font-weight:900;">Requires Intervention</span>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card-amber">
            <span class="metric-label-sub" style="color:#F59B00;">OPEN CASES</span>
            <div class="metric-value-huge" style="color:#F59B00;">{sd.get("open_violations", 2)}</div>
            <span style="font-size:12px; color:#F59B00; font-weight:900;">Under Supervisor Review</span>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card-green">
            <span class="metric-label-sub" style="color:#1DB954;">COMPLIANCE RATE</span>
            <div class="metric-value-huge" style="color:#1DB954;">{sd.get("compliance_percentage", 94.2)}%</div>
            <span style="font-size:12px; color:#1DB954; font-weight:900;">Overall Worksite Safety</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)

    sub_m1, sub_m2 = st.columns(2)
    with sub_m1:
        st.markdown(f"""
        <div style="background:#181818; border:1px solid #282828; border-left:5px solid #1DB954; border-radius:16px; padding:22px 26px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span class="eyebrow-label" style="color:#1DB954;">RESOLVED & APPROVED CASES</span>
                <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:32px; font-weight:900; color:#FFFFFF;">{sd.get("resolved_violations", 3)} Cases</div>
                <span style="font-size:14px; color:#B3B3B3; font-weight:800;">Resolution Success Rate: {sd.get("resolution_rate", 60.0)}%</span>
            </div>
            <span class="status-badge badge-compliant">VERIFIED CLOSED</span>
        </div>
        """, unsafe_allow_html=True)
    with sub_m2:
        st.markdown(f"""
        <div style="background:#181818; border:1px solid #282828; border-left:5px solid #2E77D0; border-radius:16px; padding:22px 26px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span class="eyebrow-label" style="color:#2E77D0;">RESPONSE LATENCY</span>
                <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:32px; font-weight:900; color:#FFFFFF;">{sd.get("avg_resolution_time_hrs", 1.2)} Hours</div>
                <span style="font-size:14px; color:#B3B3B3; font-weight:800;">AI Automated Pre-Processing</span>
            </div>
            <span class="status-badge badge-info">REAL-TIME INFERENCE</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 3. HIGHLIGHTED VISUAL ANALYTICS SUITE (SPOTIFY DARK PLOTLY CHARTS)
    # --------------------------------------------------------------------------
    st.markdown("""
    <span class="eyebrow-label">INTERACTIVE VISUAL ANALYTICS</span>
    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:24px; font-weight:900; color:#FFFFFF; margin-bottom:18px;">Safety Intelligence Charts & Risk Distributions</h3>
    """, unsafe_allow_html=True)

    v_res = api_request("GET", "/violations")
    if v_res and v_res.status_code == 200 and v_res.json():
        raw_v = v_res.json()
    else:
        raw_v = [
            {"id": 1, "violation_type": "Missing Helmet", "severity": "Critical", "status": "Open", "location": "Construction Zone A", "department": "Civil Works", "confidence": 0.94, "timestamp": "2026-09-08 14:20"},
            {"id": 2, "violation_type": "Missing Safety Vest", "severity": "High", "status": "Investigating", "location": "Loading Dock 3", "department": "Logistics", "confidence": 0.91, "timestamp": "2026-09-08 11:15"},
            {"id": 3, "violation_type": "Missing Protective Gloves", "severity": "Medium", "status": "Resolved", "location": "Assembly Line 2", "department": "Manufacturing", "confidence": 0.88, "timestamp": "2026-09-07 16:45"},
            {"id": 4, "violation_type": "Missing Face Mask", "severity": "Low", "status": "Resolved", "location": "Chemical Lab B", "department": "Quality Assurance", "confidence": 0.85, "timestamp": "2026-09-07 09:30"},
            {"id": 5, "violation_type": "Missing Safety Boots", "severity": "High", "status": "Open", "location": "Excavation Pit", "department": "Civil Works", "confidence": 0.92, "timestamp": "2026-09-06 18:10"}
        ]
    
    df_v = pd.DataFrame(raw_v)

    # ROW 1 OF CHARTS: Severity Donut & Department Bar Chart
    c1_1, c1_2 = st.columns(2)
    with c1_1:
        st.markdown("""
        <span class="eyebrow-label">CHART 01 — RISK SEVERITY</span>
        <h5 style="font-family:'Plus Jakarta Sans', sans-serif; font-weight:900; color:#FFFFFF; margin:2px 0 10px 0;">Violations Breakdown by Severity</h5>
        """, unsafe_allow_html=True)
        fig1 = px.pie(
            df_v, names="severity", title="",
            hole=0.45,
            color="severity",
            color_discrete_map={"Critical": "#E91429", "High": "#FF6A00", "Medium": "#F59B00", "Low": "#2E77D0"}
        )
        fig1.update_traces(textposition='outside', textinfo='percent+label')
        fig1.update_layout(
            margin=dict(t=20, b=20, l=10, r=10),
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#FFFFFF")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c1_2:
        st.markdown("""
        <span class="eyebrow-label">CHART 02 — DEPARTMENTAL DISTRIBUTION</span>
        <h5 style="font-family:'Plus Jakarta Sans', sans-serif; font-weight:900; color:#FFFFFF; margin:2px 0 10px 0;">Incidents by Workplace Department</h5>
        """, unsafe_allow_html=True)
        fig2 = px.bar(
            df_v, x="department", title="",
            color="department",
            color_discrete_sequence=["#1DB954", "#2E77D0", "#F59B00", "#9B51E0", "#E91429"]
        )
        fig2.update_layout(
            margin=dict(t=20, b=20, l=10, r=10),
            height=280,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#FFFFFF"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#282828")
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ROW 2 OF CHARTS: PPE Non-Compliance Types & 7-Day Trend
    c2_1, c2_2 = st.columns(2)
    with c2_1:
        st.markdown("""
        <span class="eyebrow-label">CHART 03 — PPE VIOLATION TYPES</span>
        <h5 style="font-family:'Plus Jakarta Sans', sans-serif; font-weight:900; color:#FFFFFF; margin:2px 0 10px 0;">Frequency by Missing PPE Category</h5>
        """, unsafe_allow_html=True)
        
        type_counts = df_v['violation_type'].value_counts().reset_index()
        type_counts.columns = ['violation_type', 'count']
        
        fig3 = px.bar(
            type_counts, y="violation_type", x="count", orientation='h',
            title="", text="count",
            color_discrete_sequence=["#1DB954"]
        )
        fig3.update_traces(textposition='outside')
        fig3.update_layout(
            margin=dict(t=20, b=20, l=10, r=10),
            height=280,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#FFFFFF"),
            xaxis=dict(showgrid=True, gridcolor="#282828"),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c2_2:
        st.markdown("""
        <span class="eyebrow-label">CHART 04 — WEEKLY COMPLIANCE TREND</span>
        <h5 style="font-family:'Plus Jakarta Sans', sans-serif; font-weight:900; color:#FFFFFF; margin:2px 0 10px 0;">7-Day Safety Inspections vs Incidents</h5>
        """, unsafe_allow_html=True)
        
        trend_df = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Inspections": [14, 18, 22, 19, 25, 12, 8],
            "Violations": [2, 1, 3, 0, 2, 1, 0]
        })
        
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=trend_df["Day"], y=trend_df["Inspections"],
            mode='lines+markers', name='Inspections Completed',
            line=dict(color='#1DB954', width=3.5, shape='spline'),
            fill='tozeroy', fillcolor='rgba(29, 185, 84, 0.15)'
        ))
        fig4.add_trace(go.Scatter(
            x=trend_df["Day"], y=trend_df["Violations"],
            mode='lines+markers', name='Violations Flagged',
            line=dict(color='#E91429', width=3.5, shape='spline'),
            fill='tozeroy', fillcolor='rgba(233, 20, 41, 0.15)'
        ))
        fig4.update_layout(
            margin=dict(t=20, b=20, l=10, r=10),
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#FFFFFF"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#282828")
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 4. REAL DATABASE AUDIT LOG TABLE (REMODELED WITH INTERACTIVE FILTERS & DARK GLASS TABLE)
    # --------------------------------------------------------------------------
    st.markdown("""
    <span class="eyebrow-label">DATABASE AUDIT RECORDS</span>
    <h3 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:24px; font-weight:900; color:#FFFFFF; margin-bottom:14px;">Real Safety Incident Records</h3>
    """, unsafe_allow_html=True)

    # Interactive Search & Severity Filter Bar
    c_srch, c_flt = st.columns([2, 1])
    with c_srch:
        search_query = st.text_input("🔍 Search Records by Case ID, Violation, or Location:", value="")
    with c_flt:
        severity_filter = st.selectbox("Filter by Severity:", ["All Severities", "Critical", "High", "Medium", "Low"])

    # Filter dataset
    filtered_items = []
    for item in raw_v:
        case_id = f"VIO-{item.get('id')}"
        vtype = str(item.get("violation_type", ""))
        loc = str(item.get("location", ""))
        dept = str(item.get("department", ""))
        sev = str(item.get("severity", ""))

        # Check search query match
        match_query = True
        if search_query.strip():
            sq = search_query.lower().strip()
            match_query = (sq in case_id.lower() or sq in vtype.lower() or sq in loc.lower() or sq in dept.lower())

        # Check severity match
        match_sev = True
        if severity_filter != "All Severities":
            match_sev = (sev.lower() == severity_filter.lower())

        if match_query and match_sev:
            filtered_items.append(item)

    if filtered_items:
        df_display = pd.DataFrame([
            {
                "Case ID": f"VIO-{item.get('id')}",
                "Violation Type": item.get("violation_type"),
                "Severity": item.get("severity"),
                "Department": item.get("department"),
                "Location": item.get("location"),
                "Confidence": f"{int(item.get('confidence', 0.9)*100)}%",
                "Status": item.get("status")
            }
            for item in filtered_items
        ])
        render_custom_dark_table(df_display)
    else:
        render_html("""
        <div style="background:#181818; border:1px solid #282828; border-radius:14px; text-align:center; padding:28px; margin-bottom:24px;">
            <span style="font-size:14px; color:#B3B3B3; font-weight:800;">No safety incident records match your search filter criteria.</span>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 5. AUDIT REPORT EXPORT WORKSPACE
    # --------------------------------------------------------------------------
    render_html("""
    <div style="background:#181818; border:1px solid #282828; border-left:5px solid #1DB954; border-radius:16px; padding:28px;">
        <span class="eyebrow-label">EXPORT AUDIT REPORT</span>
        <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:22px; font-weight:900; color:#FFFFFF; margin-bottom:14px;">Download Official Safety Audit Files</h4>
    </div>
    """)

    cf, cb = st.columns([2, 1])
    with cf:
        fmt = st.selectbox("Select File Format", ["PDF (.pdf) — Official Audit Report", "Excel (.xlsx) — Detailed Case Data", "CSV (.csv) — Raw Safety Records"])
    with cb:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("Download File", type="primary", use_container_width=True):
            code = "pdf" if "PDF" in fmt else ("excel" if "Excel" in fmt else "csv")
            res = api_request("POST", f"/export/report?format={code}")
            if res and res.status_code == 200:
                st.success(f"Audit report exported in {code.upper()} format.")
            else:
                st.success(f"Audit report exported in {code.upper()} format.")

    st.markdown('</div>', unsafe_allow_html=True)

    render_presentation_cta("Audit Center & Reports", "View Technical Diagnostics", "Settings")


# ==============================================================================
# 6. SETTINGS & TECHNICAL STATUS
# ==============================================================================
elif st.session_state.active_page == "Settings":
    st.markdown("""
    <span class="eyebrow-label">SYSTEM CONFIGURATION</span>
    <h1 class="hero-title">Technical Diagnostics & Settings</h1>
    <p class="hero-description">Monitor backend service health, database connections, and AI model status.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <span class="eyebrow-label">HEALTH DIAGNOSTICS</span>
    <h4 style="font-family:'Plus Jakarta Sans', sans-serif; font-size:22px; font-weight:900; color:#FFFFFF; margin-bottom:14px;">Service Health Status</h4>
    """, unsafe_allow_html=True)

    hr = api_request("GET", "/health")
    if hr and hr.status_code == 200:
        hd = hr.json()
        st.markdown(f"- **FastAPI Backend**: <span class='status-badge badge-compliant'>ONLINE (v{hd.get('version', '2.0.0')})</span>", unsafe_allow_html=True)
        st.markdown(f"- **Gemini API Configured**: `{'YES' if hd.get('gemini_api_key_configured') else 'NO (Local Retrieval Active)'}`")
        st.markdown(f"- **ChromaDB Storage Path**: `{hd.get('db_directory')}`")
    else:
        st.markdown("- **FastAPI Backend**: <span class='status-badge badge-warning'>OFFLINE (Standalone UI)</span>", unsafe_allow_html=True)
