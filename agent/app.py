import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Daily Reflection",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Styling ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background-color: #0f0f14;
    color: #e8e4dc;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 680px; }

/* Progress bar container */
.progress-wrap {
    display: flex;
    gap: 6px;
    margin-bottom: 2.5rem;
}
.progress-dot {
    height: 3px;
    flex: 1;
    border-radius: 2px;
    background: #2a2a35;
    transition: background 0.4s ease;
}
.progress-dot.done { background: #c8a96e; }
.progress-dot.active { background: #e8d5a3; }

/* Axis label */
.axis-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 0.5rem;
}

/* Node type badge */
.node-badge {
    display: inline-block;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a5a6e;
    margin-bottom: 1.2rem;
    font-weight: 500;
}

/* Main question text */
.question-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    line-height: 1.45;
    color: #f0ebe0;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* Reflection / bridge text */
.reflection-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    line-height: 1.6;
    color: #d4c9b0;
    font-style: italic;
    border-left: 2px solid #c8a96e;
    padding-left: 1.2rem;
    margin-bottom: 2rem;
}

/* Option buttons */
div[data-testid="stButton"] > button {
    background: #1a1a24 !important;
    color: #c8c4bc !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 10px !important;
    padding: 0.85rem 1.2rem !important;
    width: 100% !important;
    text-align: left !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 400 !important;
    line-height: 1.5 !important;
    margin-bottom: 0.5rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    background: #22222e !important;
    border-color: #c8a96e !important;
    color: #f0ebe0 !important;
    transform: translateX(4px) !important;
}

/* Continue button */
.continue-btn > button {
    background: #c8a96e !important;
    color: #0f0f14 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    margin-top: 1rem !important;
}
.continue-btn > button:hover {
    background: #d4b87a !important;
    transform: none !important;
}

/* Summary card */
.summary-card {
    background: #1a1a24;
    border: 1px solid #2a2a38;
    border-radius: 14px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.summary-axis {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #2a2a38;
}
.summary-axis:last-child { border-bottom: none; }
.summary-axis-name {
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5a5a6e;
}
.summary-axis-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: #c8a96e;
}

/* End message */
.end-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: #7a7a8a;
    text-align: center;
    margin-top: 2rem;
    font-style: italic;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1e1e2a;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────
def init_session():
    if "session" not in st.session_state:
        try:
            res = requests.get(f"{API_URL}/start")
            data = res.json()
            st.session_state.session = data["session"]
            st.session_state.node = data["node"]
            st.session_state.started = True
            st.session_state.finished = False
            st.session_state.waiting_continue = False
        except Exception as e:
            st.error(f"Cannot connect to backend. Make sure FastAPI is running.\n\n`uvicorn agent.main:app --reload`\n\nError: {e}")
            st.stop()


def advance(selected_option=None):
    try:
        res = requests.post(f"{API_URL}/advance", json={
            "session": st.session_state.session,
            "selected_option": selected_option,
        })
        data = res.json()
        st.session_state.session = data["session"]
        st.session_state.node = data["node"]

        node_type = data["node"]["type"]
        if node_type in ("reflection", "summary", "end"):
            st.session_state.waiting_continue = True
        else:
            st.session_state.waiting_continue = False

        if node_type == "end":
            st.session_state.finished = True

    except Exception as e:
        st.error(f"Error advancing session: {e}")


# ── Progress indicator ─────────────────────────────────────
def render_progress():
    node = st.session_state.node
    node_id = node["id"]

    # Define rough stage based on node prefix
    axis1_ids = {"START", "A1_OPEN", "A1_D1", "A1_Q_AGENCY_HIGH", "A1_Q_AGENCY_LOW",
                 "A1_Q2_HIGH", "A1_Q2_LOW", "A1_REFL_INT", "A1_REFL_EXT"}
    axis2_ids = {"BRIDGE_1_2", "A2_OPEN", "A2_D1", "A2_Q_CONTRIB_HIGH", "A2_Q_ENTITLE_HIGH",
                 "A2_Q2_CONTRIB", "A2_Q2_ENTITLE", "A2_REFL_CONTRIB", "A2_REFL_ENTITLE"}
    axis3_ids = {"BRIDGE_2_3", "A3_OPEN", "A3_D1", "A3_Q_SELF_HIGH", "A3_Q_ALTRO_HIGH",
                 "A3_Q2_SELF", "A3_Q2_ALTRO", "A3_REFL_SELF", "A3_REFL_ALTRO"}

    if node_id in axis1_ids:
        stage = 1
    elif node_id in axis2_ids:
        stage = 2
    elif node_id in axis3_ids:
        stage = 3
    else:
        stage = 4  # summary/end

    dots_html = '<div class="progress-wrap">'
    for i in range(1, 5):
        if i < stage:
            cls = "done"
        elif i == stage:
            cls = "active"
        else:
            cls = ""
        dots_html += f'<div class="progress-dot {cls}"></div>'
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

    labels = {1: "Axis I · Locus", 2: "Axis II · Orientation",
              3: "Axis III · Radius", 4: "Reflection"}
    st.markdown(f'<div class="axis-label">{labels.get(stage, "")}</div>', unsafe_allow_html=True)


# ── Node renderers ─────────────────────────────────────────
def render_node(node):
    node_type = node["type"]

    if node_type == "start":
        st.markdown(f'<div class="question-text">{node["text"]}</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="continue-btn">', unsafe_allow_html=True)
            if st.button("Begin →"):
                advance()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif node_type == "question":
        st.markdown(f'<div class="node-badge">Question</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{node["text"]}</div>', unsafe_allow_html=True)
        for option in node["options"]:
            if st.button(option, key=f"opt_{option}"):
                advance(selected_option=option)
                st.rerun()

    elif node_type == "reflection":
        st.markdown(f'<div class="node-badge">Reflection</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="reflection-text">{node["text"]}</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="continue-btn">', unsafe_allow_html=True)
            if st.button("Continue →"):
                st.session_state.waiting_continue = False
                advance()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif node_type == "bridge":
        st.markdown(f'<div class="reflection-text">{node["text"]}</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="continue-btn">', unsafe_allow_html=True)
            if st.button("Continue →"):
                advance()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif node_type == "summary":
        st.markdown(f'<div class="node-badge">Your Reflection</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">Here\'s what today looked like.</div>',
                    unsafe_allow_html=True)

        dominants = node.get("dominants", {})
        labels = {
            "axis1": ("Locus", {"internal": "Victor", "external": "Victim", "balanced": "Balanced"}),
            "axis2": ("Orientation", {"contribution": "Contributor", "entitlement": "Entitled", "balanced": "Balanced"}),
            "axis3": ("Radius", {"altrocentric": "Altrocentric", "selfcentric": "Self-centric", "balanced": "Balanced"}),
        }

        card_html = '<div class="summary-card">'
        for axis_key, (axis_name, pole_labels) in labels.items():
            dominant = dominants.get(axis_key, "balanced")
            label = pole_labels.get(dominant, dominant.capitalize())
            card_html += f'''
            <div class="summary-axis">
                <span class="summary-axis-name">{axis_name}</span>
                <span class="summary-axis-value">{label}</span>
            </div>'''
        card_html += '</div>'
        st.markdown(card_html, unsafe_allow_html=True)

        st.markdown(f'<div class="reflection-text">{node["text"]}</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="continue-btn">', unsafe_allow_html=True)
            if st.button("Close →"):
                advance()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif node_type == "end":
        st.markdown(f'<div class="end-text">{node["text"]}</div>', unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="continue-btn">', unsafe_allow_html=True)
            if st.button("Start over"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────
def main():
    init_session()

    # Header
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:2.5rem;">
        <span style="font-size:1.3rem;">🌙</span>
        <span style="font-family:'DM Sans',sans-serif; font-size:0.8rem;
               letter-spacing:0.14em; text-transform:uppercase;
               color:#5a5a6e; font-weight:500;">Daily Reflection</span>
    </div>
    """, unsafe_allow_html=True)

    node = st.session_state.node

    # Show progress only during conversation (not on end screen)
    if node["type"] not in ("end",):
        render_progress()

    render_node(node)


if __name__ == "__main__":
    main()
