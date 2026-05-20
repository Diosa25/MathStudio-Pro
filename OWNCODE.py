import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Numerical Project",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
for key, val in {
    "rf_results":    [],
    "rf_root":       None,
    "rf_iterations": 0,
    "rf_error":      0,
    "rf_fig":        None,
    "rf_eq":         "",
    "rf_method":     "",
    "mx_result":     None,
    "mx_op":         "",
    "history":       [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS — VINTAGE BROWN ACADEMIC DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&display=swap');

/* ─── TOKENS ─────────────────────────────────────────────────────────────── */
:root {
    --bg:         #F0E6D0;
    --bg2:        #E8D9BF;
    --cream:      #FBF4E6;
    --cream2:     #F6EDD8;
    --border:     #C8A97A;
    --border2:    #B8936A;
    --brown-dk:   #2C1A0E;
    --brown-md:   #5C3317;
    --brown-lt:   #8B5E3C;
    --tan:        #C4A882;
    --tan-lt:     #DFC9A8;
    --gold:       #D4A96A;
    --gold-lt:    #E8C98A;
    --shadow:     rgba(44,26,14,0.18);
    --shadow-dk:  rgba(44,26,14,0.35);
}

/* ─── GLOBAL ─────────────────────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
    font-family: 'Crimson Text', Georgia, serif;
    background-color: var(--bg);
    color: var(--brown-dk);
}
.main .block-container {
    padding: 0.6rem 1.8rem 2rem 1.8rem;
    max-width: 100%;
}
#MainMenu, footer { visibility: hidden; }
::-webkit-scrollbar            { width: 6px; height: 6px; }
::-webkit-scrollbar-track      { background: var(--bg2); }
::-webkit-scrollbar-thumb      { background: var(--brown-lt); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover{ background: var(--brown-md); }

/* ─── HEADER ──────────────────────────────────────────────────────────────── */
.vhdr {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem 0.9rem 2rem;
    background: linear-gradient(120deg, #1E0F06 0%, #3B2210 30%, #5C3317 60%, #3B2210 85%, #1E0F06 100%);
    border-radius: 14px;
    margin-bottom: 0.2rem;
    box-shadow: 0 6px 28px var(--shadow-dk), inset 0 1px 0 rgba(212,169,106,0.25);
    border: 1px solid #6A3E20;
    position: relative;
    overflow: hidden;
}
.vhdr::after {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(60deg, transparent, transparent 18px,
        rgba(212,169,106,0.04) 18px, rgba(212,169,106,0.04) 36px);
    pointer-events: none;
}
.vhdr-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.88rem;
    color: var(--gold);
    letter-spacing: 0.07em;
    line-height: 1.55;
    font-style: italic;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
    min-width: 185px;
}
.vhdr-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.95rem;
    font-weight: 700;
    color: #F5E6C8;
    letter-spacing: 0.25em;
    text-align: center;
    text-shadow: 0 2px 8px rgba(0,0,0,0.55);
    flex: 1;
}
.vhdr-right {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.8rem;
    color: #B8936A;
    text-align: right;
    letter-spacing: 0.05em;
    line-height: 1.6;
    min-width: 185px;
}
.ornament {
    text-align: center;
    color: #9B7245;
    letter-spacing: 0.55em;
    margin: 0.35rem 0 0.55rem 0;
    font-size: 0.95rem;
    user-select: none;
}

/* ─── NAV STRIP ───────────────────────────────────────────────────────────── */
.nav-strip {
    background: linear-gradient(135deg, #EDE0C4 0%, #E2D0AA 50%, #EDE0C4 100%);
    border: 1.5px solid var(--border);
    border-radius: 11px;
    padding: 0.6rem 1.3rem 0.45rem 1.3rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 2px 12px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.45);
}

/* ─── SECTION TITLE ───────────────────────────────────────────────────────── */
.stitle {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--brown-dk);
    border-bottom: 2px solid var(--brown-lt);
    padding-bottom: 0.28rem;
    margin-bottom: 0.75rem;
    letter-spacing: 0.04em;
}
.ssub {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    color: #6B4226;
    font-style: italic;
    margin-bottom: 0.85rem;
}

/* ─── PANEL CARDS ─────────────────────────────────────────────────────────── */
.panel {
    background: linear-gradient(160deg, var(--cream) 0%, var(--cream2) 100%);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    box-shadow: 3px 4px 18px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.55);
    margin-bottom: 0.75rem;
}
.panel-dark {
    background: linear-gradient(160deg, #EDE0C4 0%, #E5D4AE 100%);
    border: 1.5px solid var(--border2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 3px 4px 18px var(--shadow);
    margin-bottom: 0.75rem;
}
.panel-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--brown-md);
    letter-spacing: 0.04em;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ─── WIDGET OVERRIDES ────────────────────────────────────────────────────── */
div[data-testid="stRadio"] label > div p {
    font-family: 'Playfair Display', serif !important;
    font-size: 0.97rem !important;
    color: var(--brown-dk) !important;
    font-weight: 600 !important;
}
.stSelectbox > label,
.stNumberInput > label,
.stTextInput > label {
    font-family: 'Crimson Text', serif !important;
    color: #4A2A12 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input {
    border: 1.5px solid var(--border) !important;
    border-radius: 7px !important;
    background-color: var(--cream) !important;
    color: var(--brown-dk) !important;
    font-family: 'Crimson Text', serif !important;
    font-size: 0.97rem !important;
    box-shadow: inset 0 1px 5px rgba(59,31,12,0.07) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within,
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--brown-lt) !important;
    box-shadow: 0 0 0 2.5px rgba(139,94,60,0.2) !important;
}

/* ─── BUTTON ──────────────────────────────────────────────────────────────── */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--brown-md) 0%, var(--brown-lt) 55%, #7A4F2E 100%);
    color: #F5E6C8;
    font-family: 'Playfair Display', serif;
    font-size: 0.97rem;
    font-weight: 700;
    border: 1px solid #9B7245;
    letter-spacing: 0.09em;
    padding: 0.55rem 1rem;
    box-shadow: 0 3px 14px var(--shadow-dk), inset 0 1px 0 rgba(255,255,255,0.1);
    transition: all 0.25s ease;
    text-shadow: 0 1px 3px rgba(0,0,0,0.35);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1E0F06 0%, var(--brown-md) 100%);
    transform: translateY(-1.5px);
    box-shadow: 0 5px 20px var(--shadow-dk);
    color: var(--gold-lt);
}
.stButton > button:active { transform: translateY(0px); }

/* ─── METRICS ─────────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #EDE0C4, #E2CFA8) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.7rem 0.9rem !important;
    box-shadow: 2px 3px 11px var(--shadow) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Cormorant Garamond', serif !important;
    color: #6B4226 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: var(--brown-dk) !important;
    font-size: 1.45rem !important;
}

/* ─── DATAFRAME ───────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 9px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    font-family: 'Crimson Text', serif !important;
}
[data-testid="stDataFrame"] th {
    background-color: #5C3317 !important;
    color: #F5E6C8 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stDataFrame"] tr:hover {
    background-color: #EDE0C4 !important;
}

/* ─── INFO / SUCCESS ──────────────────────────────────────────────────────── */
[data-testid="stInfo"] {
    background-color: #EDE0C4 !important;
    border-left: 4px solid var(--brown-lt) !important;
    border-radius: 7px !important;
    font-family: 'Crimson Text', serif !important;
}
[data-testid="stSuccess"] {
    background-color: #E4D8C0 !important;
    border-left: 4px solid var(--brown-md) !important;
    border-radius: 7px !important;
    font-family: 'Crimson Text', serif !important;
}
[data-testid="stAlert"] {
    font-family: 'Crimson Text', serif !important;
    border-radius: 7px !important;
}

/* ─── HR ──────────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1.5px solid var(--border) !important;
    margin: 0.6rem 0 !important;
}

/* ─── SIDEBAR ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E0F06 0%, #2C1A0E 40%, #3B2210 100%) !important;
    border-right: 2px solid #5C3317 !important;
}
[data-testid="stSidebar"] * {
    color: #E8D5B0 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #3B2210, #5C3317) !important;
    border-color: #7A4F2E !important;
    color: #F5E6C8 !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #5C3317, #8B5E3C) !important;
}

/* ─── HISTORY CARD INSIDE SIDEBAR ─────────────────────────────────────────── */
.hist-card {
    background: rgba(92,51,23,0.35);
    border: 1px solid rgba(200,169,122,0.35);
    border-radius: 9px;
    padding: 0.7rem 0.85rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    transition: background 0.2s;
}
.hist-card:hover { background: rgba(92,51,23,0.55); }
.hist-method {
    font-family: 'Playfair Display', serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: #E8C98A;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
}
.hist-eq {
    font-family: 'Crimson Text', serif;
    font-size: 0.88rem;
    color: #D4BC96;
    font-style: italic;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 0.15rem;
}
.hist-ans {
    font-family: 'Playfair Display', serif;
    font-size: 0.9rem;
    color: #F5E6C8;
    font-weight: 600;
}
.hist-ts {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.75rem;
    color: #9B7A55;
    margin-top: 0.2rem;
    letter-spacing: 0.04em;
}
.hist-empty {
    text-align: center;
    padding: 1.5rem 0.5rem;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.95rem;
    font-style: italic;
    color: #7A5A3A;
}
.sidebar-hdr {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #E8C98A;
    letter-spacing: 0.1em;
    text-align: center;
    padding: 0.2rem 0 0.6rem 0;
    border-bottom: 1px solid rgba(200,169,122,0.35);
    margin-bottom: 0.7rem;
}
.sidebar-name {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 0.82rem;
    color: #B8936A;
    text-align: center;
    margin-bottom: 0.25rem;
    letter-spacing: 0.06em;
}

/* ─── PLACEHOLDER TEXT ───────────────────────────────────────────────────── */
.placeholder-box {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #9B7245;
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-style: italic;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — SAVE HISTORY PANEL
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div style="padding-top:0.4rem;">
            <div class="sidebar-hdr">✦ CALCULATION HISTORY ✦</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        clear_col, _ = st.columns([1, 0.01])
        with clear_col:
            if st.button("🗑  Clear History"):
                st.session_state.history = []
                st.rerun()

        st.markdown("<div style='margin-top:0.5rem;'>", unsafe_allow_html=True)
        # Render newest first
        for entry in reversed(st.session_state.history):
            st.markdown(f"""
                <div class="hist-card">
                    <div class="hist-method">{entry['type']} · {entry['method']}</div>
                    <div class="hist-eq">{entry['equation']}</div>
                    <div class="hist-ans">⟶ {entry['answer']}</div>
                    <div class="hist-ts">🕐 {entry['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="hist-empty">
                ✦ No calculations yet.<br>Results will appear here after solving.
            </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TOP HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div class="vhdr">
        <div class="vhdr-name">DIOSAMABEL B. PENASO<br>BSCOMPE-2</div>
        <div class="vhdr-title">✦ &nbsp; NUMERICAL PROJECT &nbsp; ✦</div>
        <div class="vhdr-right">Numerical Methods<br>Analysis</div>
    </div>
    <div class="ornament">— ✦ ◆ ✦ —</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TOP NAVIGATION STRIP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="nav-strip">', unsafe_allow_html=True)
app_mode = st.radio(
    "**Select Module**",
    ["Root Finding Analysis", "Advanced Matrix Operations"],
    horizontal=True,
    label_visibility="visible"
)
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 — ROOT FINDING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.markdown('<div class="stitle">⚙ Root Finding Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Select a numerical method, configure parameters, and instantly view the iteration table and graph.</div>', unsafe_allow_html=True)

    # ── THREE-COLUMN DASHBOARD LAYOUT ──
    col_left, col_right = st.columns([1, 2.35])

    # ────────────────── LEFT — INPUTS ──────────────────
    with col_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚙ Parameters</div>', unsafe_allow_html=True)

        eq_str   = st.text_input("Equation  f(x)", value="x**3 - x - 2",
                                 help="Use Python syntax: x**2, sin(x), exp(x), log(x)")
        method   = st.selectbox("Algorithm", [
            "Incremental Method",
            "Bisection Method",
            "Regula-Falsi Method",
            "Newton-Raphson Method",
            "Secant Method",
        ])

        if method in ["Bisection Method", "Regula-Falsi Method", "Incremental Method"]:
            xl = st.number_input("Lower Bound  (xl)", value=1.0, format="%.4f")
            xu = st.number_input("Upper Bound  (xu)", value=2.0, format="%.4f")
        elif method == "Newton-Raphson Method":
            x0 = st.number_input("Initial Guess  (x0)", value=1.0, format="%.4f")
        elif method == "Secant Method":
            x0 = st.number_input("First Guess   (x0)", value=1.0, format="%.4f")
            x1 = st.number_input("Second Guess  (x1)", value=2.0, format="%.4f")

        c_tol, c_iter = st.columns(2)
        tol      = c_tol.number_input("Tolerance",      value=0.0001, format="%.6f")
        max_iter = c_iter.number_input("Max Iterations", value=50, step=1)

        st.markdown("<div style='margin-top:0.6rem;'>", unsafe_allow_html=True)
        solve_btn = st.button("⟳  Calculate Root", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)   # /panel

    # ────────────────── RIGHT — TABLE + GRAPH ──────────────────
    with col_right:

        # ── COMPUTE ON BUTTON PRESS ──
        if solve_btn:
            try:
                xs   = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f    = sp.lambdify(xs, expr, 'numpy')
                dfdx = sp.lambdify(xs, sp.diff(expr, xs), 'numpy')

                results, root, iterations, final_err = [], None, 0, 0

                # ── INCREMENTAL METHOD ──
                # Columns: Iteration | x_l | Δx | x_u | f(x_l) | f(x_u) | f(x_l)·f(x_u) | Remark
                if method == "Incremental Method":
                    step   = tol if tol > 0 else 0.1
                    curr_x = xl
                    for i in range(int(max_iter)):
                        next_x = curr_x + step
                        fxl    = float(f(curr_x))
                        fxu    = float(f(next_x))
                        prod   = fxl * fxu
                        remark = "Sign change — root bracketed" if prod < 0 else ""
                        results.append({
                            "Iteration":        i + 1,
                            "x_l":              round(curr_x, 7),
                            "Δx":               round(step,   7),
                            "x_u":              round(next_x, 7),
                            "f(x_l)":           round(fxl,   7),
                            "f(x_u)":           round(fxu,   7),
                            "f(x_l)·f(x_u)":   round(prod,   7),
                            "Remark":           remark,
                        })
                        if prod < 0:
                            root, iterations, final_err = (curr_x + next_x) / 2, i + 1, abs(step)
                            break
                        curr_x = next_x

                # ── BISECTION METHOD ──
                # Columns: Iteration | x_l | x_r | x_u | f(x_l) | f(x_r) | |ea|% | f(x_l)·f(x_r) | Remark
                elif method == "Bisection Method":
                    _xl, _xu = xl, xu
                    xr_old   = None
                    for i in range(int(max_iter)):
                        xr   = (_xl + _xu) / 2
                        fxl  = float(f(_xl))
                        fxr  = float(f(xr))
                        prod = fxl * fxr
                        first_iter = (xr_old is None)
                        ea   = float('nan') if first_iter else abs((xr - xr_old) / xr) * 100
                        if prod < 0:
                            remark = "Root in [x_l, x_r]"
                        elif prod > 0:
                            remark = "Root in [x_r, x_u]"
                        else:
                            remark = "Exact root"
                        results.append({
                            "Iteration":        i + 1,
                            "x_l":              round(_xl,  7),
                            "x_r":              round(xr,   7),
                            "x_u":              round(_xu,  7),
                            "f(x_l)":           round(fxl,  7),
                            "f(x_r)":           round(fxr,  7),
                            "|ea|%":            "—" if first_iter else round(ea, 6),
                            "f(x_l)·f(x_r)":   round(prod,  7),
                            "Remark":           remark,
                        })
                        xr_old = xr
                        if fxr == 0 or (not first_iter and ea < tol):
                            root, iterations, final_err = xr, i + 1, 0 if first_iter else ea
                            break
                        if prod < 0:
                            _xu = xr
                        else:
                            _xl = xr
                    if root is None and results:
                        root, iterations, final_err = results[-1]["x_r"], len(results), 0

                # ── REGULA-FALSI METHOD ──
                # Columns: No. of Iteration | x_L | x_U | x_R | ea | f(x_L) | f(x_U) | f(x_R) | f(x_L)·f(x_R)
                elif method == "Regula-Falsi Method":
                    _xl, _xu = xl, xu
                    xr_old   = None
                    for i in range(int(max_iter)):
                        fxl = float(f(_xl))
                        fxu = float(f(_xu))
                        xr  = _xu - (fxu * (_xl - _xu)) / (fxl - fxu)
                        fxr = float(f(xr))
                        prod = fxl * fxr
                        first_iter = (xr_old is None)
                        ea   = float('nan') if first_iter else abs((xr - xr_old) / xr) * 100
                        results.append({
                            "No. of Iteration": i + 1,
                            "x_L":              round(_xl, 7),
                            "x_U":              round(_xu, 7),
                            "x_R":              round(xr,  7),
                            "ea":               "—" if first_iter else round(ea, 6),
                            "f(x_L)":           round(fxl, 7),
                            "f(x_U)":           round(fxu, 7),
                            "f(x_R)":           round(fxr, 7),
                            "f(x_L)·f(x_R)":   round(prod, 7),
                        })
                        xr_old = xr
                        if not first_iter and ea < tol:
                            root, iterations, final_err = xr, i + 1, ea
                            break
                        if prod < 0:
                            _xu = xr
                        elif prod > 0:
                            _xl = xr
                        else:
                            root, iterations, final_err = xr, i + 1, 0
                            break
                    if root is None and results:
                        root, iterations, final_err = results[-1]["x_R"], len(results), 0

                # ── NEWTON-RAPHSON METHOD ──
                # Columns: No. of iteration | x_i | ea | f(x) | f'(x)
                elif method == "Newton-Raphson Method":
                    xr = x0
                    for i in range(int(max_iter)):
                        fxr  = float(f(xr))
                        dfxr = float(dfdx(xr))
                        if abs(dfxr) < 1e-14:
                            st.error("Derivative is zero — choose a different initial guess.")
                            break
                        xr_new = xr - fxr / dfxr
                        ea     = abs((xr_new - xr) / xr_new) * 100 if xr_new != 0 else float('nan')
                        results.append({
                            "No. of iteration": i + 1,
                            "x_i":              round(xr_new, 7),
                            "ea":               round(ea,     6) if not (xr_new == 0) else "—",
                            "f(x)":             round(fxr,   7),
                            "f'(x)":            round(dfxr,  7),
                        })
                        xr = xr_new
                        if ea < tol:
                            root, iterations, final_err = xr, i + 1, ea
                            break
                    if root is None and results:
                        root, iterations, final_err = results[-1]["x_i"], len(results), 0

                # ── SECANT METHOD ──
                # Columns: Iteration Number | x_{i-1} | x_i | x_{i+1} | ea | f(x_{i-1}) | f(x_i) | f(x_{i+1})
                elif method == "Secant Method":
                    _x0, _x1 = x0, x1
                    for i in range(int(max_iter)):
                        fx0_ = float(f(_x0))
                        fx1_ = float(f(_x1))
                        denom = fx0_ - fx1_
                        if abs(denom) < 1e-14:
                            st.error("Near-zero denominator — choose different starting points.")
                            break
                        x2   = _x1 - (fx1_ * (_x0 - _x1)) / denom
                        fx2_ = float(f(x2))
                        ea   = abs((x2 - _x1) / x2) * 100 if x2 != 0 else float('nan')
                        results.append({
                            "Iteration Number": i + 1,
                            "x_{i-1}":          round(_x0, 7),
                            "x_i":              round(_x1, 7),
                            "x_{i+1}":          round(x2,  7),
                            "ea":               round(ea,  6) if x2 != 0 else "—",
                            "f(x_{i-1})":       round(fx0_, 7),
                            "f(x_i)":           round(fx1_, 7),
                            "f(x_{i+1})":       round(fx2_, 7),
                        })
                        _x0, _x1 = _x1, x2
                        if ea < tol:
                            root, iterations, final_err = x2, i + 1, ea
                            break
                    if root is None and results:
                        root, iterations, final_err = results[-1]["x_{i+1}"], len(results), 0

                if root is not None:
                    # Build Plotly figure with vintage palette
                    x_vals = np.linspace(root - 3, root + 3, 500)
                    y_vals = f(x_vals)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#5C3317', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.3)
                    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.3)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name=f'Root ≈ {root:.6f}',
                      marker=dict(color='#8B1A1A', size=14, symbol='circle', line=dict(color='#2C1A0E', width=2))
                    ))
                    fig.update_layout(
                        title=dict(text=f"f(x) = {eq_str}", font=dict(family="Playfair Display,serif", size=14, color="#2C1A0E")),
                        xaxis_title="x",  yaxis_title="f(x)",
                        hovermode="x unified",
                        plot_bgcolor='#FBF4E6', paper_bgcolor='#FBF4E6',
                        font=dict(family="Crimson Text,serif", color="#2C1A0E"),
                        xaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882', tickfont=dict(family="Crimson Text,serif")),
                        yaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882', tickfont=dict(family="Crimson Text,serif")),
                        legend=dict(bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1, font=dict(family="Crimson Text,serif")),
                        margin=dict(l=8, r=8, t=38, b=8),
                        height=310,
                    )

                    # Persist to session state
                    st.session_state.rf_results    = results
                    st.session_state.rf_root       = root
                    st.session_state.rf_iterations = iterations
                    st.session_state.rf_error      = final_err
                    st.session_state.rf_fig        = fig
                    st.session_state.rf_eq         = eq_str
                    st.session_state.rf_method     = method

                    # Save to history
                    st.session_state.history.append({
                        "type":      "Root Finding",
                        "method":    method,
                        "equation":  f"f(x) = {eq_str}",
                        "answer":    f"x ≈ {root:.8f}  ({iterations} iters)",
                        "timestamp": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
                    })
                    st.toast("Calculation complete!", icon="✅")
                else:
                    st.warning("No root found within the specified bounds or iterations.")

            except Exception as e:
                st.error(f"Error: Ensure the equation uses valid Python math (e.g., ** for exponents). → {e}")

        # ── DISPLAY PERSISTED RESULTS ──
        if st.session_state.rf_root is not None:
            # METRICS ROW
            m1, m2, m3 = st.columns(3)
            m1.metric("Calculated Root",  f"{st.session_state.rf_root:.8f}")
            m2.metric("Total Iterations", st.session_state.rf_iterations)
            m3.metric("Final Error",
                      f"{st.session_state.rf_error:.3e}" if st.session_state.rf_error else "—")

            # UPPER RIGHT — ITERATION TABLE
            st.markdown('<div class="panel" style="margin-top:0.7rem;">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📊 Iteration Table</div>', unsafe_allow_html=True)
            df_results = pd.DataFrame(st.session_state.rf_results)
            st.dataframe(df_results, use_container_width=True, height=220)
            st.markdown('</div>', unsafe_allow_html=True)

            # LOWER RIGHT — GRAPH
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📈 Function Graph</div>', unsafe_allow_html=True)
            st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
                <div class="panel" style="min-height:520px;">
                    <div class="placeholder-box">
                        ✦ Configure the parameters on the left<br>
                        and press <em>Calculate Root</em> to begin.<br><br>
                        The iteration table and graph will<br>
                        appear here immediately upon solving.
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 — ADVANCED MATRIX OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    st.markdown('<div class="stitle">⊞ Advanced Matrix Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Input matrices using the interactive spreadsheets and execute linear algebra operations instantly.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2.0])

    # ────────────────── LEFT — INPUTS ──────────────────
    with col_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⊞ Configuration</div>', unsafe_allow_html=True)

        op = st.selectbox("Select Operation", [
            "Addition", "Multiplication",
            "System of Equations (Ax = B)",
            "Adjoint", "Inverse", "Determinant",
            "Power of Matrix", "Transpose",
        ])

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Matrix A**")
        ca1, ca2 = st.columns(2)
        rows_A = ca1.number_input("Rows", 1, 10, 3, key="ra")
        cols_A = ca2.number_input("Cols", 1, 10, 3, key="ca")
        df_A     = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"C{i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A        = edited_A.to_numpy()

        needs_B = op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]
        if needs_B:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("**Matrix B**")
            if op == "System of Equations (Ax = B)":
                st.info("Matrix B: single column vector (same rows as A).")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:
                cb1, cb2 = st.columns(2)
                rows_B = cb1.number_input("Rows", 1, 10, int(cols_A), key="rb", disabled=True)
                cols_B = cb2.number_input("Cols", 1, 10, 3, key="cb")
            df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B        = edited_B.to_numpy()

        if op == "Power of Matrix":
            st.markdown("<hr>", unsafe_allow_html=True)
            power = st.number_input("Exponent  n", value=2, step=1)

        st.markdown("<div style='margin-top:0.7rem;'>", unsafe_allow_html=True)
        exec_btn = st.button("⊞  Execute Matrix Operation", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)   # /panel

    # ────────────────── RIGHT — RESULT ──────────────────
    with col_right:
        if exec_btn:
            try:
                with st.spinner("Processing..."):
                    time.sleep(0.35)

                result     = None
                ans_str    = ""
                if op == "Addition":
                    result  = A + B;  ans_str = "Matrix addition complete."
                elif op == "Multiplication":
                    result  = np.matmul(A, B);  ans_str = "Matrix product computed."
                elif op == "Transpose":
                    result  = A.T;  ans_str = "Matrix transposed."
                elif op == "Determinant":
                    det_val = np.linalg.det(A);  ans_str = f"det(A) = {det_val:.6f}"
                elif op == "Inverse":
                    result  = np.linalg.inv(A);  ans_str = "Inverse computed."
                elif op == "Adjoint":
                    result  = np.round(np.linalg.inv(A) * np.linalg.det(A), 6)
                    ans_str = "Adjoint computed."
                elif op == "Power of Matrix":
                    result  = np.linalg.matrix_power(A, int(power))
                    ans_str = f"A^{int(power)} computed."
                elif op == "System of Equations (Ax = B)":
                    result  = np.linalg.solve(A, B);  ans_str = "System solved for X."

                # Persist
                st.session_state.mx_result = {"op": op, "result": result,
                                               "det_val": det_val if op == "Determinant" else None,
                                               "ans_str": ans_str}
                st.session_state.mx_op = op

                # History
                st.session_state.history.append({
                    "type":      "Matrix Operation",
                    "method":    op,
                    "equation":  f"{rows_A}×{cols_A} matrix",
                    "answer":    ans_str,
                    "timestamp": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
                })
                st.toast("Operation successful!", icon="✅")

            except np.linalg.LinAlgError as e:
                st.error(f"Mathematical Error: {e}  (Matrix may be singular / non-invertible.)")
            except ValueError as e:
                st.error(f"Dimension Mismatch: {e}")

        # ── DISPLAY PERSISTED MATRIX RESULT ──
        if st.session_state.mx_result:
            r = st.session_state.mx_result
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="panel-title">⊞ Result — {r["op"]}</div>', unsafe_allow_html=True)

            if r["op"] == "Determinant":
                st.metric("Determinant Value", f'{r["det_val"]:.6f}')
            else:
                if r["op"] == "System of Equations (Ax = B)":
                    st.success("✦  Solutions found for Vector X:")
                if r["result"] is not None:
                    st.dataframe(
                        pd.DataFrame(r["result"]).style.format("{:.6g}"),
                        use_container_width=True,
                        height=420,
                    )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="panel" style="min-height:460px;">
                    <div class="placeholder-box">
                        ✦ Enter your matrix values on the left<br>
                        and press <em>Execute Matrix Operation</em>.<br><br>
                        The result will appear here immediately.
                    </div>
                </div>
            """, unsafe_allow_html=True)V
