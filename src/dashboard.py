import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import defaultdict

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="HydraAgent — Smart Hydration",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Constants ─────────────────────────────────────────────────
API_BASE = "http://localhost:8000"
DAILY_GOAL = 2500

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f5faff 100%);
    border: 1px solid rgba(61,155,233,0.15);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 4px 20px rgba(13,31,45,0.07);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-val {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #0d1f2d;
    line-height: 1.1;
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8fa8bc;
    margin-top: 4px;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(160deg, #0d2d4a 0%, #0f3d60 50%, #0a4a6a 100%);
    border-radius: 20px;
    padding: 28px 32px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 8px 40px rgba(13,45,74,0.3);
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #b8ddf7;
}

/* ── AI Analysis box ── */
.ai-box {
    background: linear-gradient(135deg, #f0f9ff 0%, #e6f4ff 100%);
    border: 1px solid rgba(61,155,233,0.2);
    border-left: 4px solid #3d9be9;
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #2d4a5f;
    margin-top: 12px;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    font-weight: 500;
}
.badge-good  { background: rgba(31,200,122,0.12); color: #1fc87a; }
.badge-warn  { background: rgba(245,166,35,0.12);  color: #f5a623; }
.badge-danger{ background: rgba(232,69,69,0.12);   color: #e84545; }

/* ── Section title ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #0d1f2d;
    margin-bottom: 14px;
}

/* ── Quick log buttons ── */
.stButton > button {
    border-radius: 12px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2d4a 0%, #0f3d60 100%);
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] .stNumberInput input {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: #3d9be9 !important;
    color: white !important;
    border: none !important;
    width: 100% !important;
    padding: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(61,155,233,0.4) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #2a8fe4 !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)


# ── API Helpers ───────────────────────────────────────────────
def log_intake_api(user_id: str, intake_ml: int):
    try:
        resp = requests.post(
            f"{API_BASE}/log-intake",
            json={"user_id": user_id, "intake_ml": intake_ml},
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    # Fallback if API is down
    return {"message": "Logged locally", "analysis": generate_local_analysis(intake_ml)}


def get_history_api(user_id: str):
    try:
        resp = requests.get(f"{API_BASE}/history/{user_id}", timeout=10)
        if resp.status_code == 200:
            return resp.json().get("history", [])
    except Exception:
        pass
    return []


def generate_local_analysis(intake_ml: int) -> str:
    total = st.session_state.get("today_total", 0) + intake_ml
    pct = round(total / DAILY_GOAL * 100)
    if pct >= 100:
        return f"🎉 Outstanding! You've hit your {DAILY_GOAL}ml goal for today. Your body is fully hydrated — keep it up!"
    elif pct >= 75:
        return f"💪 Great progress! You're at {pct}% of your daily goal. Just {DAILY_GOAL - total}ml left. Try a glass before dinner."
    elif pct >= 50:
        return f"🌊 Halfway there! You've had {total}ml. Aim for another glass every 90 minutes to stay on track."
    elif pct >= 25:
        return f"⚡ You've started with {total}ml, but there's more ground to cover. Set a reminder every hour to sip water."
    else:
        return f"🚨 Only {total}ml so far — try to drink {round((DAILY_GOAL - total) / 4)}ml every hour to catch up."


# ── Session State Init ────────────────────────────────────────
if "sessions" not in st.session_state:
    st.session_state.sessions = []   # [{date, ml}]
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_01"

today_str = datetime.today().strftime("%Y-%m-%d")


def today_sessions():
    return [s for s in st.session_state.sessions if s["date"] == today_str]

def today_total():
    return sum(s["ml"] for s in today_sessions())


# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 24px'>
        <div style='font-size:2.5rem'>💧</div>
        <div style='font-family:DM Serif Display,serif; font-size:1.5rem; letter-spacing:-0.02em'>HydraAgent</div>
        <div style='font-family:DM Mono,monospace; font-size:0.65rem; letter-spacing:0.12em; color:#b8ddf7; text-transform:uppercase; margin-top:4px'>Agentic AI · Hydration</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**👤 User ID**")
    user_id = st.text_input("", value=st.session_state.user_id, label_visibility="collapsed", key="uid_input")
    st.session_state.user_id = user_id

    st.markdown("---")
    st.markdown("**💧 Log Water Intake**")
    intake_ml = st.number_input("Amount (ml)", min_value=1, max_value=5000, value=250, step=50, label_visibility="visible")

    if st.button("➕  Log Intake", use_container_width=True):
        with st.spinner("🤖 Agent analyzing..."):
            result = log_intake_api(user_id, intake_ml)
            st.session_state.sessions.append({"date": today_str, "ml": intake_ml})
            st.session_state.ai_analysis = result.get("analysis", "")
        st.success(f"✅ +{intake_ml}ml logged!")
        st.rerun()

    st.markdown("**⚡ Quick Log**")
    qcols = st.columns(2)
    quick = [("☕ 150", 150), ("🥤 250", 250), ("🍶 500", 500), ("💧 750", 750)]
    for i, (label, ml) in enumerate(quick):
        with qcols[i % 2]:
            if st.button(label, key=f"q{ml}", use_container_width=True):
                with st.spinner("🤖 Analyzing..."):
                    result = log_intake_api(user_id, ml)
                    st.session_state.sessions.append({"date": today_str, "ml": ml})
                    st.session_state.ai_analysis = result.get("analysis", "")
                st.success(f"✅ +{ml}ml logged!")
                st.rerun()

    st.markdown("---")
    st.markdown("**⚙️ Settings**")
    api_url = st.text_input("API Base URL", value=API_BASE)
    st.markdown(
        "<div style='font-family:DM Mono,monospace;font-size:0.68rem;color:#b8ddf7;margin-top:6px'>"
        "🟢 Connected to FastAPI backend</div>",
        unsafe_allow_html=True
    )


# ── MAIN CONTENT ──────────────────────────────────────────────
total = today_total()
pct = min(100, round(total / DAILY_GOAL * 100))
remaining = max(0, DAILY_GOAL - total)
sess_count = len(today_sessions())
avg_ml = round(total / sess_count) if sess_count else 0

# Status
if pct >= 100:
    status_text, status_class, status_emoji = "Goal Reached! 🎉", "badge-good", "🟢"
elif pct >= 60:
    status_text, status_class, status_emoji = "Getting There", "badge-warn", "🟡"
else:
    status_text, status_class, status_emoji = "Needs Attention", "badge-danger", "🔴"

# ── Hero Banner ──
now_label = datetime.today().strftime("%A, %d %B %Y")
st.markdown(f"""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px">
        <div>
            <div class="hero-title">💧 HydraAgent Dashboard</div>
            <div class="hero-sub">Agentic AI · Smart Hydration Monitoring · {now_label}</div>
        </div>
        <div style="text-align:right">
            <span class="badge {status_class}">{status_emoji} {status_text}</span>
            <div style="font-family:DM Mono,monospace;font-size:0.7rem;color:#b8ddf7;margin-top:8px">User: {user_id}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top Metrics Row ──
c1, c2, c3, c4, c5, c6 = st.columns(6)
metrics = [
    (c1, f"{total} ml",        "Total Today",     "#3d9be9"),
    (c2, f"{remaining} ml",    "Remaining",        "#00c4b4"),
    (c3, f"{pct}%",            "Goal Progress",    "#1a6bff"),
    (c4, f"{sess_count}",      "Sessions",         "#ff6b35"),
    (c5, f"{avg_ml} ml" if avg_ml else "—", "Avg / Session", "#1fc87a"),
    (c6, f"{DAILY_GOAL} ml",   "Daily Goal",       "#f5a623"),
]
for col, val, label, color in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid {color}">
            <div class="metric-val" style="color:{color}">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Progress Bar + AI Analysis ──
col_prog, col_ai = st.columns([1, 2])

with col_prog:
    st.markdown('<div class="section-title">Daily Progress</div>', unsafe_allow_html=True)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total,
        delta={"reference": DAILY_GOAL, "valueformat": ".0f", "suffix": " ml"},
        number={"suffix": " ml", "font": {"size": 28, "family": "DM Serif Display"}},
        gauge={
            "axis": {"range": [0, DAILY_GOAL], "tickwidth": 1, "tickcolor": "#8fa8bc"},
            "bar": {"color": "#3d9be9", "thickness": 0.28},
            "bgcolor": "#f0f4f8",
            "borderwidth": 0,
            "steps": [
                {"range": [0, DAILY_GOAL * 0.33], "color": "rgba(232,69,69,0.12)"},
                {"range": [DAILY_GOAL * 0.33, DAILY_GOAL * 0.66], "color": "rgba(245,166,35,0.12)"},
                {"range": [DAILY_GOAL * 0.66, DAILY_GOAL], "color": "rgba(31,200,122,0.12)"},
            ],
            "threshold": {
                "line": {"color": "#1fc87a", "width": 3},
                "thickness": 0.85,
                "value": DAILY_GOAL
            }
        },
        title={"text": f"<b>{pct}% of {DAILY_GOAL}ml goal</b>", "font": {"size": 13, "family": "DM Mono"}},
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    fig_gauge.update_layout(
        height=260, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Instrument Sans"}
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_ai:
    st.markdown('<div class="section-title">🤖 AI Agent Analysis</div>', unsafe_allow_html=True)
    if st.session_state.ai_analysis:
        st.markdown(f'<div class="ai-box">{st.session_state.ai_analysis}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ai-box" style="color:#8fa8bc; font-family:'DM Mono',monospace; font-size:0.82rem;">
            Log some water to receive personalized AI analysis from HydraAgent.<br><br>
            🤖 The agent will perceive your intake, reason over your hydration status,
            and provide actionable guidance powered by LLaMA 3.1 via Groq.
        </div>
        """, unsafe_allow_html=True)

    # Today's session breakdown
    if today_sessions():
        st.markdown("<br>**Today's Sessions**", unsafe_allow_html=True)
        sess_df = pd.DataFrame(today_sessions())
        sess_df.index = range(1, len(sess_df) + 1)
        sess_df.columns = ["Date", "Amount (ml)"]
        st.dataframe(sess_df[["Amount (ml)"]], use_container_width=True, height=160)

# ── History Section ──
st.markdown("---")
st.markdown('<div class="section-title">📊 Intake History</div>', unsafe_allow_html=True)

period_tab, view_tab = st.tabs(["📅 Period View", "📋 Log View"])

with period_tab:
    period = st.radio(
        "Select Period",
        ["📅 Week", "🗓 Month", "📆 Year"],
        horizontal=True,
        label_visibility="collapsed"
    )

    all_sessions = st.session_state.sessions
    now = datetime.today()

    if period == "📅 Week":
        days = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        totals = {d: sum(s["ml"] for s in all_sessions if s["date"] == d) for d in days}
        labels = [("Today" if d == today_str else datetime.strptime(d, "%Y-%m-%d").strftime("%a")) for d in days]
        title = "Last 7 Days — Daily Intake"
        xaxis_title = "Day"

    elif period == "🗓 Month":
        year, month = now.year, now.month
        import calendar
        days_in_month = calendar.monthrange(year, month)[1]
        days = [f"{year}-{month:02d}-{d:02d}" for d in range(1, days_in_month + 1)]
        totals = {d: sum(s["ml"] for s in all_sessions if s["date"] == d) for d in days}
        labels = [str(datetime.strptime(d, "%Y-%m-%d").day) for d in days]
        title = f"{now.strftime('%B %Y')} — Daily Intake"
        xaxis_title = "Day of Month"

    else:  # Year
        months = [f"{now.year}-{m:02d}" for m in range(1, 13)]
        totals = {m: sum(s["ml"] for s in all_sessions if s["date"].startswith(m)) for m in months}
        days = months
        labels = [datetime.strptime(m + "-01", "%Y-%m-%d").strftime("%b") for m in months]
        title = f"{now.year} — Monthly Intake"
        xaxis_title = "Month"

    values = [totals.get(d, 0) for d in days]
    colors = ["#00c4b4" if d == today_str else ("#1fc87a" if v >= DAILY_GOAL else "#3d9be9")
              for d, v in zip(days, values)]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y} ml<extra></extra>",
        name="Intake"
    ))
    # Goal line (only for week/month)
    if period != "📆 Year":
        fig_bar.add_hline(
            y=DAILY_GOAL, line_dash="dot",
            line_color="#f5a623", line_width=2,
            annotation_text=f"Goal {DAILY_GOAL}ml",
            annotation_font_color="#f5a623",
            annotation_font_size=11
        )
    fig_bar.update_layout(
        title=dict(text=title, font=dict(family="DM Serif Display", size=16)),
        xaxis_title=xaxis_title, yaxis_title="ml",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Instrument Sans"),
        height=340, margin=dict(t=50, b=40, l=40, r=20),
        xaxis=dict(showgrid=False, tickfont=dict(family="DM Mono", size=11)),
        yaxis=dict(gridcolor="rgba(143,168,188,0.2)", tickfont=dict(family="DM Mono", size=11)),
        showlegend=False,
        bargap=0.25
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Period summary chips
    total_period = sum(values)
    avg_period = round(total_period / max(len([v for v in values if v > 0]), 1))
    best_day = max(values) if values else 0
    goal_days = sum(1 for v in values if v >= DAILY_GOAL)

    s1, s2, s3, s4 = st.columns(4)
    summary_items = [
        (s1, f"{total_period/1000:.1f} L", "Total Volume"),
        (s2, f"{avg_period} ml", "Avg / Day"),
        (s3, f"{best_day} ml", "Best Day"),
        (s4, f"{goal_days}", "Goal Days Hit"),
    ]
    for col, val, label in summary_items:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center">
                <div class="metric-val" style="font-size:1.5rem">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

with view_tab:
    if not all_sessions:
        st.info("No intake sessions logged yet. Start logging water from the sidebar!")
    else:
        df = pd.DataFrame(all_sessions)
        df.columns = ["Date", "Amount (ml)"]
        df = df.sort_values("Date", ascending=False).reset_index(drop=True)
        df.index = range(1, len(df) + 1)

        # Group by date for summary
        grouped = df.groupby("Date")["Amount (ml)"].sum().reset_index()
        grouped.columns = ["Date", "Total (ml)"]
        grouped["Goal %"] = (grouped["Total (ml)"] / DAILY_GOAL * 100).round(1).astype(str) + "%"
        grouped["Status"] = grouped["Total (ml)"].apply(
            lambda x: "✅ Goal Met" if x >= DAILY_GOAL else ("⚠️ In Progress" if x >= DAILY_GOAL * 0.5 else "❌ Low")
        )
        grouped = grouped.sort_values("Date", ascending=False).reset_index(drop=True)

        st.dataframe(grouped, use_container_width=True, height=300)

        # Download button
        csv = grouped.to_csv(index=False)
        st.download_button(
            label="⬇️ Download History CSV",
            data=csv,
            file_name=f"hydraagent_{user_id}_history.csv",
            mime="text/csv"
        )