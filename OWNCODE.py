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


## ==========================================
# MODULE 1: ROOT FINDING
# ==========================================
if app_mode == "Root Finding Analysis":
    st.title("Root Finding Analysis")
    st.markdown("Analyze equations and find roots using numerical methods with interactive visualizations.")
    
    col_input, col_results = st.columns([1, 2.5])
    
    with col_input:
        st.subheader("Parameters")
        eq_str = st.text_input("Equation f(x)", value="3*x + sin(x) - exp(x)", help="Use standard Python math (e.g. x**3 or x^3, sin(x), exp(x))")
        method = st.selectbox("Algorithm", ["Incremental Search", "Bisection Method", "Regula-Falsi", "Newton-Raphson", "Secant Method"])
        
        # Dynamic inputs based strictly on the provided documents
        if method == "Incremental Search":
            xl = st.number_input("Initial Value (xl)", value=0.0, format="%.4f")
            delta_x = st.number_input("Initial Increment (Δx)", value=0.5, format="%.4f")
        elif method in ["Bisection Method", "Regula-Falsi"]:
            xl = st.number_input("Lower Bound (xl)", value=-0.5 if method == "Regula-Falsi" else 0.4, format="%.4f")
            xu = st.number_input("Upper Bound (xu)", value=1.0 if method == "Regula-Falsi" else 0.6, format="%.4f")
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess (xi)", value=-5.0, format="%.4f")
        elif method == "Secant Method":
            x_prev = st.number_input("First Guess (x_i-1)", value=0.5, format="%.4f")
            x0 = st.number_input("Second Guess (x_i)", value=5.0, format="%.4f")
            
        tol = st.number_input("Tolerance (Stopping Criterion)", value=0.001, format="%.5f")
        max_iter = st.number_input("Max Iterations", value=50, step=1)
        solve_btn = st.button("Calculate Root")

    with col_results:
        if solve_btn:
            try:
                x = sp.Symbol('x')
                safe_eq_str = eq_str.replace('^', '**')
                expr = sp.sympify(safe_eq_str)
                f = sp.lambdify(x, expr, 'numpy')
                df = sp.lambdify(x, sp.diff(expr, x), 'numpy')

                results, root, iterations, final_err = [], None, 0, 0
                
                # --- 1. INCREMENTAL SEARCH ---
                if method == "Incremental Search":
                    curr_xl = xl
                    curr_dx = delta_x
                    
                    for i in range(max_iter):
                        curr_xu = curr_xl + curr_dx
                        fxl, fxu = f(curr_xl), f(curr_xu)
                        prod = fxl * fxu
                        
                        if prod > 0:
                            remark = "Go to next interval"
                        else:
                            remark = "Revert back to xl & consider smaller interval"
                            
                        # Matching PDF Table Columns
                        results.append({
                            "Iteration": i + 1,
                            "x_l": curr_xl,
                            "Δx": curr_dx,
                            "x_u": curr_xu,
                            "f(x_l)": fxl,
                            "f(x_u)": fxu,
                            "f(x_l)*f(x_u)": "> 0" if prod > 0 else "< 0",
                            "Remark": remark
                        })
                        
                        if abs(fxu) < tol or curr_dx < (tol / 10):
                            root, iterations = curr_xu, i + 1
                            break
                            
                        if prod > 0:
                            curr_xl = curr_xu  # Go to next interval
                        else:
                            curr_dx = curr_dx / 10.0  # Reduce interval step
                            
                # --- 2. BISECTION METHOD ---
                elif method == "Bisection Method":
                    if f(xl) * f(xu) > 0:
                        st.warning("f(xl) and f(xu) must have opposite signs for Bisection.")
                        st.stop()
                        
                    xr_old = None
                    for i in range(max_iter):
                        xr = (xl + xu) / 2
                        fxl, fxr = f(xl), f(xr)
                        prod = fxl * fxr
                        
                        ea = abs((xr - xr_old) / xr) * 100 if xr_old is not None else None
                        
                        if prod < 0:
                            remark = "1st subinterval"
                        else:
                            remark = "2nd subinterval"
                            
                        # Matching PDF Table Columns
                        results.append({
                            "Iteration": i + 1,
                            "x_l": xl,
                            "x_r": xr,
                            "x_u": xu,
                            "f(x_l)": fxl,
                            "f(x_r)": fxr,
                            "|E_a| %": ea if ea is not None else "",
                            "f(x_l)*f(x_r)": "< 0" if prod < 0 else "> 0",
                            "Remark": remark
                        })
                        
                        if (ea is not None and ea < tol) or fxr == 0:
                            root, iterations, final_err = xr, i + 1, ea
                            break
                            
                        if prod < 0:
                            xu = xr
                        else:
                            xl = xr
                        xr_old = xr

                # --- 3. REGULA-FALSI (FALSE POSITION) ---
                elif method == "Regula-Falsi":
                    if f(xl) * f(xu) > 0:
                        st.warning("f(xl) and f(xu) must have opposite signs for Regula-Falsi.")
                        st.stop()
                        
                    xr_old = None
                    for i in range(max_iter):
                        fxl, fxu = f(xl), f(xu)
                        if fxl - fxu == 0:
                            st.error("Division by zero encountered.")
                            break
                            
                        xr = (xu * fxl - xl * fxu) / (fxl - fxu)
                        fxr = f(xr)
                        prod = fxl * fxr
                        
                        ea = abs((xr - xr_old) / xr) if xr_old is not None else None
                        
                        # Matching PDF Table Columns
                        results.append({
                            "No. of Iteration": i + 1,
                            "x_L": xl,
                            "x_U": xu,
                            "x_R": xr,
                            "E_a": ea if ea is not None else "",
                            "f(x_L)": fxl,
                            "f(x_U)": fxu,
                            "f(x_R)": fxr,
                            "f(x_L)*f(x_R)": "< 0" if prod < 0 else "> 0"
                        })
                        
                        if (ea is not None and ea < tol) or fxr == 0:
                            root, iterations, final_err = xr, i + 1, ea
                            break
                            
                        if prod < 0:
                            xu = xr
                        else:
                            xl = xr
                        xr_old = xr

                # --- 4. NEWTON-RAPHSON ---
                elif method == "Newton-Raphson":
                    xi = x0
                    # Initial state (Iteration 0) matching PDF format
                    results.append({
                        "No. of iteration": 0,
                        "x_i": xi,
                        "E_a": "",
                        "f(x)": f(xi),
                        "f'(x)": df(xi)
                    })
                    
                    for i in range(max_iter):
                        fxi, dfxi = f(xi), df(xi)
                        if dfxi == 0:
                            st.error("Derivative became zero. Newton-Raphson fails.")
                            break
                            
                        xi_new = xi - fxi / dfxi
                        ea = abs((xi_new - xi) / xi_new)
                        
                        xi = xi_new
                        # Matching PDF Table Columns
                        results.append({
                            "No. of iteration": i + 1,
                            "x_i": xi,
                            "E_a": ea,
                            "f(x)": f(xi),
                            "f'(x)": df(xi)
                        })
                        
                        if ea < tol:
                            root, iterations, final_err = xi, i + 1, ea
                            break

                # --- 5. SECANT METHOD ---
                elif method == "Secant Method":
                    xi_prev, xi = x_prev, x0
                    for i in range(max_iter):
                        fxi, fxi_prev = f(xi), f(xi_prev)
                        if fxi - fxi_prev == 0:
                            st.error("Difference between f(x_i) and f(x_i-1) is zero. Secant fails.")
                            break
                            
                        xi_new = xi - (fxi * (xi - xi_prev)) / (fxi - fxi_prev)
                        ea = abs((xi_new - xi) / xi_new)
                        
                        # Matching Word Document Table Columns
                        results.append({
                            "Iteration Number": i + 1,
                            "x_{i-1}": xi_prev,
                            "x_i": xi,
                            "x_{i+1}": xi_new,
                            "E_a": ea,
                            "f(x_{i-1})": fxi_prev,
                            "f(x_i)": fxi,
                            "f(x_{i+1})": f(xi_new)
                        })
                        
                        xi_prev, xi = xi, xi_new
                        if ea < tol:
                            root, iterations, final_err = xi_new, i + 1, ea
                            break

                # --- METRICS & GRAPH ---
                if len(results) > 0:
                    if root is not None:
                        st.toast('Calculation Complete!', icon='✅')
                    else:
                        st.toast('Max iterations reached or stopped.', icon='⚠️')
                        # Extract the best guess for graph centering
                        latest_row = results[-1]
                        root = latest_row.get("x_u", latest_row.get("x_R", latest_row.get("x_i", latest_row.get("x_{i+1}", 0))))
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Calculated Root", f"{root:.6f}")
                    m2.metric("Total Iterations", iterations if iterations > 0 else max_iter)
                    m3.metric("Final Error (E_a)", f"{final_err:.6f}" if final_err else "N/A")
                    st.divider()

                    # Interactive Plotly Graph
                    x_vals = np.linspace(float(root) - 3, float(root) + 3, 300)
                    y_vals = f(x_vals)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)', line=dict(color='royalblue', width=2)))
                    fig.add_hline(y=0, line_dash="dash", line_color="black")
                    fig.add_vline(x=0, line_dash="dash", line_color="black")
                    fig.add_trace(go.Scatter(x=[root], y=[0], mode='markers', name='Root', marker=dict(color='red', size=12, symbol='x')))
                    
                    fig.update_layout(title="Interactive Function Graph", xaxis_title="X Axis", yaxis_title="Y Axis", hovermode="x unified", margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                    # Dynamic Expander Table - Pandas automatically reads the dictionaries and sets the exact headers
                    with st.expander("📊 View Detailed Iteration History", expanded=True):
                        st.dataframe(pd.DataFrame(results), use_container_width=True)

            except Exception as e:
                st.error(f"Error evaluating equation or solving. Details: {e}")

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

                if method == "Bisection Method":
                    _xl, _xu = xl, xu
                    for i in range(int(max_iter)):
                        xr  = (_xl + _xu) / 2
                        err = abs(_xu - _xl) / 2
                        results.append({"Iter": i+1, "xl": round(_xl,7), "xu": round(_xu,7),
                                         "xr": round(xr,7), "f(xr)": round(float(f(xr)),7), "Error": round(err,8)})
                        if f(xr) == 0 or err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(_xl) * f(xr) < 0: _xu = xr
                        else: _xl = xr

                elif method == "Regula-Falsi Method":
                    _xl, _xu = xl, xu
                    for i in range(int(max_iter)):
                        xr  = _xu - (f(_xu) * (_xl - _xu)) / (f(_xl) - f(_xu))
                        err = abs(f(xr))
                        results.append({"Iter": i+1, "xl": round(_xl,7), "xu": round(_xu,7),
                                         "xr": round(xr,7), "f(xr)": round(float(f(xr)),7), "Error": round(err,8)})
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(_xl) * f(xr) < 0: _xu = xr
                        else: _xl = xr

                elif method == "Newton-Raphson Method":
                    xr = x0
                    for i in range(int(max_iter)):
                        fxr, dfxr = f(xr), dfdx(xr)
                        xr_new = xr - fxr / dfxr
                        err = abs(xr_new - xr)
                        results.append({"Iter": i+1, "xi": round(xr,7),
                                         "f(xi)": round(float(fxr),7), "f'(xi)": round(float(dfxr),7),
                                         "xi+1": round(xr_new,7), "Error": round(err,8)})
                        xr = xr_new
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break

                elif method == "Secant Method":
                    _x0, _x1 = x0, x1
                    for i in range(int(max_iter)):
                        fx1_, fx0_ = f(_x1), f(_x0)
                        x2  = _x1 - (fx1_ * (_x0 - _x1)) / (fx0_ - fx1_)
                        err = abs(x2 - _x1)
                        results.append({"Iter": i+1, "x(i-1)": round(_x0,7), "x(i)": round(_x1,7),
                                         "x(i+1)": round(x2,7), "f(x(i+1))": round(float(f(x2)),7), "Error": round(err,8)})
                        _x0, _x1 = _x1, x2
                        if err < tol:
                            root, iterations, final_err = x2, i+1, err; break

                elif method == "Incremental Method":
                    step, curr_x = 0.1, xl
                    for i in range(int(max_iter)):
                        next_x = curr_x + step
                        results.append({"Iter": i+1, "x": round(curr_x,7), "f(x)": round(float(f(curr_x)),7)})
                        if f(curr_x) * f(next_x) < 0:
                            root, iterations, final_err = (curr_x + next_x) / 2, i+2, 0; break
                        curr_x = next_x

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
            """, unsafe_allow_html=True)
