import streamlit as st
import pandas as pd
import plotly.express as px
import time

from utils import normalize_url, is_valid_url
from feature_engine import extract_features
from redirects import get_redirect_chain
from risk_model import calculate_risk
from llm_explainer import generate_threat_report

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Sentinel AI PRO", layout="wide")

# ==========================================================
# CYBER PROTECH UI CSS
# ==========================================================
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at 20% 20%, #071021, #020617 60%);
    color: #e2e8f0;
}

/* Hide default menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Header */
.cyber-header {
    font-size: 28px;
    font-weight: 700;
    color: #22d3ee;
}

/* Glass Cards */
.glass-card {
    background: rgba(17, 25, 40, 0.6);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(34,211,238,0.2);
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-6px);
    border: 1px solid #22d3ee;
    box-shadow: 0 0 25px rgba(34,211,238,0.5);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #0ea5e9, #22d3ee);
    border-radius: 30px;
    color: white;
    font-weight: 600;
    border: none;
    padding: 0.5rem 1.5rem;
    transition: 0.3s;
}

.stButton>button:hover {
    box-shadow: 0 0 20px #22d3ee;
    transform: scale(1.05);
}

/* Text Area */
textarea {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(15, 23, 42, 0.8);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(34,211,238,0.2);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION STATE
# ==========================================================
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# ==========================================================
# HEADER NAVIGATION
# ==========================================================
st.markdown('<div class="cyber-header">🛡 Sentinel AI PRO</div>', unsafe_allow_html=True)
st.markdown("Threat Intelligence Engine")
st.markdown("---")

col1, col2, col3 = st.columns(3)

if col1.button("Dashboard"):
    st.session_state.page = "dashboard"

if col2.button("Threat Scan"):
    st.session_state.page = "scan"

if col3.button("History"):
    st.session_state.page = "history"

st.markdown("---")

# ==========================================================
# DASHBOARD
# ==========================================================
if st.session_state.page == "dashboard":

    st.markdown("""
    <div style="font-size:34px;font-weight:850;margin-top:8px;margin-bottom:8px;">
    📊 Security Intelligence Dashboard
    </div>
    """, unsafe_allow_html=True)


    history = st.session_state.scan_history
    total = len(history)

    if total > 0:
        avg = sum(x["score"] for x in history) / total
        low = sum(1 for x in history if x["level"] == "Low")
        med = sum(1 for x in history if x["level"] == "Medium")
        high = sum(1 for x in history if x["level"] == "High")
    else:
        avg = 0
        low = med = high = 0

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Total Scans", total)
    colB.metric("Avg Risk Score", f"{int(avg)}%")
    colC.metric("Safe Detections", low)
    colD.metric("High Risk Count", high)

    st.markdown("---")

    if total > 0:
        df = pd.DataFrame(history)
        df["scan_index"] = range(1, len(df)+1)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(df, x="scan_index", y="score",
                          markers=True, template="plotly_dark")
            st.plotly_chart(fig, width="stretch")

        with col2:
            dist = pd.DataFrame({
                "Level": ["Low","Medium","High"],
                "Count": [low, med, high]
            })
            fig2 = px.pie(dist, names="Level",
                          values="Count",
                          hole=0.5,
                          template="plotly_dark")
            st.plotly_chart(fig2, width="stretch")

# ==========================================================
# SCAN PAGE
# ==========================================================
elif st.session_state.page == "scan":

    st.markdown("## 🔎 Advanced Threat Scanner")

    url_input = st.text_area(
        "URL Input",
        placeholder="Paste suspicious URL here...",
        height=150,
        label_visibility="collapsed"
    )

    ai_mode = st.checkbox("Generate AI Threat Report (Accurate Mode)", value=False)

    if st.button("Run Scan"):

        if not url_input.strip():
            st.warning("Please enter URL.")
            st.stop()

        url = normalize_url(url_input.strip())

        if not is_valid_url(url):
            st.error("Invalid URL format.")
            st.stop()

        start = time.time()

        chain = get_redirect_chain(url)
        final_url = chain[-1]

        features = extract_features(final_url)

        score, level, category, confidence, reasons = calculate_risk(
            features, chain, url
        )

        st.success("Scan Complete")

        st.metric("Risk Score", f"{score}/100")
        st.write("Risk Level:", level)
        st.write("Category:", category)
        st.write("Confidence:", f"{int(confidence*100)}%")

        st.markdown("### 🔁 Redirect Chain")
        st.json(chain)

        st.markdown("### 🚨 Indicators")
        for r in reasons:
            st.write(f"- {r}")

        if ai_mode:
            with st.spinner("Generating AI Analysis..."):
                report = generate_threat_report(
                    url=url,
                    final_url=final_url,
                    score=score,
                    level=level,
                    reasons=reasons,
                    features=features
                )
            st.markdown("### 🧠 AI Threat Report")
            st.write(report)

        st.session_state.scan_history.append({
            "url": url,
            "score": score,
            "level": level,
            "category": category,
            "confidence": confidence
        })

        st.caption(f"Scan completed in {round(time.time()-start,2)} seconds")

# ==========================================================
# HISTORY
# ==========================================================
elif st.session_state.page == "history":

    st.markdown("## 🗂 Scan Archive")

    history = st.session_state.scan_history

    if len(history) == 0:
        st.info("No previous scans yet.")
    else:
        for h in reversed(history):
            st.markdown("---")
            st.write("URL:", h["url"])
            st.write("Score:", h["score"])
            st.write("Level:", h["level"])
            st.write("Category:", h["category"])
            st.write("Confidence:", f"{int(h['confidence']*100)}%")

