import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time
import json
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Numerical Project", page_icon="📜", layout="wide", initial_sidebar_state="collapsed")

# --- VINTAGE BROWN THEME CSS ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">

<style>
/* ── ROOT TOKENS ─────────────────────────────────────────────── */
:root {
  --cream:      #f5ede0;
  --parchment:  #ede0c8;
  --warm-beige: #d9c9a8;
  --mocha:      #8b6543;
  --coffee:     #6b4c2a;
  --espresso:   #3e2a14;
  --caramel:    #b8813a;
  --brown-mid:  #a0714f;
  --ink:        #2c1a0e;
  --muted:      #7a5c3e;
  --gold:       #c9943a;
  --shadow:     rgba(62, 42, 20, 0.18);
  --panel-bg:   rgba(237, 224, 200, 0.55);
  --glass:      rgba(245, 237, 224, 0.45);
}

/* ── GLOBAL RESET ────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'Crimson Text', Georgia, serif;
  color: var(--ink);
}

.stApp {
  background:
    radial-gradient(ellipse at 15% 20%, rgba(185,135,80,0.12) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 75%, rgba(107,76,42,0.10) 0%, transparent 55%),
    linear-gradient(160deg, #f0e6d0 0%, #e8d9be 40%, #ddc9a5 100%);
  min-height: 100vh;
}

/* Subtle paper texture overlay */
.stApp::before {
  content: "";
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}

/* ── HEADER SECTION ──────────────────────────────────────────── */
.site-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px 28px 10px;
  margin-bottom: 4px;
}
.header-left {
  position: absolute;
  left: 28px;
  font-family: 'EB Garamond', serif;
  font-size: 0.78rem;
  color: var(--muted);
  letter-spacing: 0.04em;
  line-height: 1.55;
}
.header-left strong {
  display: block;
  font-family: 'Playfair Display', serif;
  font-size: 0.88rem;
  color: var(--coffee);
  font-weight: 600;
  letter-spacing: 0.02em;
}
.header-center {
  text-align: center;
}
.header-center .main-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.05rem;
  font-weight: 700;
  color: var(--espresso);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  line-height: 1.2;
  text-shadow: 1px 2px 6px rgba(62,42,20,0.15);
}
.header-center .sub-title {
  font-family: 'Crimson Text', serif;
  font-style: italic;
  font-size: 0.95rem;
  color: var(--mocha);
  letter-spacing: 0.12em;
  margin-top: 2px;
}
.vintage-divider {
  text-align: center;
  margin: 4px 0 18px;
  color: var(--caramel);
  font-size: 1.1rem;
  letter-spacing: 0.3em;
  opacity: 0.7;
}
.vintage-divider::before,
.vintage-divider::after {
  content: "────────────────";
  font-size: 0.6rem;
  vertical-align: middle;
  opacity: 0.5;
}

/* ── MODULE SELECTOR BAR ─────────────────────────────────────── */
.module-bar {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-bottom: 20px;
}

/* ── PANELS / CARDS ──────────────────────────────────────────── */
.panel {
  background: var(--panel-bg);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(185,135,80,0.35);
  border-radius: 12px;
  padding: 20px 20px 16px;
  box-shadow: 0 4px 20px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.4);
  margin-bottom: 16px;
}
.panel-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--coffee);
  letter-spacing: 0.04em;
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(185,135,80,0.3);
  padding-bottom: 6px;
}

/* ── METRIC CARDS ────────────────────────────────────────────── */
div[data-testid="metric-container"] {
  background: linear-gradient(135deg, rgba(245,237,224,0.8), rgba(217,201,168,0.6)) !important;
  border: 1px solid rgba(185,135,80,0.4) !important;
  border-radius: 10px !important;
  padding: 12px 16px !important;
  box-shadow: 0 2px 10px var(--shadow) !important;
}
div[data-testid="metric-container"] label {
  font-family: 'EB Garamond', serif !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.08em !important;
  color: var(--muted) !important;
  text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: 'Playfair Display', serif !important;
  font-size: 1.4rem !important;
  color: var(--espresso) !important;
  font-weight: 700 !important;
}

/* ── INPUTS ──────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
  background: rgba(245, 237, 224, 0.75) !important;
  border: 1px solid rgba(139, 101, 67, 0.4) !important;
  border-radius: 8px !important;
  color: var(--ink) !important;
  font-family: 'Crimson Text', serif !important;
  font-size: 1rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--caramel) !important;
  box-shadow: 0 0 0 2px rgba(201,148,58,0.2) !important;
}
label[data-testid="stWidgetLabel"] {
  font-family: 'EB Garamond', serif !important;
  font-size: 0.88rem !important;
  color: var(--coffee) !important;
  letter-spacing: 0.03em !important;
  font-weight: 600 !important;
}

/* ── BUTTONS ─────────────────────────────────────────────────── */
.stButton > button {
  width: 100%;
  font-family: 'Playfair Display', serif !important;
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.08em !important;
  background: linear-gradient(135deg, var(--mocha), var(--coffee)) !important;
  color: var(--cream) !important;
  border: 1px solid var(--caramel) !important;
  border-radius: 8px !important;
  padding: 10px 20px !important;
  box-shadow: 0 3px 12px rgba(62,42,20,0.25) !important;
  transition: all 0.28s ease !important;
  text-transform: uppercase !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, var(--coffee), var(--espresso)) !important;
  box-shadow: 0 5px 18px rgba(62,42,20,0.35) !important;
  transform: translateY(-1px) scale(1.01) !important;
}
.stButton > button:active {
  transform: translateY(0) scale(0.99) !important;
}

/* ── DATAFRAME / TABLE ───────────────────────────────────────── */
.stDataFrame {
  border: 1px solid rgba(185,135,80,0.35) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}
.stDataFrame thead tr th {
  background: var(--coffee) !important;
  color: var(--cream) !important;
  font-family: 'EB Garamond', serif !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 8px 12px !important;
}
.stDataFrame tbody tr:nth-child(even) td {
  background: rgba(217,201,168,0.35) !important;
}
.stDataFrame tbody tr:nth-child(odd) td {
  background: rgba(245,237,224,0.5) !important;
}
.stDataFrame tbody tr:hover td {
  background: rgba(185,135,80,0.2) !important;
}
.stDataFrame td {
  font-family: 'Crimson Text', serif !important;
  font-size: 0.93rem !important;
  color: var(--ink) !important;
  padding: 6px 12px !important;
}

/* ── PLOTLY GRAPH CONTAINER ──────────────────────────────────── */
.stPlotlyChart {
  border: 1px solid rgba(185,135,80,0.4) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
  box-shadow: 0 4px 16px var(--shadow) !important;
}

/* ── ALERTS & INFO BOXES ─────────────────────────────────────── */
.stSuccess {
  background: rgba(185,135,80,0.15) !important;
  border-color: var(--caramel) !important;
  color: var(--espresso) !important;
  border-radius: 8px !important;
}
.stError {
  border-radius: 8px !important;
}
.stInfo {
  background: rgba(217,201,168,0.4) !important;
  border-color: var(--mocha) !important;
  border-radius: 8px !important;
}

/* ── SELECT BOX ──────────────────────────────────────────────── */
.stSelectbox [data-baseweb="select"] > div {
  background: rgba(245, 237, 224, 0.75) !important;
  border-color: rgba(139, 101, 67, 0.4) !important;
  border-radius: 8px !important;
}

/* ── SIDEBAR ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #3e2a14 0%, #5a3a1a 100%) !important;
  border-right: 2px solid var(--caramel) !important;
}
section[data-testid="stSidebar"] * {
  color: var(--cream) !important;
}

/* ── SPINNER ─────────────────────────────────────────────────── */
.stSpinner > div {
  border-top-color: var(--caramel) !important;
}

/* ── EXPANDER ────────────────────────────────────────────────── */
.stExpander {
  background: var(--glass) !important;
  border: 1px solid rgba(185,135,80,0.3) !important;
  border-radius: 10px !important;
}
.stExpander summary {
  font-family: 'EB Garamond', serif !important;
  font-weight: 600 !important;
  color: var(--coffee) !important;
  letter-spacing: 0.04em !important;
}

/* ── DATA EDITOR ─────────────────────────────────────────────── */
.stDataEditor {
  border: 1px solid rgba(185,135,80,0.35) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}

/* ── HIDE STREAMLIT BRANDING ─────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── SECTION BADGE ───────────────────────────────────────────── */
.section-badge {
  display: inline-block;
  font-family: 'EB Garamond', serif;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--cream);
  background: var(--coffee);
  border-radius: 4px;
  padding: 2px 10px;
  margin-bottom: 8px;
}

/* ── HISTORY ENTRY ───────────────────────────────────────────── */
.history-entry {
  background: rgba(245,237,224,0.6);
  border: 1px solid rgba(185,135,80,0.3);
  border-left: 3px solid var(--caramel);
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 10px;
  font-family: 'Crimson Text', serif;
  font-size: 0.93rem;
  color: var(--ink);
}
.history-entry .h-method {
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  color: var(--coffee);
  font-size: 0.97rem;
}
.history-entry .h-meta {
  font-size: 0.78rem;
  color: var(--muted);
  font-style: italic;
  margin-top: 2px;
}
.history-entry .h-answer {
  color: var(--espresso);
  font-weight: 600;
  margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── HISTORY HELPERS ───────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

def save_to_history(method, equation, inputs_dict, answer, module="Root Finding"):
    entry = {
        "module":   module,
        "method":   method,
        "equation": equation,
        "inputs":   inputs_dict,
        "answer":   answer,
        "datetime": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
    }
    st.session_state.history.insert(0, entry)  # newest first

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
  <div class="header-left">
    <strong>DIOSAMABEL B. PENASO</strong>
    BSCOMPE-2
  </div>
  <div class="header-center">
    <div class="main-title">Numerical Project</div>
    <div class="sub-title">Mathematical Analysis Dashboard</div>
  </div>
</div>
<div class="vintage-divider">✦ &nbsp;&nbsp; ✦ &nbsp;&nbsp; ✦</div>
""", unsafe_allow_html=True)

# ── MODULE SELECTOR ───────────────────────────────────────────────────────────
app_mode = st.radio(
    "Select Module",
    ["Root Finding Analysis", "Advanced Matrix Operations", "📜 Calculation History"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<hr style='border:none;border-top:1px solid rgba(185,135,80,0.35);margin:4px 0 20px;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — ROOT FINDING
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":

    col_input, col_results = st.columns([1, 2.4])

    # ── LEFT — INPUTS ─────────────────────────────────────────────────────────
    with col_input:
        st.markdown('<div class="section-badge">Parameters</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        eq_str = st.text_input("Equation f(x)", value="x**3 - x - 2")
        method = st.selectbox("Algorithm", [
            "Incremental Search", "Bisection Method",
            "Regula-Falsi", "Newton-Raphson", "Secant Method"
        ])

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            xl = st.number_input("Lower Bound (xl)", value=1.0)
            xu = st.number_input("Upper Bound (xu)", value=2.0)
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess (x0)", value=1.0)
        elif method == "Secant Method":
            x0 = st.number_input("First Guess (x0)", value=1.0)
            x1 = st.number_input("Second Guess (x1)", value=2.0)

        tol      = st.number_input("Tolerance",      value=0.0001, format="%.5f")
        max_iter = st.number_input("Max Iterations", value=50, step=1)

        st.markdown("</div>", unsafe_allow_html=True)
        solve_btn = st.button("⚙ Calculate Root")

    # ── RIGHT — RESULTS ───────────────────────────────────────────────────────
    with col_results:
        if solve_btn:
            try:
                x    = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f    = sp.lambdify(x, expr, 'numpy')
                df   = sp.lambdify(x, sp.diff(expr, x), 'numpy')

                results, root, iterations, final_err = [], None, 0, 0

                # ── ALGORITHMS (unchanged) ────────────────────────────────────
                if method == "Bisection Method":
                    for i in range(max_iter):
                        xr  = (xl + xu) / 2
                        err = abs(xu - xl) / 2
                        results.append({"Iter": i+1, "xl": xl, "xu": xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if f(xr) == 0 or err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(xl) * f(xr) < 0: xu = xr
                        else: xl = xr

                elif method == "Regula-Falsi":
                    for i in range(max_iter):
                        xr  = xu - (f(xu)*(xl - xu)) / (f(xl) - f(xu))
                        err = abs(f(xr))
                        results.append({"Iter": i+1, "xl": xl, "xu": xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(xl) * f(xr) < 0: xu = xr
                        else: xl = xr

                elif method == "Newton-Raphson":
                    xr = x0
                    for i in range(max_iter):
                        fxr, dfxr = f(xr), df(xr)
                        xr_new    = xr - fxr/dfxr
                        err       = abs(xr_new - xr)
                        results.append({"Iter": i+1, "xi": xr, "f(xi)": fxr, "f'(xi)": dfxr, "xi+1": xr_new, "Error": err})
                        xr = xr_new
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break

                elif method == "Secant Method":
                    for i in range(max_iter):
                        fx1, fx0 = f(x1), f(x0)
                        x2       = x1 - (fx1 * (x0 - x1)) / (fx0 - fx1)
                        err      = abs(x2 - x1)
                        results.append({"Iter": i+1, "x(i-1)": x0, "x(i)": x1, "x(i+1)": x2, "f(x(i+1))": f(x2), "Error": err})
                        x0, x1 = x1, x2
                        if err < tol:
                            root, iterations, final_err = x2, i+1, err; break

                elif method == "Incremental Search":
                    step, curr_x = 0.1, xl
                    for i in range(max_iter):
                        next_x = curr_x + step
                        results.append({"Iter": i+1, "x": curr_x, "f(x)": f(curr_x)})
                        if f(curr_x) * f(next_x) < 0:
                            root, iterations = (curr_x + next_x)/2, i+2; break
                        curr_x = next_x

                # ── OUTPUT ────────────────────────────────────────────────────
                if root is not None:
                    st.toast('Calculation Complete!', icon='✅')

                    # Save to history
                    inputs_info = {}
                    if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
                        inputs_info = {"xl": xl, "xu": xu, "tol": tol}
                    elif method == "Newton-Raphson":
                        inputs_info = {"x0": x0, "tol": tol}
                    elif method == "Secant Method":
                        inputs_info = {"x0": x0, "x1": x1, "tol": tol}
                    save_to_history(method, eq_str, inputs_info, f"{root:.6f}")

                    # Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Calculated Root", f"{root:.6f}")
                    m2.metric("Total Iterations", iterations)
                    m3.metric("Final Error", f"{final_err:.6f}" if final_err else "N/A")

                    st.markdown("<div style='margin:10px 0;'>", unsafe_allow_html=True)

                    # ── Iteration Table (top-right, always visible) ───────────
                    st.markdown('<div class="section-badge">Iteration History</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(results), use_container_width=True, height=260)

                    st.markdown("<div style='margin:12px 0;'>", unsafe_allow_html=True)

                    # ── Graph (below table) ───────────────────────────────────
                    st.markdown('<div class="section-badge">Function Graph</div>', unsafe_allow_html=True)
                    x_vals = np.linspace(root - 3, root + 3, 300)
                    y_vals = f(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#8b6543', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="#3e2a14", line_width=1)
                    fig.add_vline(x=0, line_dash="dash", line_color="#3e2a14", line_width=1)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name='Root',
                        marker=dict(color='#c9943a', size=13, symbol='x',
                                    line=dict(width=2.5, color='#3e2a14'))
                    ))
                    fig.update_layout(
                        title=dict(text="Function Graph", font=dict(family="Playfair Display, serif", size=15, color="#3e2a14")),
                        paper_bgcolor='rgba(245,237,224,0.6)',
                        plot_bgcolor='rgba(237,224,200,0.4)',
                        font=dict(family="Crimson Text, serif", color="#2c1a0e"),
                        xaxis=dict(title="X Axis", gridcolor='rgba(185,135,80,0.2)', zerolinecolor='rgba(62,42,20,0.4)'),
                        yaxis=dict(title="Y Axis", gridcolor='rgba(185,135,80,0.2)', zerolinecolor='rgba(62,42,20,0.4)'),
                        hovermode="x unified",
                        margin=dict(l=10, r=10, t=40, b=10),
                        legend=dict(bgcolor='rgba(245,237,224,0.7)', bordercolor='rgba(185,135,80,0.4)', borderwidth=1)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error evaluating equation: Make sure it is valid Python math (e.g., use ** for exponents). Details: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — MATRIX OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    st.markdown('<div class="section-badge">Select Operation</div>', unsafe_allow_html=True)
    op = st.selectbox("Select Operation", [
        "Addition", "Multiplication", "System of Equations (Ax = B)",
        "Adjoint", "Inverse", "Determinant", "Power of Matrix", "Transpose"
    ], label_visibility="collapsed")

    st.markdown("<hr style='border:none;border-top:1px solid rgba(185,135,80,0.25);margin:8px 0 16px;'>", unsafe_allow_html=True)

    if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
        col1, col2 = st.columns(2)
    else:
        col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-badge">Matrix A</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        rows_A = c1.number_input("Rows A", 1, 10, 3)
        cols_A = c2.number_input("Cols A", 1, 10, 3)

        df_A     = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"Col {i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A        = edited_A.to_numpy()

    if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
        with col2:
            st.markdown('<div class="section-badge">Matrix B</div>', unsafe_allow_html=True)
            if op == "System of Equations (Ax = B)":
                st.info("Matrix B must be a single column (Results vector)")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:
                c1, c2 = st.columns(2)
                rows_B = c1.number_input("Rows B", 1, 10, cols_A, disabled=True)
                cols_B = c2.number_input("Cols B", 1, 10, 3)

            df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"Col {i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B        = edited_B.to_numpy()

    if op == "Power of Matrix":
        with col2:
            st.markdown('<div class="section-badge">Settings</div>', unsafe_allow_html=True)
            power = st.number_input("Calculate to the power of (n):", value=2, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    exec_btn = st.button("⚙ Execute Matrix Operation", use_container_width=True)

    if exec_btn:
        try:
            with st.spinner("Calculating…"):
                time.sleep(0.5)

            st.markdown('<div class="section-badge">Result</div>', unsafe_allow_html=True)

            if op == "Addition":
                result = A + B
            elif op == "Multiplication":
                result = np.matmul(A, B)
            elif op == "Transpose":
                result = A.T
            elif op == "Determinant":
                result = np.linalg.det(A)
                st.metric("Determinant Value", f"{result:.4f}")
                save_to_history(op, f"Matrix {rows_A}×{cols_A}", {"matrix": "A"}, f"det = {result:.4f}", module="Matrix")
                result = None
            elif op == "Inverse":
                result = np.linalg.inv(A)
            elif op == "Adjoint":
                result = np.round(np.linalg.inv(A) * np.linalg.det(A), 4)
            elif op == "Power of Matrix":
                result = np.linalg.matrix_power(A, power)
            elif op == "System of Equations (Ax = B)":
                result = np.linalg.solve(A, B)
                st.success("Solutions found for Vector X:")

            if result is not None:
                st.dataframe(pd.DataFrame(result), use_container_width=True)
                st.toast('Operation Successful!', icon='✅')
                save_to_history(op, f"Matrix {rows_A}×{cols_A}", {"operation": op}, "See result table", module="Matrix")

        except np.linalg.LinAlgError as e:
            st.error(f"Mathematical Error: {e} (e.g., Matrix might be singular/non-invertible)")
        except ValueError as e:
            st.error(f"Dimension Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — CALCULATION HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "📜 Calculation History":
    st.markdown("""
    <div style="font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:700;
                color:#3e2a14; letter-spacing:0.05em; margin-bottom:4px;">
      Calculation History
    </div>
    <p style="font-family:'Crimson Text',serif;font-style:italic;color:#7a5c3e;font-size:0.95rem;margin-bottom:18px;">
      A chronological record of all computations performed this session.
    </p>
    """, unsafe_allow_html=True)

    h_col1, h_col2, h_col3 = st.columns([1, 1, 3])
    with h_col1:
        if st.button("🗑  Clear History"):
            st.session_state.history = []
            st.success("History cleared.")
    with h_col2:
        if st.button("💾  Export as CSV"):
            if st.session_state.history:
                hist_df = pd.DataFrame(st.session_state.history)
                csv     = hist_df.to_csv(index=False)
                st.download_button(
                    label="⬇ Download CSV",
                    data=csv,
                    file_name=f"calculation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No history to export yet.")

    st.markdown("<hr style='border:none;border-top:1px solid rgba(185,135,80,0.3);margin:12px 0 20px;'>", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center;padding:50px 20px;color:#7a5c3e;
                    font-family:'Crimson Text',serif;font-style:italic;font-size:1.1rem;">
          No calculations have been recorded yet.<br>
          <span style="font-size:0.88rem;opacity:0.7;">
            Solve an equation or perform a matrix operation to begin.
          </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, entry in enumerate(st.session_state.history):
            inputs_str = ", ".join(f"{k}: {v}" for k, v in entry.get("inputs", {}).items())
            st.markdown(f"""
            <div class="history-entry">
              <div class="h-method">#{len(st.session_state.history)-i} &nbsp;·&nbsp; {entry['method']}</div>
              <div class="h-meta">{entry['datetime']} &nbsp;·&nbsp; {entry['module']}</div>
              <div style="margin-top:5px;">
                <span style="color:#6b4c2a;font-weight:600;">f(x):</span> {entry['equation']}
              </div>
              <div style="font-size:0.85rem;color:#7a5c3e;margin-top:2px;">{inputs_str}</div>
              <div class="h-answer">Answer: {entry['answer']}</div>
            </div>
            """, unsafe_allow_html=True)
