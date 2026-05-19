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
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Vintage Brown Academic Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Lato:wght@300;400;700&display=swap');

/* ── Root palette ── */
:root {
    --cream:        #F5F0E8;
    --parchment:    #EDE5D0;
    --warm-beige:   #D9C9A8;
    --tan:          #C4A882;
    --coffee:       #7B5C3E;
    --espresso:     #4A3728;
    --dark-wood:    #2C1F14;
    --ink:          #1A1208;
    --accent-gold:  #C9A84C;
    --accent-rust:  #8B4A2A;
    --white-smoke:  #FAF7F2;
    --shadow:       rgba(44,31,20,0.18);
    --shadow-deep:  rgba(44,31,20,0.32);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'EB Garamond', Georgia, serif;
    background-color: var(--parchment) !important;
    color: var(--ink) !important;
}

/* ── Paper texture overlay ── */
.stApp {
    background-color: var(--parchment) !important;
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── Masthead ── */
.masthead {
    background: linear-gradient(135deg, var(--dark-wood) 0%, var(--espresso) 60%, var(--coffee) 100%);
    padding: 18px 40px 14px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid var(--accent-gold);
    box-shadow: 0 4px 20px var(--shadow-deep);
    margin-bottom: 0;
}
.masthead-left {
    font-family: 'Lato', sans-serif;
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--warm-beige);
    letter-spacing: 0.08em;
    line-height: 1.6;
}
.masthead-left span {
    display: block;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--cream);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.masthead-center {
    text-align: center;
    flex: 1;
}
.masthead-center h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.95rem;
    font-weight: 700;
    color: var(--cream);
    margin: 0;
    letter-spacing: 0.06em;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.masthead-center .subtitle {
    font-family: 'EB Garamond', serif;
    font-style: italic;
    font-size: 0.88rem;
    color: var(--accent-gold);
    letter-spacing: 0.1em;
    margin-top: 2px;
}
.masthead-ornament {
    color: var(--accent-gold);
    font-size: 1.5rem;
    opacity: 0.7;
}

/* ── Decorative rule ── */
.ornamental-rule {
    text-align: center;
    color: var(--accent-gold);
    font-size: 1.1rem;
    letter-spacing: 0.3em;
    margin: 0;
    padding: 7px 0 4px 0;
    background: var(--espresso);
    border-bottom: 1px solid var(--coffee);
}

/* ── Tab navigation ── */
.tab-bar {
    display: flex;
    gap: 0;
    background: var(--espresso);
    padding: 0 40px;
    border-bottom: 2px solid var(--accent-gold);
}
.tab-item {
    padding: 11px 28px;
    cursor: pointer;
    font-family: 'Lato', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--warm-beige);
    border-bottom: 3px solid transparent;
    transition: all 0.2s ease;
    user-select: none;
}
.tab-item:hover { color: var(--accent-gold); border-bottom-color: var(--coffee); }
.tab-item.active { color: var(--accent-gold); border-bottom-color: var(--accent-gold); background: rgba(201,168,76,0.08); }

/* ── Streamlit radio as tab strip ── */
div[data-testid="stHorizontalBlock"] .stRadio > label { display: none; }
.stRadio [data-testid="stWidgetLabel"] { display: none !important; }
.stRadio > div > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 0 !important;
    background: var(--espresso);
    padding: 0 20px;
    border-bottom: 2px solid var(--accent-gold);
}
.stRadio label {
    padding: 11px 26px !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--warm-beige) !important;
    border-radius: 0 !important;
    border-bottom: 3px solid transparent !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stRadio label:hover { color: var(--accent-gold) !important; }
.stRadio label[data-checked="true"],
.stRadio input:checked + label,
.stRadio div[aria-checked="true"] > label { color: var(--accent-gold) !important; border-bottom-color: var(--accent-gold) !important; }

/* ── Section card ── */
.vintage-card {
    background: var(--white-smoke);
    border: 1px solid var(--warm-beige);
    border-radius: 4px;
    padding: 22px 22px 18px 22px;
    box-shadow: 3px 3px 14px var(--shadow), inset 0 0 0 1px rgba(255,255,255,0.6);
    margin-bottom: 16px;
    position: relative;
}
.vintage-card::before {
    content: '';
    position: absolute;
    top: 6px; left: 6px; right: 6px; bottom: 6px;
    border: 1px solid var(--warm-beige);
    border-radius: 2px;
    pointer-events: none;
    opacity: 0.4;
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.0rem;
    font-weight: 600;
    color: var(--espresso);
    letter-spacing: 0.04em;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--warm-beige);
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-title .icon { font-size: 1.1rem; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: var(--cream) !important;
    border: 1px solid var(--tan) !important;
    border-radius: 3px !important;
    color: var(--ink) !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1rem !important;
    box-shadow: inset 1px 1px 4px rgba(0,0,0,0.06) !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--coffee) !important;
    box-shadow: inset 1px 1px 4px rgba(0,0,0,0.06), 0 0 0 2px rgba(123,92,62,0.15) !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: var(--coffee) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(160deg, var(--coffee) 0%, var(--espresso) 100%) !important;
    color: var(--cream) !important;
    border: 1px solid var(--accent-gold) !important;
    border-radius: 3px !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    box-shadow: 2px 3px 10px var(--shadow) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(160deg, var(--accent-rust) 0%, var(--espresso) 100%) !important;
    box-shadow: 2px 4px 16px var(--shadow-deep) !important;
    transform: translateY(-1px) !important;
    border-color: var(--accent-gold) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: var(--white-smoke) !important;
    border: 1px solid var(--warm-beige) !important;
    border-top: 3px solid var(--coffee) !important;
    border-radius: 3px !important;
    padding: 14px 16px !important;
    box-shadow: 2px 3px 10px var(--shadow) !important;
}
div[data-testid="metric-container"] label {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--coffee) !important;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.5rem !important;
    color: var(--espresso) !important;
}

/* ── DataFrames / tables ── */
.stDataFrame {
    border: 1px solid var(--tan) !important;
    border-radius: 3px !important;
    overflow: hidden !important;
}
.stDataFrame table { border-collapse: collapse !important; width: 100% !important; }
.stDataFrame thead th {
    background: var(--espresso) !important;
    color: var(--cream) !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    padding: 8px 10px !important;
    border-bottom: 2px solid var(--accent-gold) !important;
}
.stDataFrame tbody tr:nth-child(even) td { background: var(--parchment) !important; }
.stDataFrame tbody tr:nth-child(odd) td { background: var(--white-smoke) !important; }
.stDataFrame tbody td {
    font-family: 'EB Garamond', serif !important;
    font-size: 0.9rem !important;
    color: var(--ink) !important;
    padding: 6px 10px !important;
    border-bottom: 1px solid var(--warm-beige) !important;
}
.stDataFrame tbody tr:hover td { background: #e8dcc6 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--parchment) !important;
    border: 1px solid var(--tan) !important;
    border-radius: 3px !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: var(--coffee) !important;
}
.streamlit-expanderContent {
    border: 1px solid var(--warm-beige) !important;
    border-top: none !important;
    background: var(--white-smoke) !important;
}

/* ── Alert / info boxes ── */
.stAlert {
    border-radius: 3px !important;
    border-left: 4px solid var(--coffee) !important;
    background: var(--cream) !important;
    font-family: 'EB Garamond', serif !important;
}

/* ── Divider ── */
hr { border-color: var(--warm-beige) !important; }

/* ── History panel ── */
.history-item {
    background: var(--white-smoke);
    border: 1px solid var(--warm-beige);
    border-left: 4px solid var(--coffee);
    border-radius: 3px;
    padding: 12px 14px;
    margin-bottom: 8px;
    font-family: 'EB Garamond', serif;
    font-size: 0.95rem;
    transition: box-shadow 0.2s;
}
.history-item:hover { box-shadow: 2px 3px 10px var(--shadow); }
.history-meta {
    font-family: 'Lato', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--coffee);
    margin-bottom: 4px;
}
.history-answer {
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    color: var(--espresso);
    font-size: 1.05rem;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Lato', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--coffee);
    margin-bottom: 4px;
    opacity: 0.8;
}

/* ── Number input spinners ── */
.stNumberInput button {
    background: var(--parchment) !important;
    border-color: var(--tan) !important;
    color: var(--coffee) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: var(--parchment); }
::-webkit-scrollbar-thumb { background: var(--tan); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--coffee); }

/* ── Data editor ── */
.stDataEditor thead th {
    background: var(--espresso) !important;
    color: var(--cream) !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── Selectbox dropdown ── */
.stSelectbox [data-baseweb="select"] > div:first-child {
    background: var(--cream) !important;
    border-color: var(--tan) !important;
}

/* ── Toast ── */
.stToast { background: var(--espresso) !important; color: var(--cream) !important; border-left: 4px solid var(--accent-gold) !important; }

/* ── Module title ── */
.module-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--espresso);
    letter-spacing: 0.02em;
    margin: 0 0 2px 0;
}
.module-sub {
    font-family: 'EB Garamond', serif;
    font-style: italic;
    font-size: 1.0rem;
    color: var(--coffee);
    margin-bottom: 16px;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--coffee) !important; }

/* full-width padding */
.main-container { padding: 20px 32px 32px 32px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
#  MASTHEAD
# ─────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div class="masthead-left">
    <span>Diosamabel B. Penaso</span>
    BSCOMPE-2
  </div>
  <div class="masthead-center">
    <h1>✦ Numerical Project ✦</h1>
    <div class="subtitle">Root Finding Analysis &amp; Matrix Operations</div>
  </div>
  <div class="masthead-ornament">⚙</div>
</div>
<div class="ornamental-rule">· · · ✦ · · ·</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TOP NAV (radio styled as tabs)
# ─────────────────────────────────────────────
with st.container():
    app_mode = st.radio(
        "Module",
        ["Root Finding Methods", "Matrix Operations", "Calculation History"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  MODULE 1 — ROOT FINDING
# ══════════════════════════════════════════════
if app_mode == "Root Finding Methods":
    st.markdown('<div class="module-header">Root Finding Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-sub">Locate equation roots via classical numerical methods with iterative refinement</div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 2.2], gap="large")

    # ── LEFT: Inputs ──────────────────────────
    with left_col:

        # Equation & Method card
        st.markdown('<div class="vintage-card"><div class="card-title"><span class="icon">𝑓</span> Equation & Method</div>', unsafe_allow_html=True)
        eq_str = st.text_input("Equation  f(x)", value="x**3 - x - 2", help="Use Python syntax: x**2, sp.sin(x), sp.exp(x)")
        method = st.selectbox("Algorithm", [
            "Incremental Search",
            "Bisection Method",
            "Regula-Falsi",
            "Newton-Raphson",
            "Secant Method"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # Parameters card
        st.markdown('<div class="vintage-card"><div class="card-title"><span class="icon">⚙</span> Parameters</div>', unsafe_allow_html=True)
        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            xl = st.number_input("Lower Bound  (xₗ)", value=1.0)
            xu = st.number_input("Upper Bound  (x_u)", value=2.0)
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess  (x₀)", value=1.0)
        elif method == "Secant Method":
            x0 = st.number_input("First Guess  (x₀)", value=1.0)
            x1 = st.number_input("Second Guess  (x₁)", value=2.0)

        tol     = st.number_input("Tolerance  (ε)", value=0.0001, format="%.6f")
        max_iter = int(st.number_input("Max Iterations", value=50, step=1, min_value=1, max_value=500))
        st.markdown('</div>', unsafe_allow_html=True)

        solve_btn = st.button("▶  Compute Root", use_container_width=True)

    # ── RIGHT: Results ────────────────────────
    with right_col:
        if solve_btn:
            try:
                xsym = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f  = sp.lambdify(xsym, expr, 'numpy')
                df_sym = sp.diff(expr, xsym)
                dff = sp.lambdify(xsym, df_sym, 'numpy')

                results, root, iterations, final_err = [], None, 0, 0.0

                # ── Algorithms ──────────────────
                if method == "Bisection Method":
                    _xl, _xu = xl, xu
                    for i in range(max_iter):
                        xr  = (_xl + _xu) / 2
                        err = abs(_xu - _xl) / 2
                        results.append({"Iter": i+1, "xₗ": round(_xl,6), "x_u": round(_xu,6),
                                        "xᵣ": round(xr,6), "f(xᵣ)": round(f(xr),6), "Error": round(err,6)})
                        if f(xr) == 0 or err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(_xl)*f(xr) < 0: _xu = xr
                        else: _xl = xr

                elif method == "Regula-Falsi":
                    _xl, _xu = xl, xu
                    for i in range(max_iter):
                        xr  = _xu - (f(_xu)*(_xl - _xu)) / (f(_xl) - f(_xu))
                        err = abs(f(xr))
                        results.append({"Iter": i+1, "xₗ": round(_xl,6), "x_u": round(_xu,6),
                                        "xᵣ": round(xr,6), "f(xᵣ)": round(f(xr),6), "Error": round(err,6)})
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(_xl)*f(xr) < 0: _xu = xr
                        else: _xl = xr

                elif method == "Newton-Raphson":
                    xr = x0
                    for i in range(max_iter):
                        fxr, dfxr = f(xr), dff(xr)
                        xr_new    = xr - fxr/dfxr
                        err       = abs(xr_new - xr)
                        results.append({"Iter": i+1, "xᵢ": round(xr,6), "f(xᵢ)": round(fxr,6),
                                        "f′(xᵢ)": round(dfxr,6), "xᵢ₊₁": round(xr_new,6), "Error": round(err,6)})
                        xr = xr_new
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break

                elif method == "Secant Method":
                    _x0, _x1 = x0, x1
                    for i in range(max_iter):
                        fx1, fx0 = f(_x1), f(_x0)
                        x2  = _x1 - (fx1*(_x0 - _x1)) / (fx0 - fx1)
                        err = abs(x2 - _x1)
                        results.append({"Iter": i+1, "x(i-1)": round(_x0,6), "x(i)": round(_x1,6),
                                        "x(i+1)": round(x2,6), "f(x(i+1))": round(f(x2),6), "Error": round(err,6)})
                        _x0, _x1 = _x1, x2
                        if err < tol:
                            root, iterations, final_err = x2, i+1, err; break

                elif method == "Incremental Search":
                    step, curr_x = 0.1, xl
                    for i in range(max_iter):
                        next_x = curr_x + step
                        results.append({"Iter": i+1, "x": round(curr_x,6), "f(x)": round(f(curr_x),6),
                                        "x_next": round(next_x,6), "f(x_next)": round(f(next_x),6)})
                        if f(curr_x)*f(next_x) < 0:
                            root, iterations, final_err = (curr_x+next_x)/2, i+2, abs(next_x-curr_x)/2; break
                        curr_x = next_x

                # ── Display results ──────────────
                if root is not None:
                    st.toast("Root located successfully", icon="✦")
                    time.sleep(0.3)

                    # Save to history
                    st.session_state.history.append({
                        "method":    method,
                        "equation":  eq_str,
                        "root":      round(root, 8),
                        "iters":     iterations,
                        "error":     round(final_err, 8) if final_err else 0,
                        "timestamp": datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                    })

                    # Metric strip
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Root  xᵣ",       f"{root:.7f}")
                    m2.metric("Iterations",      iterations)
                    m3.metric("Final Error  ε",  f"{final_err:.2e}" if final_err else "—")

                    st.markdown("---")

                    # Upper right: table  |  Lower right: graph
                    tbl_col, _ = st.columns([1, 0.001])
                    with tbl_col:
                        st.markdown('<div class="card-title"><span class="icon">📋</span> Iteration Table</div>', unsafe_allow_html=True)
                        df_results = pd.DataFrame(results)
                        st.dataframe(df_results, use_container_width=True, height=min(320, 42 + 35*len(results)))

                    st.markdown("---")

                    # Graph
                    st.markdown('<div class="card-title"><span class="icon">📈</span> Function Graph</div>', unsafe_allow_html=True)
                    x_vals = np.linspace(root - 3, root + 3, 400)
                    try:
                        y_vals = f(x_vals)
                        y_vals = np.where(np.abs(y_vals) > 200, np.nan, y_vals)
                    except Exception:
                        y_vals = np.zeros_like(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#7B5C3E', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dot", line_color="#4A3728", line_width=1.2)
                    fig.add_vline(x=0, line_dash="dot", line_color="#4A3728", line_width=1.2)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name=f'Root ≈ {root:.5f}',
                        marker=dict(color='#C9A84C', size=13, symbol='x-thin',
                                    line=dict(width=3, color='#8B4A2A'))
                    ))
                    fig.update_layout(
                        paper_bgcolor='#FAF7F2',
                        plot_bgcolor='#F5F0E8',
                        font=dict(family='EB Garamond, serif', color='#1A1208'),
                        title=dict(text=f"f(x) = {eq_str}", font=dict(family='Playfair Display, serif', size=15, color='#4A3728')),
                        xaxis=dict(title="x", gridcolor='#D9C9A8', linecolor='#C4A882', zerolinecolor='#7B5C3E'),
                        yaxis=dict(title="f(x)", gridcolor='#D9C9A8', linecolor='#C4A882', zerolinecolor='#7B5C3E'),
                        legend=dict(bgcolor='#EDE5D0', bordercolor='#C4A882', borderwidth=1, font=dict(size=12)),
                        hovermode="x unified",
                        margin=dict(l=10, r=10, t=50, b=10),
                        height=370
                    )
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("⚠  No root found within the given bounds/iterations. Try adjusting the parameters.")

            except Exception as e:
                st.error(f"Equation error: ensure valid Python syntax (e.g. `x**2`, `sp.sin(x)`).  Details: {e}")

        else:
            # Placeholder state
            st.markdown("""
            <div style="text-align:center; padding: 80px 20px; color: #C4A882; font-family:'EB Garamond',serif; font-style:italic; font-size:1.15rem;">
                Configure parameters on the left<br>and press <strong>Compute Root</strong> to begin.
                <div style="font-size:3rem; margin-top:18px; opacity:0.35;">𝑓(𝑥) = 0</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  MODULE 2 — MATRIX OPERATIONS
# ══════════════════════════════════════════════
elif app_mode == "Matrix Operations":
    st.markdown('<div class="module-header">Matrix Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-sub">Interactive matrix algebra — enter values directly in the editable grid</div>', unsafe_allow_html=True)

    st.markdown('<div class="vintage-card"><div class="card-title"><span class="icon">⊞</span> Select Operation</div>', unsafe_allow_html=True)
    op = st.selectbox("Operation", [
        "Addition", "Multiplication",
        "System of Equations (Ax = B)",
        "Adjoint", "Inverse", "Determinant",
        "Power of Matrix", "Transpose"
    ], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
        col1, col2 = st.columns(2, gap="large")
    else:
        col1, col2 = st.columns([1.4, 1], gap="large")

    with col1:
        st.markdown('<div class="vintage-card"><div class="card-title"><span class="icon">𝐴</span> Matrix A</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        rows_A = int(c1.number_input("Rows A", 1, 10, 3))
        cols_A = int(c2.number_input("Cols A", 1, 10, 3))
        df_A = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"Col {i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A = edited_A.to_numpy()
        st.markdown('</div>', unsafe_allow_html=True)

    if op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]:
        with col2:
            st.markdown('<div class="vintage-card"><div class="card-title"><span class="icon">𝐵</span> Matrix B</div>', unsafe_allow_html=True)
            if op == "System of Equations (Ax = B)":
                st.info("B must be a single-column results vector.")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:
                c1b, c2b = st.columns(2)
                rows_B = int(c1b.number_input("Rows B", 1, 10, cols_A, disabled=True))
                cols_B = int(c2b.number_input("Cols B", 1, 10, 3))
            df_B = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"Col {i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B = edited_B.to_numpy()
            st.markdown('</div>', unsafe_allow_html=True)

    if op == "Power of Matrix":
        with col2:
            st.markdown('<div class="vintage-card"><div class="card-title"><span class="icon">ⁿ</span> Settings</div>', unsafe_allow_html=True)
            power = int(st.number_input("Exponent n", value=2, step=1))
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    exec_btn = st.button("▶  Execute Matrix Operation", use_container_width=True)

    if exec_btn:
        try:
            with st.spinner("Computing…"):
                time.sleep(0.4)
                st.markdown('<div class="card-title"><span class="icon">📊</span> Result</div>', unsafe_allow_html=True)

                if op == "Addition":          result = A + B
                elif op == "Multiplication":  result = np.matmul(A, B)
                elif op == "Transpose":       result = A.T
                elif op == "Determinant":
                    det_val = np.linalg.det(A)
                    st.metric("Determinant  det(A)", f"{det_val:.6f}")
                    result = None
                elif op == "Inverse":         result = np.linalg.inv(A)
                elif op == "Adjoint":
                    result = np.round(np.linalg.inv(A) * np.linalg.det(A), 6)
                elif op == "Power of Matrix": result = np.linalg.matrix_power(A, power)
                elif op == "System of Equations (Ax = B)":
                    result = np.linalg.solve(A, B)
                    st.success("Solution vector **X** computed:")
                else:
                    result = None

                if result is not None:
                    st.dataframe(pd.DataFrame(result).style.format("{:.6g}"), use_container_width=True)
                    st.toast("Operation complete", icon="✦")

        except np.linalg.LinAlgError as e:
            st.error(f"Linear algebra error: {e}  (matrix may be singular or incompatible)")
        except ValueError as e:
            st.error(f"Dimension mismatch: {e}")

# ══════════════════════════════════════════════
#  MODULE 3 — CALCULATION HISTORY
# ══════════════════════════════════════════════
elif app_mode == "Calculation History":
    st.markdown('<div class="module-header">Calculation History</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-sub">Automatically saved log of all root-finding computations</div>', unsafe_allow_html=True)

    hcol1, hcol2 = st.columns([1, 5])
    with hcol1:
        if st.button("🗑  Clear History"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")

    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#C4A882;
                    font-family:'EB Garamond',serif; font-style:italic; font-size:1.1rem;">
            No calculations saved yet.<br>
            Run a root-finding method to populate the history log.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Table summary
        df_hist = pd.DataFrame(st.session_state.history)
        df_hist.index = range(1, len(df_hist)+1)
        df_hist.columns = ["Method", "Equation", "Root", "Iterations", "Final Error", "Timestamp"]
        st.dataframe(df_hist, use_container_width=True)

        st.markdown("---")
        st.markdown("**Detail Cards**")
        for i, h in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-meta">#{len(st.session_state.history)-i+1} &nbsp;·&nbsp; {h['timestamp']} &nbsp;·&nbsp; {h['method']}</div>
                <div style="font-size:0.95rem; color:#4A3728; margin-bottom:4px;">f(x) = {h['equation']}</div>
                <div class="history-answer">Root ≈ {h['root']}</div>
                <div style="font-family:'Lato',sans-serif; font-size:0.72rem; color:#7B5C3E; margin-top:4px; letter-spacing:0.06em;">
                    {h['iters']} iterations &nbsp;|&nbsp; ε = {h['error']}
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-container

# ── Footer ──────────────────────────────────
st.markdown("""
<div style="
    margin-top: 40px;
    border-top: 1px solid #C4A882;
    padding: 14px 32px 10px 32px;
    text-align: center;
    font-family: 'Lato', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7B5C3E;
    background: #EDE5D0;
">
    Diosamabel B. Penaso &nbsp;·&nbsp; BSCOMPE-2 &nbsp;·&nbsp; Numerical Methods &nbsp;·&nbsp; ✦
</div>
""", unsafe_allow_html=True)
