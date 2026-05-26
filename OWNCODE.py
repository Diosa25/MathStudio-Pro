import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RootSolver X — Numerical Methods",
    page_icon="⊛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
defaults = {
    "solve_results": [],
    "compare_results": {},
    "last_fig": None,
    "last_eq": "",
    "history": [],
    "active_tab": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS — DARK BIOPUNK TERMINAL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700;900&display=swap');

:root {
    --bg0:      #020508;
    --bg1:      #050d12;
    --bg2:      #081520;
    --bg3:      #0d1f2d;
    --bg4:      #102534;
    --cyan:     #00e5ff;
    --cyan2:    #00b4cc;
    --cyan3:    #007a8c;
    --teal:     #00ffd0;
    --teal2:    #00c8a0;
    --amber:    #ffb300;
    --amber2:   #ff8f00;
    --red:      #ff3d5a;
    --green:    #00e676;
    --border:   rgba(0,229,255,0.18);
    --border2:  rgba(0,229,255,0.35);
    --glow:     0 0 18px rgba(0,229,255,0.22);
    --glow2:    0 0 35px rgba(0,229,255,0.35);
    --text:     #b8d4e0;
    --text2:    #6a8fa0;
    --white:    #e8f4f8;
}

html, body, [class*="css"], .stApp {
    font-family: 'Rajdhani', 'Share Tech Mono', monospace;
    background-color: var(--bg0) !important;
    color: var(--text) !important;
}

/* Scanline overlay */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,229,255,0.012) 2px,
        rgba(0,229,255,0.012) 4px
    );
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    padding: 0.5rem 1.5rem 2rem 1.5rem;
    max-width: 100%;
}
#MainMenu, footer { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb { background: var(--cyan3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ─── HEADER ─── */
.site-header {
    position: relative;
    padding: 1.2rem 2rem 1.1rem 2rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #020d14 0%, #061624 40%, #091e2e 70%, #020d14 100%);
    border: 1px solid var(--border2);
    border-radius: 6px;
    overflow: hidden;
    box-shadow: var(--glow2), inset 0 1px 0 rgba(0,229,255,0.1);
}
.site-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--teal), var(--cyan), transparent);
    animation: scanH 3s linear infinite;
}
@keyframes scanH { 0%{opacity:0.4} 50%{opacity:1} 100%{opacity:0.4} }

.header-grid {
    display: flex; align-items: center; justify-content: space-between;
}
.header-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.85rem;
    font-weight: 900;
    color: var(--cyan);
    letter-spacing: 0.15em;
    text-shadow: 0 0 20px rgba(0,229,255,0.6), 0 0 40px rgba(0,229,255,0.3);
    line-height: 1;
}
.header-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--cyan3);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.header-right {
    text-align: right;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--text2);
    letter-spacing: 0.1em;
    line-height: 1.8;
}
.status-dot {
    display: inline-block; width: 7px; height: 7px;
    background: var(--green); border-radius: 50%;
    margin-right: 5px;
    box-shadow: 0 0 6px var(--green);
    animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

.header-badge {
    display: inline-block;
    background: rgba(0,229,255,0.08);
    border: 1px solid var(--border2);
    border-radius: 3px;
    padding: 0.15rem 0.6rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--cyan2);
    letter-spacing: 0.15em;
    margin-top: 0.35rem;
}
.corner-tl, .corner-tr, .corner-bl, .corner-br {
    position: absolute;
    width: 12px; height: 12px;
    border-color: var(--cyan);
    border-style: solid;
    opacity: 0.6;
}
.corner-tl { top: 6px; left: 6px; border-width: 1px 0 0 1px; }
.corner-tr { top: 6px; right: 6px; border-width: 1px 1px 0 0; }
.corner-bl { bottom: 6px; left: 6px; border-width: 0 0 1px 1px; }
.corner-br { bottom: 6px; right: 6px; border-width: 0 1px 1px 0; }

/* ─── PANELS ─── */
.panel {
    background: linear-gradient(145deg, var(--bg1) 0%, var(--bg2) 100%);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.1rem 1.2rem;
    box-shadow: var(--glow), inset 0 1px 0 rgba(0,229,255,0.06);
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan2), transparent);
    opacity: 0.5;
}
.panel-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--cyan);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.panel-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--cyan3), transparent);
    opacity: 0.4;
}

/* ─── ROOT CARDS ─── */
.root-card {
    background: linear-gradient(135deg, rgba(0,229,255,0.05) 0%, rgba(0,255,208,0.03) 100%);
    border: 1px solid var(--border2);
    border-radius: 5px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
    position: relative;
    transition: all 0.3s ease;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
.root-card:hover {
    border-color: var(--cyan);
    box-shadow: var(--glow2);
    transform: translateX(3px);
}
.root-card-num {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    color: var(--cyan3);
    letter-spacing: 0.2em;
    margin-bottom: 0.3rem;
}
.root-card-val {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.25rem;
    color: var(--cyan);
    text-shadow: 0 0 12px rgba(0,229,255,0.5);
    font-weight: 700;
}
.root-card-meta {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--text2);
    margin-top: 0.25rem;
    display: flex; gap: 1rem; flex-wrap: wrap;
}
.root-card-meta span { color: var(--teal2); }
.root-acc-bar {
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--teal));
    border-radius: 1px;
    margin-top: 0.5rem;
    box-shadow: 0 0 6px rgba(0,229,255,0.4);
}

/* ─── METHOD BADGE ─── */
.method-tag {
    display: inline-block;
    background: rgba(0,229,255,0.1);
    border: 1px solid var(--cyan3);
    border-radius: 3px;
    padding: 0.15rem 0.55rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    color: var(--cyan2);
    letter-spacing: 0.1em;
    margin: 0.1rem;
}

/* ─── FORMULA BOX ─── */
.formula-box {
    background: rgba(0,0,0,0.5);
    border: 1px solid var(--border);
    border-left: 3px solid var(--cyan);
    border-radius: 4px;
    padding: 0.7rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: var(--teal);
    margin-bottom: 0.7rem;
    letter-spacing: 0.05em;
    line-height: 1.7;
}

/* ─── WARNING / INFO ─── */
.warn-box {
    background: rgba(255,179,0,0.07);
    border: 1px solid rgba(255,179,0,0.35);
    border-left: 3px solid var(--amber);
    border-radius: 4px;
    padding: 0.65rem 1rem;
    font-family: 'Rajdhani', monospace;
    font-size: 0.9rem;
    color: #f0cc70;
    margin-bottom: 0.7rem;
}
.info-box {
    background: rgba(0,229,255,0.05);
    border: 1px solid var(--border);
    border-left: 3px solid var(--cyan2);
    border-radius: 4px;
    padding: 0.65rem 1rem;
    font-family: 'Rajdhani', monospace;
    font-size: 0.88rem;
    color: var(--text);
    margin-bottom: 0.7rem;
}
.success-box {
    background: rgba(0,230,118,0.06);
    border: 1px solid rgba(0,230,118,0.3);
    border-left: 3px solid var(--green);
    border-radius: 4px;
    padding: 0.65rem 1rem;
    font-family: 'Rajdhani', monospace;
    font-size: 0.88rem;
    color: #80ffc0;
    margin-bottom: 0.7rem;
}

/* ─── SECTION TITLE ─── */
.sec-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--cyan);
    letter-spacing: 0.22em;
    text-transform: uppercase;
    padding: 0.5rem 0 0.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}

/* ─── COMPARE GRID ─── */
.compare-cell {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.6rem 0.85rem;
    margin-bottom: 0.4rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
}
.compare-label { color: var(--text2); font-size: 0.68rem; letter-spacing: 0.15em; margin-bottom: 0.2rem; }
.compare-value { color: var(--cyan); font-size: 0.95rem; }

/* ─── WIDGET OVERRIDES ─── */
.stSelectbox > label, .stNumberInput > label, .stTextInput > label,
.stSlider > label, .stRadio > label {
    font-family: 'Rajdhani', monospace !important;
    color: var(--text2) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 4px !important;
    color: var(--cyan2) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.88rem !important;
}
.stTextInput input, .stNumberInput input {
    background: var(--bg2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 4px !important;
    color: var(--teal) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.9rem !important;
    caret-color: var(--cyan) !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.15) !important;
}
div[data-testid="stRadio"] label > div p {
    font-family: 'Rajdhani', monospace !important;
    font-size: 0.88rem !important;
    color: var(--text) !important;
    letter-spacing: 0.05em !important;
}

/* ─── BUTTON ─── */
.stButton > button {
    width: 100%;
    border-radius: 4px;
    background: linear-gradient(135deg, #00384a 0%, #004d63 50%, #003848 100%);
    color: var(--cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    border: 1px solid var(--cyan2) !important;
    letter-spacing: 0.18em !important;
    padding: 0.6rem 1rem !important;
    box-shadow: 0 0 12px rgba(0,229,255,0.15), inset 0 1px 0 rgba(0,229,255,0.1) !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
    position: relative;
    overflow: hidden;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00516e 0%, #006a8a 100%) !important;
    box-shadow: 0 0 22px rgba(0,229,255,0.35) !important;
    transform: translateY(-1px) !important;
    border-color: var(--cyan) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ─── METRICS ─── */
[data-testid="metric-container"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    padding: 0.7rem 0.9rem !important;
    box-shadow: var(--glow) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--text2) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    color: var(--cyan) !important;
    font-size: 1.35rem !important;
    text-shadow: 0 0 10px rgba(0,229,255,0.4) !important;
}

/* ─── DATAFRAME ─── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
}
[data-testid="stDataFrame"] th {
    background: #031520 !important;
    color: var(--cyan2) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    border-bottom: 1px solid var(--border2) !important;
}
[data-testid="stDataFrame"] td {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.78rem !important;
    color: var(--text) !important;
    background: var(--bg1) !important;
}
[data-testid="stDataFrame"] tr:hover td { background: var(--bg3) !important; }

/* ─── ALERTS ─── */
[data-testid="stAlert"], [data-testid="stInfo"], [data-testid="stSuccess"],
[data-testid="stWarning"], [data-testid="stError"] {
    font-family: 'Rajdhani', monospace !important;
    border-radius: 4px !important;
}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020810 0%, #040e18 50%, #020810 100%) !important;
    border-right: 1px solid var(--border2) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #011018, #021828) !important;
    border-color: var(--border2) !important;
    font-size: 0.72rem !important;
    color: var(--cyan2) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #002030, #003040) !important;
    border-color: var(--cyan) !important;
}

/* ─── HISTORY SIDEBAR ─── */
.hist-card {
    background: rgba(0,229,255,0.04);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.5rem;
    transition: all 0.2s;
}
.hist-card:hover { background: rgba(0,229,255,0.08); border-color: var(--cyan2); }
.hist-method { font-family:'Orbitron',monospace; font-size:0.65rem; color:var(--cyan2); letter-spacing:0.12em; margin-bottom:0.2rem; }
.hist-eq     { font-family:'Share Tech Mono',monospace; font-size:0.8rem; color:var(--teal2); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.hist-ans    { font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:var(--text); margin-top:0.15rem; }
.hist-ts     { font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:var(--text2); margin-top:0.1rem; }
.hist-empty  { text-align:center; padding:1.8rem 0.5rem; font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:var(--text2); letter-spacing:0.1em; line-height:2; }
.sidebar-hdr { font-family:'Orbitron',monospace; font-size:0.72rem; font-weight:700; color:var(--cyan); letter-spacing:0.22em; text-align:center; padding:0.3rem 0 0.7rem 0; border-bottom:1px solid var(--border); margin-bottom:0.7rem; }

/* ─── PLACEHOLDER ─── */
.placeholder-box {
    text-align: center;
    padding: 3rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: var(--text2);
    line-height: 2.2;
    letter-spacing: 0.1em;
}
.placeholder-box .big-icon { font-size: 2.5rem; margin-bottom: 0.8rem; filter: grayscale(0.3); }

/* ─── PRESET BUTTONS ─── */
.preset-eq {
    display: inline-block;
    background: rgba(0,229,255,0.06);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 0.2rem 0.6rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--cyan2);
    margin: 0.15rem;
    cursor: pointer;
    transition: all 0.2s;
}
.preset-eq:hover { background: rgba(0,229,255,0.15); border-color: var(--cyan); color: var(--cyan); }

/* ─── EXPANDER ─── */
details > summary {
    font-family: 'Rajdhani', monospace !important;
    color: var(--cyan2) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    background: var(--bg1) !important;
}

/* ─── TABS ─── */
[data-testid="stTabs"] button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    color: var(--text2) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
}

/* ─── HR ─── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 0.6rem 0 !important; }

/* ─── CONVERGENCE STATUS ─── */
.conv-yes { color: #00e676; font-weight: 700; }
.conv-no  { color: #ff3d5a; font-weight: 700; }

/* Grid background pattern */
.data-grid {
    background-image:
        linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px;
    background-position: -1px -1px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CORE NUMERICAL ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def parse_equation(eq_str: str):
    """Parse equation string into sympy expr and numpy lambda. Returns (expr, f, df, err_msg)."""
    try:
        safe = (eq_str.strip()
                .replace('^', '**')
                .replace('ln(', 'log(')
                .replace('e^', 'exp(1)**')
                )
        x = sp.Symbol('x')
        expr = sp.sympify(safe, locals={'x': x, 'e': sp.E, 'pi': sp.pi,
                                         'ln': sp.log, 'log': sp.log,
                                         'sin': sp.sin, 'cos': sp.cos,
                                         'tan': sp.tan, 'exp': sp.exp,
                                         'sqrt': sp.sqrt, 'abs': sp.Abs})
        deriv = sp.diff(expr, x)
        modules = [{'log': np.log, 'exp': np.exp, 'sin': np.sin,
                    'cos': np.cos, 'tan': np.tan, 'sqrt': np.sqrt,
                    'Abs': np.abs, 'pi': np.pi, 'E': np.e}, 'numpy']
        f  = sp.lambdify(x, expr,  modules=modules)
        df = sp.lambdify(x, deriv, modules=modules)
        return expr, f, df, None
    except Exception as e:
        return None, None, None, str(e)


def safe_eval(f, x_val):
    """Evaluate f at x safely, returning np.nan on error."""
    try:
        v = float(f(x_val))
        return v if np.isfinite(v) else np.nan
    except Exception:
        return np.nan


def scan_brackets(f, a, b, n=2000):
    """Find all sign-change brackets in [a, b]."""
    xs = np.linspace(a, b, n)
    brackets = []
    prev_f = safe_eval(f, xs[0])
    for i in range(1, len(xs)):
        curr_f = safe_eval(f, xs[i])
        if (not np.isnan(prev_f) and not np.isnan(curr_f)
                and prev_f * curr_f < 0):
            # Avoid duplicate brackets
            if not brackets or abs(xs[i-1] - brackets[-1][1]) > 1e-9:
                brackets.append((float(xs[i-1]), float(xs[i])))
        prev_f = curr_f
    return brackets


def bisection(f, xl, xu, tol, max_iter):
    rows, root, ea = [], None, None
    xr_old = None
    for i in range(int(max_iter)):
        xr  = (xl + xu) / 2
        fxl = safe_eval(f, xl)
        fxr = safe_eval(f, xr)
        ea  = abs((xr - xr_old) / xr) * 100 if xr_old is not None and xr != 0 else None
        converged = ea is not None and ea < tol
        rows.append({
            "Iter": i+1, "x_l": round(xl,8), "x_r": round(xr,8), "x_u": round(xu,8),
            "f(x_r)": round(fxr, 8),
            "|Ea| %": round(ea, 6) if ea is not None else "—",
            "Status": "✓ CONV" if converged else "→"
        })
        if converged or fxr == 0:
            root = xr; break
        if fxl * fxr < 0: xu = xr
        else:              xl = xr
        xr_old = xr
    if root is None: root = xr_old or (xl+xu)/2
    return root, ea or 0, rows


def regula_falsi(f, xl, xu, tol, max_iter):
    rows, root, ea = [], None, None
    xr_old = None
    for i in range(int(max_iter)):
        fxl, fxu = safe_eval(f, xl), safe_eval(f, xu)
        if fxl == fxu: break
        xr  = xu - fxu * (xl - xu) / (fxl - fxu)
        fxr = safe_eval(f, xr)
        ea  = abs((xr - xr_old) / xr) if xr_old is not None and xr != 0 else None
        converged = ea is not None and ea < tol
        rows.append({
            "Iter": i+1, "x_L": round(xl,8), "x_R": round(xr,8), "x_U": round(xu,8),
            "f(x_R)": round(fxr, 8),
            "Ea": round(ea, 8) if ea is not None else "—",
            "Status": "✓ CONV" if converged else "→"
        })
        if converged or fxr == 0:
            root = xr; break
        if fxl * fxr < 0: xu = xr
        else:              xl = xr
        xr_old = xr
    if root is None: root = xr_old or (xl+xu)/2
    return root, ea or 0, rows


def newton_raphson(f, df, x0, tol, max_iter):
    rows, root, ea = [], None, None
    xi = x0
    for i in range(int(max_iter)):
        fxi  = safe_eval(f,  xi)
        dfxi = safe_eval(df, xi)
        if np.isnan(fxi) or np.isnan(dfxi) or abs(dfxi) < 1e-14:
            rows.append({"Iter": i+1, "x_i": round(xi,8), "f(x_i)": round(fxi,8) if not np.isnan(fxi) else "NaN",
                         "f'(x_i)": "~0 or NaN", "Ea": "—", "Status": "✗ FAIL"}); break
        xi_new = xi - fxi / dfxi
        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        converged = ea < tol
        rows.append({
            "Iter": i+1, "x_i": round(xi,8), "f(x_i)": round(fxi,8),
            "f'(x_i)": round(dfxi,8),
            "x_{i+1}": round(xi_new,8),
            "Ea": round(ea,8),
            "Status": "✓ CONV" if converged else "→"
        })
        xi = xi_new
        if converged:
            root = xi; break
    if root is None: root = xi
    return root, ea or 0, rows


def secant(f, x0, x1, tol, max_iter):
    rows, root, ea = [], None, None
    xp, xc = x0, x1
    for i in range(int(max_iter)):
        fxp, fxc = safe_eval(f, xp), safe_eval(f, xc)
        if abs(fxc - fxp) < 1e-14: break
        xn = xc - fxc * (xc - xp) / (fxc - fxp)
        ea = abs((xn - xc) / xn) if xn != 0 else abs(xn - xc)
        converged = ea < tol
        rows.append({
            "Iter": i+1, "x_{i-1}": round(xp,8), "x_i": round(xc,8),
            "x_{i+1}": round(xn,8), "f(x_{i+1})": round(safe_eval(f,xn),8),
            "Ea": round(ea,8),
            "Status": "✓ CONV" if converged else "→"
        })
        xp, xc = xc, xn
        if converged:
            root = xn; break
    if root is None: root = xc
    return root, ea or 0, rows


def incremental(f, xl, xu, tol, max_iter):
    """Incremental search with progressive interval shrinking."""
    rows, root, ea = [], None, None
    dx = (xu - xl) / 20.0
    cx = xl
    for i in range(int(max_iter)):
        nx = cx + dx
        fcx, fnx = safe_eval(f, cx), safe_eval(f, nx)
        if np.isnan(fcx) or np.isnan(fnx):
            cx = nx; continue
        prod = fcx * fnx
        remark = "Next interval" if prod > 0 else "Sign change — refine Δx"
        rows.append({
            "Iter": i+1, "x_l": round(cx,8), "Δx": round(dx,8),
            "x_u": round(nx,8), "f(x_l)": round(fcx,8), "f(x_u)": round(fnx,8),
            "f·f sign": "> 0" if prod > 0 else "< 0",
            "Remark": remark
        })
        if abs(fnx) < tol or dx < tol / 100:
            root = nx; ea = abs(fnx); break
        if prod > 0:
            cx = nx
        else:
            dx /= 10.0
    if root is None: root = cx
    return root, ea or 0, rows


def solve_root_in_bracket(method, f, df, xl, xu, tol, max_iter):
    xm = (xl + xu) / 2.0
    xm2 = xl + (xu - xl) * 0.3
    if   method == "Bisection Method":       return bisection(f, xl, xu, tol, max_iter)
    elif method == "Regula Falsi":           return regula_falsi(f, xl, xu, tol, max_iter)
    elif method == "Newton-Raphson Method":  return newton_raphson(f, df, xm, tol, max_iter)
    elif method == "Secant Method":          return secant(f, xm2, xm, tol, max_iter)
    elif method == "Incremental Search":     return incremental(f, xl, xu, tol, max_iter)
    return None, 0, []


# ══════════════════════════════════════════════════════════════════════════════
#  PLOTLY THEME HELPERS
# ══════════════════════════════════════════════════════════════════════════════
PLOT_COLORS = ['#00e5ff','#00ffd0','#ffb300','#ff3d5a','#b388ff','#69f0ae','#ff8a65','#40c4ff']

def make_figure(f, a, b, all_roots):
    margin = (b - a) * 0.12
    xs = np.linspace(a - margin, b + margin, 1200)
    ys = np.array([safe_eval(f, xi) for xi in xs], dtype=float)

    # Clip extreme values
    q99 = np.nanpercentile(np.abs(ys[np.isfinite(ys)]), 99) if np.any(np.isfinite(ys)) else 1e6
    ys_clipped = np.where(np.abs(ys) > min(q99 * 3, 1e5), np.nan, ys)

    fig = go.Figure()

    # Grid-like background effect via shapes
    fig.update_layout(
        plot_bgcolor='#030d14',
        paper_bgcolor='#020810',
    )

    # Function curve
    fig.add_trace(go.Scatter(
        x=xs, y=ys_clipped, mode='lines', name='f(x)',
        line=dict(color='#00e5ff', width=2.2),
        hovertemplate='x = %{x:.5f}<br>f(x) = %{y:.5f}<extra></extra>'
    ))

    # Zero lines
    fig.add_hline(y=0, line_dash="dot", line_color='rgba(0,229,255,0.3)', line_width=1)
    fig.add_vline(x=0, line_dash="dot", line_color='rgba(0,229,255,0.2)', line_width=0.8)

    # Root markers
    for idx, r in enumerate(all_roots):
        col = PLOT_COLORS[idx % len(PLOT_COLORS)]
        fy  = safe_eval(f, r['root'])
        fig.add_trace(go.Scatter(
            x=[r['root']], y=[0],
            mode='markers+text',
            name=f"Root {idx+1}  x={r['root']:.6f}",
            marker=dict(color=col, size=14, symbol='circle',
                        line=dict(color='#ffffff', width=1.5),
                        opacity=0.95),
            text=[f"  x={r['root']:.5f}"],
            textposition='top right',
            textfont=dict(family='Share Tech Mono', size=10, color=col),
            hovertemplate=f"Root {idx+1}<br>x = {r['root']:.8f}<br>f(x) ≈ {fy:.2e}<extra></extra>"
        ))
        # Drop line to x-axis
        fig.add_shape(type='line',
            x0=r['root'], x1=r['root'], y0=0, y1=fy if abs(fy) < 1e4 else 0,
            line=dict(color=col, width=1, dash='dot'), opacity=0.4)

    fig.update_layout(
        font=dict(family='Share Tech Mono, monospace', color='#6a8fa0'),
        xaxis=dict(
            title='x', gridcolor='rgba(0,229,255,0.06)', linecolor='rgba(0,229,255,0.2)',
            zerolinecolor='rgba(0,229,255,0.15)', tickfont=dict(family='Share Tech Mono'),
            title_font=dict(color='#00e5ff'), showgrid=True,
        ),
        yaxis=dict(
            title='f(x)', gridcolor='rgba(0,229,255,0.06)', linecolor='rgba(0,229,255,0.2)',
            zerolinecolor='rgba(0,229,255,0.15)', tickfont=dict(family='Share Tech Mono'),
            title_font=dict(color='#00e5ff'), showgrid=True,
        ),
        legend=dict(
            bgcolor='rgba(3,13,20,0.85)', bordercolor='rgba(0,229,255,0.25)',
            borderwidth=1, font=dict(family='Share Tech Mono', size=10, color='#b8d4e0'),
        ),
        hovermode='x unified',
        margin=dict(l=10, r=10, t=30, b=10),
        height=360,
    )
    return fig


def make_convergence_chart(rows_list, labels):
    """Multi-line convergence chart of |Ea| per iteration."""
    fig = go.Figure()
    colors = PLOT_COLORS[:len(rows_list)]
    for rows, label, col in zip(rows_list, labels, colors):
        iters, eas = [], []
        for r in rows:
            ea_val = r.get("Ea", r.get("|Ea| %", "—"))
            try:
                ea_val = float(ea_val)
                iters.append(r.get("Iter", len(iters)+1))
                eas.append(ea_val)
            except Exception:
                pass
        if iters:
            fig.add_trace(go.Scatter(
                x=iters, y=eas, mode='lines+markers', name=label,
                line=dict(color=col, width=2),
                marker=dict(size=5, color=col),
                hovertemplate='Iter %{x}<br>Ea = %{y:.3e}<extra></extra>'
            ))
    fig.update_layout(
        plot_bgcolor='#030d14', paper_bgcolor='#020810',
        font=dict(family='Share Tech Mono', color='#6a8fa0'),
        xaxis=dict(title='Iteration', gridcolor='rgba(0,229,255,0.06)',
                   linecolor='rgba(0,229,255,0.2)', tickfont=dict(family='Share Tech Mono'),
                   title_font=dict(color='#00e5ff')),
        yaxis=dict(title='Approx. Error (Ea)', type='log', gridcolor='rgba(0,229,255,0.06)',
                   linecolor='rgba(0,229,255,0.2)', tickfont=dict(family='Share Tech Mono'),
                   title_font=dict(color='#00e5ff')),
        legend=dict(bgcolor='rgba(3,13,20,0.85)', bordercolor='rgba(0,229,255,0.25)',
                    borderwidth=1, font=dict(family='Share Tech Mono', size=10, color='#b8d4e0')),
        hovermode='x unified',
        margin=dict(l=10, r=10, t=20, b=10),
        height=260,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-hdr">⊛ SOLVE HISTORY</div>', unsafe_allow_html=True)

    if st.session_state.history:
        if st.button("⊘ Clear History"):
            st.session_state.history = []
            st.rerun()
        for entry in reversed(st.session_state.history[-15:]):
            st.markdown(f"""
                <div class="hist-card">
                    <div class="hist-method">{entry['method']}</div>
                    <div class="hist-eq">{entry['equation']}</div>
                    <div class="hist-ans">{entry['answer']}</div>
                    <div class="hist-ts">{entry['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="hist-empty">
                NO HISTORY YET<br>
                ──────────────<br>
                Results will appear<br>
                after solving.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.65rem;color:#2a4a5a;text-align:center;letter-spacing:0.15em;line-height:2;">ROOTSOLVER X v2.0<br>NUMERICAL METHODS ENGINE<br>PYTHON · SYMPY · NUMPY</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="site-header data-grid">
    <div class="corner-tl"></div>
    <div class="corner-tr"></div>
    <div class="corner-bl"></div>
    <div class="corner-br"></div>
    <div class="header-grid">
        <div>
            <div class="header-logo">⊛ ROOTSOLVER X</div>
            <div class="header-sub">Numerical Methods Root-Finding Engine</div>
            <div class="header-badge">MULTI-ROOT DETECTION · ADAPTIVE SCAN · CONVERGENCE ANALYSIS</div>
        </div>
        <div class="header-right">
            <div><span class="status-dot"></span>SYSTEM ONLINE</div>
            <div>PYTHON · SYMPY · PLOTLY</div>
            <div>BISECTION · NR · SECANT · RF · INCR</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
col_ctrl, col_main = st.columns([1, 2.6])

# ──────────────────────────────────────────────────────────────────────────────
#  LEFT: CONTROL PANEL
# ──────────────────────────────────────────────────────────────────────────────
with col_ctrl:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⊛ EQUATION INPUT</div>', unsafe_allow_html=True)

    # Presets
    PRESETS = [
        ("x³-6x²+11x-6",   "x**3 - 6*x**2 + 11*x - 6"),
        ("ln(x)+x-3",       "log(x) + x - 3"),
        ("e^(-x)-x",        "exp(-x) - x"),
        ("x⁵-x³+2x-1",      "x**5 - x**3 + 2*x - 1"),
        ("ln(x)-sin(x)",    "log(x) - sin(x)"),
        ("e^x-3x",          "exp(x) - 3*x"),
    ]
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.65rem;color:#2a6a7a;letter-spacing:0.12em;margin-bottom:0.4rem;">QUICK PRESETS →</div>', unsafe_allow_html=True)

    preset_cols = st.columns(2)
    preset_clicked = None
    for pi, (label, val) in enumerate(PRESETS):
        with preset_cols[pi % 2]:
            if st.button(label, key=f"preset_{pi}"):
                preset_clicked = val

    eq_str = st.text_input(
        "f(x) = ",
        value=preset_clicked if preset_clicked else st.session_state.get("eq_cache", "x**3 - 6*x**2 + 11*x - 6"),
        key="eq_input",
        help="Python/SymPy syntax: x**2, log(x), exp(x), sin(x), cos(x), sqrt(x)"
    )
    if preset_clicked:
        st.session_state["eq_cache"] = preset_clicked

    st.markdown('<div class="info-box">Supports: <b>log(x)</b>=ln(x), <b>exp(x)</b>=eˣ, <b>sin/cos/tan</b>, <b>sqrt(x)</b>, <b>x**n</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⊙ METHOD & RANGE</div>', unsafe_allow_html=True)

    method = st.selectbox("Root-Finding Method", [
        "Bisection Method", "Regula Falsi",
        "Newton-Raphson Method", "Secant Method", "Incremental Search"
    ])

    c1, c2 = st.columns(2)
    a_range = c1.number_input("Range  a", value=-2.0, format="%.3f", key="ra")
    b_range = c2.number_input("Range  b", value=4.0,  format="%.3f", key="rb")

    tol      = st.number_input("Tolerance (Ea)", value=1e-6, format="%.2e", min_value=1e-15)
    max_iter = st.number_input("Max Iterations", value=100,  step=10, min_value=5)
    n_scan   = st.number_input("Scan Points", value=2000, step=500, min_value=200,
                                help="Higher = finds more roots in dense regions")

    st.markdown('</div>', unsafe_allow_html=True)

    solve_btn   = st.button("⊛  SOLVE — FIND ALL ROOTS", use_container_width=True)
    compare_btn = st.button("⊞  RUN ALL METHODS & COMPARE", use_container_width=True)

    # Method formula display
    METHOD_FORMULAS = {
        "Bisection Method":      "xᵣ = (x_L + x_U) / 2\nSign change: f(x_L)·f(xᵣ) < 0\nEa = |Δxᵣ / xᵣ| × 100%",
        "Regula Falsi":          "xᵣ = x_U − f(x_U)·(x_L−x_U)\n         / (f(x_L)−f(x_U))\nEa = |xᵣ_new − xᵣ_old| / |xᵣ_new|",
        "Newton-Raphson Method": "x_{i+1} = x_i − f(x_i) / f′(x_i)\nEa = |x_new − x_old| / |x_new|",
        "Secant Method":         "x_{i+1} = x_i − f(x_i)·(x_i−x_{i-1})\n           / (f(x_i)−f(x_{i-1}))",
        "Incremental Search":    "Scan x in steps of Δx\nFind where f(x_i)·f(x_{i+1}) < 0\nRefine by shrinking Δx → Δx/10",
    }
    st.markdown(f'<div class="formula-box">{METHOD_FORMULAS[method]}</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  RIGHT: RESULTS AREA
# ──────────────────────────────────────────────────────────────────────────────
with col_main:

    # ── SOLVE ──
    if solve_btn or compare_btn:
        expr_sym, f_lam, df_lam, parse_err = parse_equation(eq_str)

        if parse_err:
            st.error(f"⊘ Parse Error: {parse_err}")
        elif b_range <= a_range:
            st.error("⊘ Range b must be greater than a.")
        else:
            brackets = scan_brackets(f_lam, a_range, b_range, n=int(n_scan))

            if not brackets:
                st.markdown(f'<div class="warn-box">⚠ No sign changes detected in [{a_range}, {b_range}]. Try expanding range or increasing scan points.</div>', unsafe_allow_html=True)
            else:
                all_roots_data = []
                all_rows_for_conv = []
                all_labels_for_conv = []

                if solve_btn:
                    methods_to_run = [method]
                else:
                    methods_to_run = ["Bisection Method", "Regula Falsi", "Newton-Raphson Method", "Secant Method"]

                seen_roots = []
                for m in methods_to_run:
                    for bk in brackets:
                        xl_b, xu_b = bk
                        root, ea, rows = solve_root_in_bracket(m, f_lam, df_lam, xl_b, xu_b, tol, int(max_iter))
                        if root is None: continue
                        # Dedup
                        is_dup = any(abs(root - sr['root']) < max(tol * 1000, 1e-6) and sr['method'] == m for sr in seen_roots)
                        if not is_dup:
                            entry = {"root": root, "error": ea, "iterations": len(rows),
                                     "method": m, "bracket": bk, "rows": rows,
                                     "f_val": safe_eval(f_lam, root)}
                            all_roots_data.append(entry)
                            seen_roots.append({"root": root, "method": m})
                            all_rows_for_conv.append(rows)
                            all_labels_for_conv.append(f"{m[:4]}… Bracket [{xl_b:.2f},{xu_b:.2f}]")

                if not all_roots_data:
                    st.markdown('<div class="warn-box">⚠ Brackets found but no roots converged. Adjust tolerance or max iterations.</div>', unsafe_allow_html=True)
                else:
                    # Build figure (use first method's unique roots for plotting)
                    unique_for_plot = []
                    seen_vals = []
                    for r in all_roots_data:
                        if not any(abs(r['root'] - sv) < 1e-5 for sv in seen_vals):
                            unique_for_plot.append(r)
                            seen_vals.append(r['root'])

                    fig = make_figure(f_lam, a_range, b_range, unique_for_plot)

                    st.session_state.solve_results = all_roots_data
                    st.session_state.last_fig      = fig
                    st.session_state.last_eq       = eq_str

                    # History
                    roots_str = " | ".join([f"x≈{r['root']:.5f}" for r in unique_for_plot])
                    method_str = method if solve_btn else "ALL METHODS"
                    st.session_state.history.append({
                        "method":    method_str,
                        "equation":  f"f(x) = {eq_str}",
                        "answer":    f"{len(unique_for_plot)} root(s): {roots_str}",
                        "timestamp": datetime.now().strftime("%b %d %H:%M:%S"),
                    })
                    st.toast(f"Found {len(unique_for_plot)} root(s)!", icon="⊛")

    # ── DISPLAY RESULTS ──
    if st.session_state.solve_results:
        all_roots_data = st.session_state.solve_results

        # Unique roots for metrics
        seen_vals = []
        unique_roots = []
        for r in all_roots_data:
            if not any(abs(r['root'] - sv) < 1e-5 for sv in seen_vals):
                unique_roots.append(r)
                seen_vals.append(r['root'])

        # ── METRICS ROW ──
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("ROOTS FOUND", len(unique_roots))
        m2.metric("METHOD", all_roots_data[0]['method'][:12] + "…" if len(all_roots_data[0]['method'])>12 else all_roots_data[0]['method'])
        m3.metric("BRACKETS", len(set(r['bracket'] for r in all_roots_data)))
        best_err = min(r['error'] for r in all_roots_data if r['error']) if any(r['error'] for r in all_roots_data) else 0
        m4.metric("BEST Ea", f"{best_err:.2e}" if best_err else "—")

        # ── TABS ──
        tabs = st.tabs(["⊛ GRAPH", "⊞ ROOT CARDS", "▦ ITERATION TABLES", "◈ CONVERGENCE", "⊟ COMPARE"])

        # ──── TAB 1: GRAPH ────
        with tabs[0]:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="panel-title">⊛ FUNCTION GRAPH — f(x) = {st.session_state.last_eq[:60]}</div>', unsafe_allow_html=True)
            st.plotly_chart(st.session_state.last_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Equation info
            expr_sym2, _, _, _ = parse_equation(st.session_state.last_eq)
            if expr_sym2 is not None:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-title">⊙ EQUATION ANALYSIS</div>', unsafe_allow_html=True)
                ac1, ac2 = st.columns(2)
                with ac1:
                    x = sp.Symbol('x')
                    try:
                        deriv = sp.diff(expr_sym2, x)
                        st.markdown(f'<div class="formula-box">f(x)  =  {sp.pretty(expr_sym2)}\nf\'(x) =  {sp.pretty(deriv)}</div>', unsafe_allow_html=True)
                    except:
                        pass
                with ac2:
                    st.markdown(f'<div class="formula-box">Range  : [{a_range}, {b_range}]\nTolerance  : {tol:.2e}\nScan Pts   : {n_scan}\nBrackets   : {len(set(r["bracket"] for r in all_roots_data))}\nRoots Found: {len(unique_roots)}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # ──── TAB 2: ROOT CARDS ────
        with tabs[1]:
            st.markdown('<div class="sec-title">⊞ ALL DETECTED ROOTS</div>', unsafe_allow_html=True)

            # Summary dataframe
            summary = []
            for i, r in enumerate(unique_roots):
                summary.append({
                    "Root #": f"Root {i+1}",
                    "x value": round(r['root'], 10),
                    "f(x) at root": f"{r['f_val']:.4e}",
                    "Iterations": r['iterations'],
                    "Final Ea": f"{r['error']:.4e}" if r['error'] else "—",
                    "Method": r['method'],
                    "Bracket": f"[{r['bracket'][0]:.4f}, {r['bracket'][1]:.4f}]",
                })
            st.dataframe(pd.DataFrame(summary), use_container_width=True, height=min(250, 60+42*len(summary)))

            st.markdown('<div class="sec-title" style="margin-top:1rem;">◈ ROOT DETAIL CARDS</div>', unsafe_allow_html=True)
            card_cols = st.columns(min(3, len(unique_roots)))
            for i, r in enumerate(unique_roots):
                col = PLOT_COLORS[i % len(PLOT_COLORS)]
                with card_cols[i % len(card_cols)]:
                    accuracy = max(0, 100 - r['error']*100) if r['error'] < 1 else 0
                    st.markdown(f"""
                        <div class="root-card">
                            <div class="root-card-num">ROOT  {i+1}  /  {len(unique_roots)}</div>
                            <div class="root-card-val" style="color:{col};text-shadow:0 0 12px {col}88;">
                                x = {r['root']:.8f}
                            </div>
                            <div class="root-card-meta">
                                <span>f(x) ≈ {r['f_val']:.3e}</span>
                                <span>Ea = {r['error']:.3e}</span>
                                <span>{r['iterations']} iters</span>
                            </div>
                            <div class="root-card-meta" style="margin-top:0.2rem;">
                                <div class="method-tag">{r['method']}</div>
                            </div>
                            <div class="root-acc-bar" style="background:linear-gradient(90deg,{col},{col}88);width:{min(100,100-r['error']*1e4):.0f}%;min-width:8%"></div>
                        </div>
                    """, unsafe_allow_html=True)

        # ──── TAB 3: ITERATION TABLES ────
        with tabs[2]:
            st.markdown('<div class="sec-title">▦ ITERATION CONVERGENCE TABLES</div>', unsafe_allow_html=True)

            # Group by method+bracket
            groups = {}
            for r in all_roots_data:
                key = f"{r['method']} · Bracket [{r['bracket'][0]:.4f}, {r['bracket'][1]:.4f}]"
                if key not in groups:
                    groups[key] = r

            if groups:
                group_tabs = st.tabs([f"Root {i+1}" for i, k in enumerate(groups)])
                for (key, r), gtab in zip(groups.items(), group_tabs):
                    with gtab:
                        st.markdown(f'<div class="info-box">Method: <b>{r["method"]}</b> &nbsp;|&nbsp; Root: <b>x ≈ {r["root"]:.8f}</b> &nbsp;|&nbsp; Final Ea: <b>{r["error"]:.4e}</b></div>', unsafe_allow_html=True)
                        df_rows = pd.DataFrame(r['rows'])
                        st.dataframe(df_rows, use_container_width=True, height=300)

                        # Step-by-step last iteration
                        if r['rows']:
                            last = r['rows'][-1]
                            st.markdown('<div class="formula-box">', unsafe_allow_html=True)
                            step_text = f"Final Iteration #{last.get('Iter','—')}\n"
                            for k2, v in last.items():
                                if k2 != 'Iter':
                                    step_text += f"  {k2:15s} = {v}\n"
                            st.markdown(f'<div class="formula-box">{step_text}</div>', unsafe_allow_html=True)

        # ──── TAB 4: CONVERGENCE CHART ────
        with tabs[3]:
            st.markdown('<div class="sec-title">◈ CONVERGENCE & ERROR ANALYSIS</div>', unsafe_allow_html=True)

            rows_list  = [r['rows'] for r in all_roots_data[:8]]
            labels_list = [f"{r['method'][:8]} x≈{r['root']:.4f}" for r in all_roots_data[:8]]
            conv_fig = make_convergence_chart(rows_list, labels_list)
            st.plotly_chart(conv_fig, use_container_width=True)

            # Error table
            err_data = []
            for r in all_roots_data:
                err_data.append({
                    "Method": r['method'], "Root": round(r['root'], 8),
                    "Final Ea": f"{r['error']:.6e}", "Iterations": r['iterations'],
                    "f(root)": f"{r['f_val']:.6e}",
                    "Converged": "✓ YES" if r['error'] < tol * 100 else "✗ CHECK"
                })
            st.dataframe(pd.DataFrame(err_data), use_container_width=True)

        # ──── TAB 5: COMPARE ALL METHODS ────
        with tabs[4]:
            st.markdown('<div class="sec-title">⊞ MULTI-METHOD COMPARISON</div>', unsafe_allow_html=True)

            # Run all methods fresh for comparison
            ALL_METHODS = ["Bisection Method", "Regula Falsi", "Newton-Raphson Method", "Secant Method", "Incremental Search"]
            _, f2, df2, _ = parse_equation(st.session_state.last_eq)
            if f2:
                brackets2 = scan_brackets(f2, a_range, b_range, n=int(n_scan))
                compare_rows = []
                for m2 in ALL_METHODS:
                    for bk2 in brackets2[:5]:  # limit to 5 brackets for speed
                        xl2, xu2 = bk2
                        root2, ea2, rows2 = solve_root_in_bracket(m2, f2, df2, xl2, xu2, float(tol), int(max_iter))
                        if root2 is not None:
                            compare_rows.append({
                                "Method": m2, "Root": round(root2, 8),
                                "Iterations": len(rows2),
                                "Final Ea": f"{ea2:.4e}" if ea2 else "—",
                                "f(root)": f"{safe_eval(f2, root2):.4e}",
                                "Bracket": f"[{xl2:.3f},{xu2:.3f}]",
                            })

                if compare_rows:
                    st.dataframe(pd.DataFrame(compare_rows), use_container_width=True)

                    # Best method per root (fewest iterations)
                    st.markdown('<div class="sec-title" style="margin-top:1rem;">⊙ METHOD EFFICIENCY RANKING</div>', unsafe_allow_html=True)
                    df_compare = pd.DataFrame(compare_rows)
                    # Group by bracket
                    for bk_str in df_compare["Bracket"].unique():
                        sub = df_compare[df_compare["Bracket"] == bk_str].sort_values("Iterations")
                        st.markdown(f'<div class="compare-label">BRACKET {bk_str}</div>', unsafe_allow_html=True)
                        eff_cols = st.columns(len(sub))
                        for ci, (_, row2) in enumerate(sub.iterrows()):
                            with eff_cols[ci]:
                                rank_col = PLOT_COLORS[ci]
                                st.markdown(f"""
                                    <div class="root-card" style="border-color:{rank_col}44;padding:0.6rem 0.8rem;">
                                        <div class="root-card-num" style="color:{rank_col};">RANK {ci+1}</div>
                                        <div class="root-card-val" style="color:{rank_col};font-size:0.75rem;">{row2['Method']}</div>
                                        <div class="root-card-meta"><span>{row2['Iterations']} iters</span><span>Ea={row2['Final Ea']}</span></div>
                                    </div>
                                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="warn-box">⚠ Could not reparse equation for comparison.</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
            <div class="panel" style="min-height:560px;">
                <div class="placeholder-box">
                    <div class="big-icon">⊛</div>
                    ROOTSOLVER X — READY<br>
                    ────────────────────────────────<br>
                    Configure equation and parameters<br>
                    on the left panel, then press<br>
                    <br>
                    ⊛ SOLVE — FIND ALL ROOTS<br>
                    <br>
                    to automatically detect every root<br>
                    in the specified range.<br>
                    <br>
                    Supports · ln(x) · exp(x) · polynomials<br>
                    · mixed transcendental equations ·
                </div>
            </div>
        """, unsafe_allow_html=True)
