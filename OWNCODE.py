import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time
import json
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Numerical Project", page_icon="📐", layout="wide", initial_sidebar_state="collapsed")

# --- VINTAGE BROWN THEME CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300&family=IM+Fell+English:ital@0;1&display=swap');

/* === ROOT VARIABLES === */
:root {
    --cream:      #f5ede0;
    --parchment:  #ede0cc;
    --sand:       #d9c4a7;
    --mocha:      #a07850;
    --coffee:     #7a5533;
    --espresso:   #4e3219;
    --dark-roast: #2d1a0a;
    --ink:        #1e1008;
    --gold:       #c9a84c;
    --gold-light: #e8d5a3;
    --shadow:     rgba(46, 26, 10, 0.18);
    --shadow-deep:rgba(46, 26, 10, 0.35);
}

/* === GLOBAL RESET === */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--espresso) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
    color: var(--cream) !important;
}

/* === PAPER TEXTURE BACKGROUND === */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}

/* === MAIN BLOCK === */
[data-testid="block-container"] {
    padding: 1rem 2rem 2rem 2rem !important;
    position: relative;
    z-index: 1;
}

/* === HIDE DEFAULT STREAMLIT ELEMENTS === */
#MainMenu, footer, [data-testid="stToolbar"], header { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* =========================================
   HEADER BANNER
   ========================================= */
.header-banner {
    background: linear-gradient(135deg, var(--espresso) 0%, var(--dark-roast) 50%, var(--espresso) 100%);
    border: 1px solid var(--gold);
    border-radius: 6px;
    padding: 18px 32px 14px 32px;
    margin-bottom: 6px;
    position: relative;
    box-shadow: 0 4px 24px var(--shadow-deep), inset 0 1px 0 rgba(201,168,76,0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-banner::before, .header-banner::after {
    content: '✦';
    color: var(--gold);
    font-size: 10px;
    position: absolute;
    top: 6px;
}
.header-banner::before { left: 10px; }
.header-banner::after  { right: 10px; }
.header-left {
    font-family: 'Crimson Pro', serif;
    font-size: 0.75rem;
    font-weight: 300;
    color: var(--gold-light);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    line-height: 1.5;
    opacity: 0.85;
}
.header-center {
    text-align: center;
    flex: 1;
}
.header-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    margin: 0;
    line-height: 1.1;
}
.header-subtitle {
    font-family: 'IM Fell English', Georgia, serif;
    font-style: italic;
    font-size: 0.78rem;
    color: var(--sand);
    letter-spacing: 0.15em;
    margin-top: 2px;
    opacity: 0.75;
}
.header-ornament {
    color: var(--gold);
    font-size: 1.2rem;
    opacity: 0.5;
    margin: 0 10px;
}

/* === GOLD DIVIDER === */
.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), var(--mocha), var(--gold), transparent);
    margin: 6px 0 18px 0;
    opacity: 0.6;
}
.gold-divider-thick {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, var(--gold) 20%, var(--gold-light) 50%, var(--gold) 80%, transparent);
    margin: 10px 0;
    opacity: 0.7;
}

/* =========================================
   MODULE TAB NAVIGATION
   ========================================= */
.module-nav {
    display: flex;
    gap: 0;
    background: var(--dark-roast);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 18px;
    box-shadow: 0 2px 12px var(--shadow);
}
.module-btn {
    flex: 1;
    padding: 10px 20px;
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    border: none;
    cursor: pointer;
    transition: all 0.25s ease;
    text-align: center;
}
.module-btn.active {
    background: linear-gradient(135deg, var(--coffee), var(--mocha));
    color: var(--gold-light);
    box-shadow: inset 0 -2px 0 var(--gold);
}
.module-btn.inactive {
    background: transparent;
    color: var(--sand);
}
.module-btn.inactive:hover {
    background: rgba(160,120,80,0.15);
    color: var(--gold-light);
}

/* =========================================
   PANEL / CARD
   ========================================= */
.vintage-panel {
    background: linear-gradient(160deg, rgba(78,50,25,0.92) 0%, rgba(46,26,10,0.95) 100%);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 8px;
    padding: 20px 22px;
    box-shadow: 0 4px 20px var(--shadow), inset 0 1px 0 rgba(201,168,76,0.12);
    backdrop-filter: blur(4px);
    margin-bottom: 14px;
}
.panel-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--gold);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(201,168,76,0.2);
}

/* =========================================
   INPUTS OVERRIDES
   ========================================= */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background-color: rgba(245,237,224,0.08) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    border-radius: 5px !important;
    color: var(--cream) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.95rem !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label,
.stCheckbox label {
    color: var(--sand) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
}

/* =========================================
   BUTTONS
   ========================================= */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--coffee) 0%, var(--mocha) 100%) !important;
    color: var(--gold-light) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    border-radius: 6px !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 10px 16px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 3px 12px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--mocha) 0%, var(--gold) 100%) !important;
    color: var(--dark-roast) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px var(--shadow-deep) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* =========================================
   METRICS
   ========================================= */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(122,85,51,0.35), rgba(78,50,25,0.5)) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 8px !important;
    padding: 14px 18px !important;
    box-shadow: 0 2px 10px var(--shadow) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--sand) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--gold) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.4rem !important;
}

/* =========================================
   DATAFRAME / TABLE
   ========================================= */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
.stDataFrame iframe { border-radius: 8px !important; }

/* =========================================
   EXPANDER
   ========================================= */
[data-testid="stExpander"] {
    background: rgba(46,26,10,0.6) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: var(--gold-light) !important;
    font-family: 'Crimson Pro', serif !important;
}

/* =========================================
   ALERTS / INFO / SUCCESS / ERROR
   ========================================= */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 3px !important;
    font-family: 'Crimson Pro', serif !important;
}
.stSuccess {
    background: rgba(60,90,40,0.3) !important;
    border-color: #7aad4a !important;
    color: #c5e8a0 !important;
}
.stError {
    background: rgba(120,40,30,0.3) !important;
    border-color: #c0504a !important;
    color: #f0c0b0 !important;
}
.stInfo {
    background: rgba(40,70,100,0.25) !important;
    border-color: var(--mocha) !important;
    color: var(--sand) !important;
}

/* =========================================
   SECTION LABELS
   ========================================= */
.section-label {
    font-family: 'Playfair Display', serif;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--gold);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::before, .section-label::after {
    content: '';
    flex: 0 0 20px;
    height: 1px;
    background: var(--gold);
    opacity: 0.4;
}

/* =========================================
   HISTORY SECTION
   ========================================= */
.history-card {
    background: rgba(46,26,10,0.7);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-family: 'Crimson Pro', serif;
    font-size: 0.88rem;
    color: var(--sand);
    transition: border-color 0.2s;
}
.history-card:hover { border-color: rgba(201,168,76,0.5); }
.history-card .h-method {
    font-family: 'Playfair Display', serif;
    color: var(--gold);
    font-size: 0.92rem;
    font-weight: 600;
    margin-bottom: 4px;
}
.history-card .h-answer {
    color: var(--cream);
    font-weight: 600;
}
.history-card .h-time {
    color: var(--mocha);
    font-size: 0.78rem;
    margin-top: 4px;
}

/* =========================================
   PLOTLY GRAPH CONTAINER
   ========================================= */
[data-testid="stPlotlyChart"] {
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 16px var(--shadow);
}

/* =========================================
   SPINNER
   ========================================= */
[data-testid="stSpinner"] {
    color: var(--gold) !important;
}

/* =========================================
   SUBHEADER / MARKDOWN OVERRIDES
   ========================================= */
h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--gold-light) !important;
}
p, li, .stMarkdown {
    font-family: 'Crimson Pro', serif !important;
    color: var(--sand) !important;
}

/* DATA EDITOR */
[data-testid="stDataEditor"] {
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 8px !important;
}

/* DIVIDER */
hr {
    border-color: rgba(201,168,76,0.2) !important;
}

/* TOAST override */
[data-testid="stToast"] {
    background: var(--espresso) !important;
    border: 1px solid var(--gold) !important;
    color: var(--gold-light) !important;
    font-family: 'Crimson Pro', serif !important;
}

/* NUMBER INPUT increment/decrement */
[data-testid="stNumberInput"] button {
    background: rgba(122,85,51,0.3) !important;
    color: var(--gold-light) !important;
    border-color: rgba(201,168,76,0.2) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--dark-roast); }
::-webkit-scrollbar-thumb { background: var(--coffee); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--mocha); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HISTORY HELPER (session state)
# ==========================================
if "calc_history" not in st.session_state:
    st.session_state.calc_history = []

def save_to_history(method, equation, inputs_dict, answer):
    entry = {
        "method": method,
        "equation": equation,
        "inputs": inputs_dict,
        "answer": answer,
        "datetime": datetime.now().strftime("%b %d, %Y  %I:%M %p")
    }
    st.session_state.calc_history.insert(0, entry)

# ==========================================
# HEADER BANNER
# ==========================================
st.markdown("""
<div class="header-banner">
    <div class="header-left">
        DIOSAMABEL B. PENASO<br>BSCOMPE-2
    </div>
    <div class="header-center">
        <div class="header-title">✦ Numerical Project ✦</div>
        <div class="header-subtitle">Advanced Mathematical Computing Studio</div>
    </div>
    <div class="header-left" style="text-align:right; opacity:0.5;">
        &nbsp;
    </div>
</div>
<div class="gold-divider-thick"></div>
""", unsafe_allow_html=True)

# ==========================================
# MODULE SELECTOR (top, radio styled)
# ==========================================
app_mode = st.radio(
    "Module",
    ["⚙ Root Finding Analysis", "⬛ Advanced Matrix Operations"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ==========================================
# MODULE 1: ROOT FINDING
# ==========================================
if app_mode == "⚙ Root Finding Analysis":

    left_col, right_col = st.columns([1, 1.8], gap="medium")

    # ---- LEFT: INPUTS ----
    with left_col:
        st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📐 Parameters</div>', unsafe_allow_html=True)

        eq_str = st.text_input("Equation  f(x)", value="x**3 - x - 2",
                               help="Use Python syntax: x**2, sp.sin(x), etc.")
        method = st.selectbox("Algorithm", [
            "Incremental Search", "Bisection Method",
            "Regula-Falsi", "Newton-Raphson", "Secant Method"
        ])

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            c1, c2 = st.columns(2)
            xl = c1.number_input("Lower Bound (xl)", value=1.0)
            xu = c2.number_input("Upper Bound (xu)", value=2.0)
        elif method == "Newton-Raphson":
            xl = xu = None
            x0 = st.number_input("Initial Guess (x0)", value=1.0)
        elif method == "Secant Method":
            xl = xu = None
            c1, c2 = st.columns(2)
            x0 = c1.number_input("First Guess (x0)", value=1.0)
            x1 = c2.number_input("Second Guess (x1)", value=2.0)

        c1, c2 = st.columns(2)
        tol      = c1.number_input("Tolerance",      value=0.0001, format="%.5f")
        max_iter = c2.number_input("Max Iterations", value=50, step=1)

        st.markdown("</div>", unsafe_allow_html=True)
        solve_btn = st.button("🔍  Calculate Root", key="root_solve")

        # --- HISTORY PANEL (left, below inputs) ---
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🕰 Calculation History</div>', unsafe_allow_html=True)

        h_col1, h_col2 = st.columns(2)
        view_hist  = h_col1.button("View History",  key="view_hist_root")
        clear_hist = h_col2.button("Clear History", key="clear_hist_root")

        if clear_hist:
            st.session_state.calc_history = []
            st.toast("History cleared.", icon="🗑")

        if view_hist or clear_hist:
            if st.session_state.calc_history:
                for entry in st.session_state.calc_history:
                    inputs_str = ", ".join([f"{k}: {v}" for k, v in entry["inputs"].items()])
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="h-method">▸ {entry['method']}</div>
                        <div>f(x) = {entry['equation']}</div>
                        <div>Inputs: {inputs_str}</div>
                        <div class="h-answer">Root ≈ {entry['answer']}</div>
                        <div class="h-time">🕐 {entry['datetime']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No history yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- RIGHT: RESULTS ----
    with right_col:
        if solve_btn:
            try:
                x = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f  = sp.lambdify(x, expr, 'numpy')
                df_sym = sp.lambdify(x, sp.diff(expr, x), 'numpy')

                results, root, iterations, final_err = [], None, 0, 0

                if method == "Bisection Method":
                    _xl, _xu = xl, xu
                    for i in range(int(max_iter)):
                        xr = (_xl + _xu) / 2
                        err = abs(_xu - _xl) / 2
                        results.append({"Iter": i+1, "xl": _xl, "xu": _xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if f(xr) == 0 or err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(_xl) * f(xr) < 0: _xu = xr
                        else: _xl = xr

                elif method == "Regula-Falsi":
                    _xl, _xu = xl, xu
                    for i in range(int(max_iter)):
                        xr = _xu - (f(_xu)*(_xl - _xu)) / (f(_xl) - f(_xu))
                        err = abs(f(xr))
                        results.append({"Iter": i+1, "xl": _xl, "xu": _xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(_xl) * f(xr) < 0: _xu = xr
                        else: _xl = xr

                elif method == "Newton-Raphson":
                    xr = x0
                    for i in range(int(max_iter)):
                        fxr, dfxr = f(xr), df_sym(xr)
                        xr_new = xr - fxr/dfxr
                        err = abs(xr_new - xr)
                        results.append({"Iter": i+1, "xi": xr, "f(xi)": fxr, "f'(xi)": dfxr, "xi+1": xr_new, "Error": err})
                        xr = xr_new
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break

                elif method == "Secant Method":
                    _x0, _x1 = x0, x1
                    for i in range(int(max_iter)):
                        fx1, fx0 = f(_x1), f(_x0)
                        x2 = _x1 - (fx1 * (_x0 - _x1)) / (fx0 - fx1)
                        err = abs(x2 - _x1)
                        results.append({"Iter": i+1, "x(i-1)": _x0, "x(i)": _x1, "x(i+1)": x2, "f(x(i+1))": f(x2), "Error": err})
                        _x0, _x1 = _x1, x2
                        if err < tol:
                            root, iterations, final_err = x2, i+1, err; break

                elif method == "Incremental Search":
                    step, curr_x = 0.1, xl
                    for i in range(int(max_iter)):
                        next_x = curr_x + step
                        results.append({"Iter": i+1, "x": curr_x, "f(x)": f(curr_x)})
                        if f(curr_x) * f(next_x) < 0:
                            root, iterations = (curr_x + next_x)/2, i+2; break
                        curr_x = next_x

                if root is not None:
                    # Save to history
                    if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
                        inp = {"xl": xl, "xu": xu, "tol": tol}
                    elif method == "Newton-Raphson":
                        inp = {"x0": x0, "tol": tol}
                    else:
                        inp = {"x0": x0, "x1": x1, "tol": tol}
                    save_to_history(method, eq_str, inp, f"{root:.6f}")

                    st.toast("Calculation Complete!", icon="✅")

                    # METRICS
                    st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
                    st.markdown('<div class="panel-title">📊 Results Summary</div>', unsafe_allow_html=True)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Calculated Root",  f"{root:.6f}")
                    m2.metric("Total Iterations", iterations)
                    m3.metric("Final Error",       f"{final_err:.6f}" if final_err else "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)

                    # ITERATION TABLE (directly visible)
                    st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
                    st.markdown('<div class="panel-title">📋 Iteration History</div>', unsafe_allow_html=True)
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df, use_container_width=True, height=220)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # GRAPH (directly below table)
                    st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
                    st.markdown('<div class="panel-title">📈 Function Graph</div>', unsafe_allow_html=True)
                    x_vals = np.linspace(root - 3, root + 3, 300)
                    y_vals = f(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#c9a84c', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="rgba(245,237,224,0.3)", line_width=1)
                    fig.add_vline(x=0, line_dash="dash", line_color="rgba(245,237,224,0.3)", line_width=1)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name='Root',
                        marker=dict(color='#e87070', size=13, symbol='x', line=dict(width=2.5, color='#e87070'))
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(46,26,10,0)',
                        plot_bgcolor='rgba(46,26,10,0.5)',
                        font=dict(family='Crimson Pro, serif', color='#d9c4a7'),
                        title=dict(text=f"f(x) = {eq_str}", font=dict(family='Playfair Display', color='#c9a84c', size=14)),
                        xaxis=dict(
                            title="X Axis",
                            gridcolor='rgba(160,120,80,0.15)',
                            linecolor='rgba(201,168,76,0.3)',
                            zerolinecolor='rgba(201,168,76,0.2)'
                        ),
                        yaxis=dict(
                            title="Y Axis",
                            gridcolor='rgba(160,120,80,0.15)',
                            linecolor='rgba(201,168,76,0.3)',
                            zerolinecolor='rgba(201,168,76,0.2)'
                        ),
                        legend=dict(bgcolor='rgba(46,26,10,0.6)', bordercolor='rgba(201,168,76,0.3)', borderwidth=1),
                        hovermode="x unified",
                        margin=dict(l=10, r=10, t=40, b=10),
                        height=340
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                else:
                    st.warning("Root not found within the given iterations/bounds. Try adjusting the parameters.")

            except Exception as e:
                st.error(f"Error: {e}. Ensure valid Python math syntax (e.g., ** for exponents).")

        else:
            st.markdown('<div class="vintage-panel" style="text-align:center; padding:50px 20px;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Playfair Display',serif; color:rgba(201,168,76,0.4); font-size:3rem;">📐</div>
            <div style="font-family:'IM Fell English',serif; font-style:italic; color:rgba(217,196,167,0.4); font-size:1.05rem; margin-top:10px;">
                Configure parameters and press<br><em>Calculate Root</em> to begin analysis
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODULE 2: MATRIX OPERATIONS
# ==========================================
elif app_mode == "⬛ Advanced Matrix Operations":

    left_col, right_col = st.columns([1, 1.4], gap="medium")

    # ---- LEFT: MATRIX INPUTS ----
    with left_col:
        st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⬛ Matrix Configuration</div>', unsafe_allow_html=True)

        op = st.selectbox("Select Operation", [
            "Addition", "Multiplication", "System of Equations (Ax = B)",
            "Adjoint", "Inverse", "Determinant", "Power of Matrix", "Transpose"
        ])
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Matrix A</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        rows_A = c1.number_input("Rows A", 1, 10, 3)
        cols_A = c2.number_input("Cols A", 1, 10, 3)
        df_A = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"C{i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A = edited_A.to_numpy()

        if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Matrix B</div>', unsafe_allow_html=True)
            if op == "System of Equations (Ax = B)":
                st.info("Matrix B must be a single column (results vector)")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:
                c1, c2 = st.columns(2)
                rows_B = c1.number_input("Rows B", 1, 10, int(cols_A), disabled=True)
                cols_B = c2.number_input("Cols B", 1, 10, 3)
            df_B = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B = edited_B.to_numpy()

        if op == "Power of Matrix":
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            power = st.number_input("Power (n)", value=2, step=1)

        st.markdown("</div>", unsafe_allow_html=True)
        mat_btn = st.button("▶  Execute Matrix Operation", key="mat_solve")

        # --- HISTORY PANEL ---
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🕰 Calculation History</div>', unsafe_allow_html=True)
        h1, h2 = st.columns(2)
        view_mhist  = h1.button("View History",  key="view_hist_mat")
        clear_mhist = h2.button("Clear History", key="clear_hist_mat")
        if clear_mhist:
            st.session_state.calc_history = []
            st.toast("History cleared.", icon="🗑")
        if view_mhist or clear_mhist:
            mat_entries = [e for e in st.session_state.calc_history if "Matrix" in e.get("method","") or e.get("equation","") == "—"]
            if mat_entries:
                for entry in mat_entries:
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="h-method">▸ {entry['method']}</div>
                        <div class="h-answer">Result: {entry['answer']}</div>
                        <div class="h-time">🕐 {entry['datetime']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No matrix history yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- RIGHT: RESULTS ----
    with right_col:
        if mat_btn:
            try:
                with st.spinner("Computing..."):
                    time.sleep(0.4)

                st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-title">📊 Operation Result</div>', unsafe_allow_html=True)

                result = None
                answer_str = ""

                if op == "Addition":
                    result = A + B
                elif op == "Multiplication":
                    result = np.matmul(A, B)
                elif op == "Transpose":
                    result = A.T
                elif op == "Determinant":
                    det_val = np.linalg.det(A)
                    st.metric("Determinant Value", f"{det_val:.4f}")
                    answer_str = f"det = {det_val:.4f}"
                    result = None
                elif op == "Inverse":
                    result = np.linalg.inv(A)
                elif op == "Adjoint":
                    result = np.round(np.linalg.inv(A) * np.linalg.det(A), 4)
                elif op == "Power of Matrix":
                    result = np.linalg.matrix_power(A, int(power))
                elif op == "System of Equations (Ax = B)":
                    result = np.linalg.solve(A, B)
                    st.success("Solutions found for Vector X:")

                if result is not None:
                    answer_str = f"{op} computed successfully"
                    st.dataframe(pd.DataFrame(result), use_container_width=True)
                    st.toast("Operation Successful!", icon="✅")

                st.markdown("</div>", unsafe_allow_html=True)

                # Save to history
                save_to_history(f"Matrix: {op}", "—", {"Operation": op}, answer_str)

                # Visual: show matrix A heatmap
                st.markdown('<div class="vintage-panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-title">🔍 Matrix A Heatmap</div>', unsafe_allow_html=True)
                fig_heat = go.Figure(data=go.Heatmap(
                    z=A,
                    colorscale=[[0, '#2d1a0a'], [0.5, '#7a5533'], [1, '#c9a84c']],
                    showscale=True,
                    text=np.round(A, 3),
                    texttemplate="%{text}",
                    hovertemplate="Row %{y}, Col %{x}: %{z}<extra></extra>"
                ))
                fig_heat.update_layout(
                    paper_bgcolor='rgba(46,26,10,0)',
                    plot_bgcolor='rgba(46,26,10,0)',
                    font=dict(family='Crimson Pro, serif', color='#d9c4a7'),
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=280
                )
                st.plotly_chart(fig_heat, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            except np.linalg.LinAlgError as e:
                st.error(f"Mathematical Error: {e}")
            except ValueError as e:
                st.error(f"Dimension Error: {e}")

        else:
            st.markdown('<div class="vintage-panel" style="text-align:center; padding:60px 20px;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Playfair Display',serif; color:rgba(201,168,76,0.4); font-size:3rem;">⬛</div>
            <div style="font-family:'IM Fell English',serif; font-style:italic; color:rgba(217,196,167,0.4); font-size:1.05rem; margin-top:10px;">
                Input matrices on the left and press<br><em>Execute Matrix Operation</em> to proceed
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:6px 0 2px 0;">
    <span style="font-family:'IM Fell English',serif; font-style:italic;
                 color:rgba(201,168,76,0.4); font-size:0.78rem; letter-spacing:0.12em;">
        ✦ &nbsp; MathStudio Pro &nbsp;·&nbsp; Numerical Methods &amp; Matrix Analysis &nbsp;·&nbsp;
        DIOSAMABEL B. PENASO, BSCOMPE-2 &nbsp; ✦
    </span>
</div>
""", unsafe_allow_html=True)
