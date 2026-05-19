import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Numerical Project — Penaso",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VINTAGE BROWN ACADEMIC CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Crimson+Pro:wght@300;400;500&display=swap');

/* ── ROOT PALETTE ── */
:root {
    --cream:        #F5EFE0;
    --parchment:    #EDE3C8;
    --tan:          #D4B896;
    --caramel:      #B8936A;
    --brown:        #8B5E3C;
    --coffee:       #5C3D1E;
    --espresso:     #3A2410;
    --ink:          #2B1A0E;
    --gold:         #C9973A;
    --gold-light:   #E8C47A;
    --shadow:       rgba(58,36,16,0.18);
    --shadow-deep:  rgba(58,36,16,0.32);
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"], .stApp {
    background-color: var(--cream) !important;
    font-family: 'EB Garamond', serif !important;
    color: var(--ink) !important;
}

/* ── HIDE DEFAULT STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOP HEADER BANNER ── */
.top-banner {
    background: linear-gradient(135deg, var(--espresso) 0%, var(--coffee) 45%, var(--brown) 100%);
    padding: 18px 40px 14px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid var(--gold);
    box-shadow: 0 4px 18px var(--shadow-deep);
    position: relative;
}
.top-banner::after {
    content: '';
    position: absolute;
    bottom: -7px; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--gold-light), transparent);
}
.banner-left {
    font-family: 'Crimson Pro', serif;
    font-size: 0.82rem;
    font-weight: 300;
    color: var(--tan);
    letter-spacing: 0.08em;
    line-height: 1.5;
}
.banner-left strong {
    display: block;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--gold-light);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.banner-center {
    text-align: center;
    flex: 1;
}
.banner-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--cream);
    letter-spacing: 0.05em;
    line-height: 1;
    text-shadow: 0 2px 8px var(--shadow-deep);
}
.banner-subtitle {
    font-family: 'Crimson Pro', serif;
    font-size: 0.78rem;
    color: var(--gold-light);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 3px;
}
.banner-ornament {
    color: var(--gold);
    font-size: 1.2rem;
    letter-spacing: 0.3em;
    display: block;
    margin-top: 2px;
}
.banner-right {
    font-family: 'Crimson Pro', serif;
    font-size: 0.78rem;
    color: var(--tan);
    text-align: right;
    letter-spacing: 0.06em;
}

/* ── METHOD SELECTOR BAR ── */
.selector-bar {
    background: linear-gradient(90deg, var(--coffee) 0%, var(--espresso) 100%);
    padding: 12px 40px;
    border-bottom: 2px solid var(--caramel);
    display: flex;
    align-items: center;
    gap: 30px;
}
.selector-label {
    font-family: 'Crimson Pro', serif;
    font-size: 0.78rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--tan);
}

/* ── MAIN CONTENT WRAPPER ── */
.main-wrapper {
    padding: 22px 30px 30px 30px;
    background: var(--cream);
}

/* ── PANEL CARDS ── */
.panel-card {
    background: linear-gradient(160deg, #FDFAF3 0%, var(--parchment) 100%);
    border: 1px solid var(--tan);
    border-radius: 12px;
    padding: 22px 20px;
    box-shadow: 0 4px 16px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.6);
    position: relative;
}
.panel-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--brown), var(--gold), var(--brown));
    border-radius: 12px 12px 0 0;
}

/* ── PANEL HEADINGS ── */
.panel-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.0rem;
    font-weight: 600;
    color: var(--coffee);
    letter-spacing: 0.04em;
    border-bottom: 1px solid var(--tan);
    padding-bottom: 8px;
    margin-bottom: 16px;
}
.panel-heading-sm {
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--brown);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stRadio label {
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--coffee) !important;
    letter-spacing: 0.04em !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #FBF7EE !important;
    border: 1px solid var(--caramel) !important;
    border-radius: 7px !important;
    color: var(--ink) !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 0.9rem !important;
    box-shadow: inset 0 1px 4px rgba(139,94,60,0.10) !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--brown) !important;
    box-shadow: 0 0 0 2px rgba(139,94,60,0.20) !important;
}

/* ── SOLVE BUTTON ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--coffee) 0%, var(--brown) 100%) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    padding: 0.55rem 1rem !important;
    box-shadow: 0 3px 10px var(--shadow-deep) !important;
    transition: all 0.25s ease !important;
    border-top: 1px solid rgba(255,255,255,0.15) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--brown) 0%, var(--caramel) 100%) !important;
    box-shadow: 0 5px 18px var(--shadow-deep) !important;
    transform: translateY(-1px) !important;
}

/* ── METRIC CARDS ── */
.metric-row { display: flex; gap: 12px; margin-bottom: 16px; }
.metric-box {
    flex: 1;
    background: linear-gradient(135deg, var(--coffee) 0%, var(--espresso) 100%);
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
    box-shadow: 0 3px 10px var(--shadow-deep);
    border: 1px solid var(--brown);
}
.metric-label {
    font-family: 'Crimson Pro', serif;
    font-size: 0.7rem;
    color: var(--tan);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--gold-light);
    letter-spacing: 0.02em;
}

/* ── ITERATION TABLE ── */
.iter-table-wrapper {
    overflow-y: auto;
    max-height: 280px;
    border-radius: 8px;
    border: 1px solid var(--tan);
}
.iter-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Crimson Pro', serif;
    font-size: 0.82rem;
}
.iter-table thead tr {
    background: linear-gradient(90deg, var(--coffee), var(--brown));
    position: sticky;
    top: 0;
    z-index: 2;
}
.iter-table thead th {
    padding: 9px 10px;
    color: var(--cream);
    font-weight: 500;
    letter-spacing: 0.08em;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.12);
    font-size: 0.78rem;
    text-transform: uppercase;
}
.iter-table tbody tr {
    background: #FDFAF3;
    transition: background 0.15s;
}
.iter-table tbody tr:nth-child(even) { background: var(--parchment); }
.iter-table tbody tr:hover { background: #EDD9B8; }
.iter-table tbody td {
    padding: 7px 10px;
    text-align: center;
    border-right: 1px solid var(--tan);
    border-bottom: 1px solid rgba(180,150,100,0.2);
    color: var(--espresso);
}

/* ── HISTORY PANEL ── */
.history-entry {
    background: linear-gradient(135deg, #FBF7EE 0%, var(--parchment) 100%);
    border: 1px solid var(--tan);
    border-left: 4px solid var(--brown);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 10px;
    font-family: 'Crimson Pro', serif;
    font-size: 0.82rem;
    color: var(--espresso);
    box-shadow: 0 2px 6px var(--shadow);
}
.history-method {
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--coffee);
    margin-bottom: 2px;
}
.history-meta {
    color: var(--brown);
    font-size: 0.75rem;
    letter-spacing: 0.04em;
}

/* ── SECTION DIVIDER ── */
.ornament-divider {
    text-align: center;
    color: var(--caramel);
    font-size: 0.9rem;
    letter-spacing: 0.5em;
    margin: 4px 0 12px 0;
    opacity: 0.6;
}

/* ── RADIO BUTTONS ── */
.stRadio > div { flex-direction: row !important; gap: 20px !important; flex-wrap: wrap !important; }
.stRadio > div > label {
    background: var(--parchment) !important;
    border: 1px solid var(--caramel) !important;
    border-radius: 20px !important;
    padding: 5px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
.stRadio > div > label:hover {
    background: var(--tan) !important;
    border-color: var(--brown) !important;
}

/* ── DATA EDITOR (MATRIX) ── */
.stDataEditor { border: 1px solid var(--tan) !important; border-radius: 8px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: var(--parchment); border-radius: 4px; }
::-webkit-scrollbar-thumb { background: var(--caramel); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--brown); }

/* ── PLOTLY CHART ── */
.js-plotly-plot .plotly { border-radius: 10px !important; }

/* ── SECTION TABS (module selector) ── */
.module-tab {
    display: inline-block;
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 7px 22px;
    border-radius: 20px;
    cursor: pointer;
    border: 1px solid var(--caramel);
    color: var(--tan);
    background: transparent;
    transition: all 0.2s;
}
.module-tab.active {
    background: var(--gold);
    color: var(--espresso);
    border-color: var(--gold);
    box-shadow: 0 2px 8px var(--shadow);
}

/* stSelectbox dropdown */
.stSelectbox div[data-baseweb="select"] > div {
    background: #FBF7EE !important;
    border: 1px solid var(--caramel) !important;
    border-radius: 7px !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "history" not in st.session_state:
    st.session_state.history = []

# ══════════════════════════════════════════════
# TOP HEADER BANNER
# ══════════════════════════════════════════════
st.markdown("""
<div class="top-banner">
    <div class="banner-left">
        <strong>DIOSAMABEL B. PENASO</strong>
        BSCOMPE-2
    </div>
    <div class="banner-center">
        <div class="banner-title">NUMERICAL PROJECT</div>
        <div class="banner-subtitle">Computational Methods &amp; Analysis</div>
        <span class="banner-ornament">✦ &nbsp; ✦ &nbsp; ✦</span>
    </div>
    <div class="banner-right">
        Numerical Methods<br>Laboratory
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# MODULE SELECTOR BAR
# ══════════════════════════════════════════════
st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

sel_col1, sel_col2, sel_col3 = st.columns([1, 2, 1])
with sel_col2:
    app_mode = st.radio(
        "**Select Module**",
        ["Root Finding Analysis", "Advanced Matrix Operations"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown('<div class="ornament-divider">— ✦ —</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# MODULE 1 — ROOT FINDING
# ══════════════════════════════════════════════
if app_mode == "Root Finding Analysis":

    main_left, main_right = st.columns([1, 2.2], gap="medium")

    # ── LEFT: INPUTS ──
    with main_left:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">⚙ Parameters &amp; Configuration</div>', unsafe_allow_html=True)

        eq_str = st.text_input("Equation  f(x)", value="x**3 - x - 2",
                               help="Use Python math syntax. E.g. x**2 - 4, sin(x) - x/2")

        method = st.selectbox("Numerical Method", [
            "Bisection Method",
            "Regula-Falsi",
            "Incremental Search",
            "Newton-Raphson",
            "Secant Method"
        ])

        st.markdown('<div class="ornament-divider" style="margin:8px 0">— ✦ —</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading-sm">Boundary / Initial Values</div>', unsafe_allow_html=True)

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            c1, c2 = st.columns(2)
            with c1:
                xl = st.number_input("Lower Bound (xₗ)", value=1.0, format="%.4f")
            with c2:
                xu = st.number_input("Upper Bound (xᵤ)", value=2.0, format="%.4f")
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess (x₀)", value=1.0, format="%.4f")
        elif method == "Secant Method":
            c1, c2 = st.columns(2)
            with c1:
                x0 = st.number_input("First Guess (x₀)", value=1.0, format="%.4f")
            with c2:
                x1 = st.number_input("Second Guess (x₁)", value=2.0, format="%.4f")

        st.markdown('<div class="ornament-divider" style="margin:8px 0">— ✦ —</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading-sm">Stopping Criteria</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            tol = st.number_input("Tolerance (εₛ)", value=0.0001, format="%.6f")
        with c2:
            max_iter = st.number_input("Max Iterations", value=50, step=1, min_value=1)

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        solve_btn = st.button("▶  Calculate Root", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── HISTORY PANEL (below inputs) ──
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">📜 Calculation History</div>', unsafe_allow_html=True)

        if st.session_state.history:
            hist_container = st.container()
            with hist_container:
                for entry in reversed(st.session_state.history[-8:]):
                    st.markdown(f"""
                    <div class="history-entry">
                        <div class="history-method">{entry['method']}</div>
                        <div>f(x) = <em>{entry['equation']}</em></div>
                        <div>Root ≈ <strong>{entry['root']}</strong> &nbsp;|&nbsp; {entry['iters']} iters</div>
                        <div class="history-meta">{entry['datetime']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            if st.button("🗑  Clear History", use_container_width=True):
                st.session_state.history = []
                st.rerun()
        else:
            st.markdown("""
            <div style="text-align:center; padding:20px; color:#8B7355;
                font-family:'Crimson Pro',serif; font-style:italic; font-size:0.9rem;">
                No calculations yet.<br>Results will appear here automatically.
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: RESULTS ──
    with main_right:

        if solve_btn:
            try:
                x_sym = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f = sp.lambdify(x_sym, expr, 'numpy')
                df_func = sp.lambdify(x_sym, sp.diff(expr, x_sym), 'numpy')

                results, root, iterations, final_err = [], None, 0, 0.0

                # ── ALGORITHMS ──
                if method == "Bisection Method":
                    xl_cur, xu_cur = xl, xu
                    for i in range(int(max_iter)):
                        xr = (xl_cur + xu_cur) / 2
                        err = abs(xu_cur - xl_cur) / 2 if i > 0 else None
                        results.append({
                            "Iter": i+1,
                            "xₗ": round(xl_cur, 6),
                            "xᵤ": round(xu_cur, 6),
                            "xᵣ": round(xr, 6),
                            "f(xₗ)": round(float(f(xl_cur)), 6),
                            "f(xᵣ)": round(float(f(xr)), 6),
                            "Error": round(err, 8) if err else "—",
                            "Subinterval": "1st" if f(xl_cur)*f(xr) < 0 else "2nd"
                        })
                        if f(xr) == 0 or (err is not None and err < tol):
                            root, iterations, final_err = xr, i+1, (err or 0)
                            break
                        if f(xl_cur) * f(xr) < 0:
                            xu_cur = xr
                        else:
                            xl_cur = xr
                        if i == int(max_iter)-1:
                            root, iterations, final_err = xr, i+1, (err or 0)

                elif method == "Regula-Falsi":
                    xl_cur, xu_cur = xl, xu
                    xr_old = None
                    for i in range(int(max_iter)):
                        denom = f(xl_cur) - f(xu_cur)
                        if denom == 0: break
                        xr = xu_cur - (f(xu_cur)*(xl_cur - xu_cur)) / denom
                        err = abs((xr - xr_old)/xr * 100) if xr_old and xr != 0 else None
                        results.append({
                            "Iter": i+1,
                            "xₗ": round(xl_cur, 6),
                            "xᵤ": round(xu_cur, 6),
                            "xᵣ": round(xr, 6),
                            "f(xₗ)": round(float(f(xl_cur)), 6),
                            "f(xᵤ)": round(float(f(xu_cur)), 6),
                            "f(xᵣ)": round(float(f(xr)), 6),
                            "εₐ %": round(err, 6) if err else "—",
                            "f(xₗ)·f(xᵣ)": "<0" if float(f(xl_cur))*float(f(xr)) < 0 else ">0"
                        })
                        if err is not None and abs(err) < tol * 100:
                            root, iterations, final_err = xr, i+1, (err or 0)
                            break
                        if float(f(xl_cur)) * float(f(xr)) < 0:
                            xu_cur = xr
                        else:
                            xl_cur = xr
                        xr_old = xr
                        if i == int(max_iter)-1:
                            root, iterations, final_err = xr, i+1, (err or 0)

                elif method == "Newton-Raphson":
                    xr = x0
                    for i in range(int(max_iter)):
                        fxr = float(f(xr))
                        dfxr = float(df_func(xr))
                        if dfxr == 0: break
                        xr_new = xr - fxr/dfxr
                        err = abs((xr_new - xr)/xr_new * 100) if xr_new != 0 else abs(xr_new - xr)
                        results.append({
                            "Iter": i+1,
                            "xᵢ": round(xr, 6),
                            "f(xᵢ)": round(fxr, 6),
                            "f′(xᵢ)": round(dfxr, 6),
                            "xᵢ₊₁": round(xr_new, 6),
                            "εₐ": round(err, 6)
                        })
                        xr = xr_new
                        if err < tol * 100:
                            root, iterations, final_err = xr, i+1, err
                            break
                        if i == int(max_iter)-1:
                            root, iterations, final_err = xr, i+1, err

                elif method == "Secant Method":
                    x0_c, x1_c = x0, x1
                    for i in range(int(max_iter)):
                        fx1, fx0 = float(f(x1_c)), float(f(x0_c))
                        denom = fx0 - fx1
                        if denom == 0: break
                        x2 = x1_c - (fx1 * (x0_c - x1_c)) / denom
                        err = abs((x2 - x1_c)/x2 * 100) if x2 != 0 else abs(x2 - x1_c)
                        results.append({
                            "Iter": i+1,
                            "x(i-1)": round(x0_c, 6),
                            "x(i)": round(x1_c, 6),
                            "x(i+1)": round(x2, 6),
                            "f(x(i+1))": round(float(f(x2)), 6),
                            "εₐ": round(err, 6)
                        })
                        x0_c, x1_c = x1_c, x2
                        if err < tol * 100:
                            root, iterations, final_err = x2, i+1, err
                            break
                        if i == int(max_iter)-1:
                            root, iterations, final_err = x2, i+1, err

                elif method == "Incremental Search":
                    step, curr_x = 0.1, xl
                    xr_old = None
                    i = 0
                    while i < int(max_iter):
                        next_x = curr_x + step
                        fc = float(f(curr_x))
                        fn = float(f(next_x))
                        err = None
                        if xr_old is not None and curr_x != 0:
                            err = abs((curr_x - xr_old)/curr_x * 100)
                        results.append({
                            "Iter": i+1,
                            "xₗ": round(curr_x, 6),
                            "Δx": round(step, 6),
                            "xᵤ": round(next_x, 6),
                            "f(xₗ)": round(fc, 6),
                            "f(xᵤ)": round(fn, 6),
                            "f(xₗ)·f(xᵤ)": round(fc*fn, 8),
                            "Remark": "Sign Change — Revert" if fc*fn < 0 else "Go to next interval"
                        })
                        if fc * fn < 0:
                            root_cand = (curr_x + next_x)/2
                            if err is not None and abs(err) < tol * 100:
                                root, iterations, final_err = root_cand, i+1, (err or 0)
                                break
                            xr_old = curr_x
                            step /= 10
                        else:
                            xr_old = curr_x
                            curr_x = next_x
                        i += 1
                        if root is None and i == int(max_iter):
                            root = (curr_x + next_x)/2
                            iterations = i
                            final_err = 0

                if root is not None:
                    # Save to history
                    st.session_state.history.append({
                        "method": method,
                        "equation": eq_str,
                        "root": f"{root:.6f}",
                        "iters": iterations,
                        "datetime": datetime.now().strftime("%b %d, %Y  %H:%M")
                    })

                    # ── METRIC CARDS ──
                    st.markdown(f"""
                    <div class="metric-row">
                        <div class="metric-box">
                            <div class="metric-label">Calculated Root</div>
                            <div class="metric-value">{root:.6f}</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">Total Iterations</div>
                            <div class="metric-value">{iterations}</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">Final Error</div>
                            <div class="metric-value">{f"{final_err:.6f}" if final_err else "—"}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── ITERATION TABLE ──
                    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="panel-heading">📊 Iteration Table — {method}</div>', unsafe_allow_html=True)

                    df_results = pd.DataFrame(results)
                    cols = list(df_results.columns)

                    # Build HTML table
                    thead = "".join([f"<th>{c}</th>" for c in cols])
                    tbody_rows = ""
                    for _, row in df_results.iterrows():
                        tds = ""
                        for c in cols:
                            val = row[c]
                            tds += f"<td>{val}</td>"
                        tbody_rows += f"<tr>{tds}</tr>"

                    table_html = f"""
                    <div class="iter-table-wrapper">
                        <table class="iter-table">
                            <thead><tr>{thead}</tr></thead>
                            <tbody>{tbody_rows}</tbody>
                        </table>
                    </div>
                    """
                    st.markdown(table_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

                    # ── GRAPH ──
                    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                    st.markdown('<div class="panel-heading">📈 Function Graph</div>', unsafe_allow_html=True)

                    span = max(3, abs(root) * 1.5)
                    x_vals = np.linspace(root - span, root + span, 400)
                    try:
                        y_vals = f(x_vals)
                        y_vals = np.where(np.abs(y_vals) > 1e6, np.nan, y_vals)
                    except:
                        y_vals = np.zeros_like(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#8B5E3C', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="#5C3D1E", line_width=1)
                    fig.add_vline(x=0, line_dash="dash", line_color="#5C3D1E", line_width=1)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name=f'Root ≈ {root:.5f}',
                        marker=dict(color='#C9973A', size=14, symbol='x',
                                    line=dict(width=3, color='#3A2410'))
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(253,250,243,0)',
                        plot_bgcolor='rgba(253,250,243,0.6)',
                        font=dict(family='EB Garamond', color='#3A2410', size=12),
                        margin=dict(l=10, r=10, t=30, b=10),
                        height=320,
                        legend=dict(
                            bgcolor='rgba(237,227,200,0.85)',
                            bordercolor='#B8936A', borderwidth=1,
                            font=dict(family='Crimson Pro', size=12)
                        ),
                        xaxis=dict(
                            gridcolor='rgba(180,150,100,0.25)',
                            zeroline=False,
                            title='x',
                            titlefont=dict(family='Playfair Display', size=12)
                        ),
                        yaxis=dict(
                            gridcolor='rgba(180,150,100,0.25)',
                            zeroline=False,
                            title='f(x)',
                            titlefont=dict(family='Playfair Display', size=12)
                        ),
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.warning("No root found within the given parameters. Adjust your bounds or initial guess.")

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            # Placeholder when nothing is solved yet
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                height:460px; background:linear-gradient(160deg,#FDFAF3,#EDE3C8);
                border:1px solid #D4B896; border-radius:12px; text-align:center;
                box-shadow:0 4px 16px rgba(58,36,16,0.12);">
                <div style="font-size:3rem; margin-bottom:16px; opacity:0.4;">📐</div>
                <div style="font-family:'Playfair Display',serif; font-size:1.3rem;
                    color:#5C3D1E; font-weight:600; margin-bottom:8px;">
                    Awaiting Computation
                </div>
                <div style="font-family:'Crimson Pro',serif; font-size:0.92rem;
                    color:#8B7355; max-width:300px; line-height:1.6; font-style:italic;">
                    Configure your parameters on the left and press<br>
                    <em>Calculate Root</em> to begin the analysis.
                </div>
                <div style="margin-top:20px; color:#B8936A; font-size:0.85rem;
                    letter-spacing:0.3em; font-family:'Crimson Pro',serif;">
                    ✦ &nbsp; ✦ &nbsp; ✦
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# MODULE 2 — MATRIX OPERATIONS
# ══════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":

    st.markdown('<div style="padding:0 4px">', unsafe_allow_html=True)

    # Operation selector
    op_col1, op_col2, op_col3 = st.columns([1, 2, 1])
    with op_col2:
        op = st.selectbox("**Select Matrix Operation**", [
            "Addition", "Multiplication",
            "System of Equations (Ax = B)",
            "Adjoint", "Inverse", "Determinant",
            "Power of Matrix", "Transpose"
        ])

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # ── MATRIX INPUT PANELS ──
    if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
        mat_col1, mat_col2 = st.columns(2, gap="medium")
    else:
        mat_col1, mat_col2 = st.columns([1, 1], gap="medium")

    with mat_col1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">Matrix A</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        rows_A = c1.number_input("Rows", 1, 10, 3, key="rA")
        cols_A = c2.number_input("Cols", 1, 10, 3, key="cA")
        df_A = pd.DataFrame(np.zeros((int(rows_A), int(cols_A))),
                            columns=[f"C{i+1}" for i in range(int(cols_A))])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A = edited_A.to_numpy()
        st.markdown('</div>', unsafe_allow_html=True)

    if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
        with mat_col2:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">Matrix B</div>', unsafe_allow_html=True)
            if op == "System of Equations (Ax = B)":
                st.info("B must be a single-column results vector.")
                rows_B, cols_B = int(rows_A), 1
            elif op == "Addition":
                rows_B, cols_B = int(rows_A), int(cols_A)
            else:
                c1, c2 = st.columns(2)
                rows_B = int(cols_A)
                cols_B = c2.number_input("Cols B", 1, 10, 3, key="cB")
            df_B = pd.DataFrame(np.zeros((rows_B, cols_B)),
                                columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B = edited_B.to_numpy()
            st.markdown('</div>', unsafe_allow_html=True)

    if op == "Power of Matrix":
        with mat_col2:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">Settings</div>', unsafe_allow_html=True)
            power = st.number_input("Power (n)", value=2, step=1)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    btn_c1, btn_c2, btn_c3 = st.columns([1, 2, 1])
    with btn_c2:
        exec_btn = st.button("▶  Execute Matrix Operation", use_container_width=True)

    if exec_btn:
        try:
            with st.spinner("Computing..."):
                time.sleep(0.3)

            result = None
            res_label = "Result"

            if op == "Addition":
                result = A + B
            elif op == "Multiplication":
                result = np.matmul(A, B)
            elif op == "Transpose":
                result = A.T
            elif op == "Determinant":
                det_val = np.linalg.det(A)
                st.markdown(f"""
                <div class="metric-row" style="justify-content:center">
                    <div class="metric-box" style="max-width:280px">
                        <div class="metric-label">Determinant Value</div>
                        <div class="metric-value">{det_val:.6f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif op == "Inverse":
                result = np.linalg.inv(A)
            elif op == "Adjoint":
                result = np.round(np.linalg.inv(A) * np.linalg.det(A), 4)
            elif op == "Power of Matrix":
                result = np.linalg.matrix_power(A, int(power))
            elif op == "System of Equations (Ax = B)":
                result = np.linalg.solve(A, B)
                res_label = "Solution Vector X"

            if result is not None:
                st.markdown(f'<div style="height:12px"></div>', unsafe_allow_html=True)
                res_c1, res_c2, res_c3 = st.columns([1, 2, 1])
                with res_c2:
                    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="panel-heading">✓ {res_label}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(np.round(result, 6)), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        except np.linalg.LinAlgError as e:
            st.error(f"Mathematical Error: {e}")
        except ValueError as e:
            st.error(f"Dimension Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div style="text-align:center; padding:18px 0 10px 0;
    font-family:'Crimson Pro',serif; font-size:0.78rem;
    color:#8B7355; letter-spacing:0.12em; border-top:1px solid #D4B896; margin-top:20px;">
    ✦ &nbsp; NUMERICAL METHODS &nbsp;·&nbsp; BSCOMPE-2 &nbsp;·&nbsp; DIOSAMABEL B. PENASO &nbsp; ✦
</div>
""", unsafe_allow_html=True)
