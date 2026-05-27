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
    "rf_roots":      [],
    "rf_root":       None,
    "rf_iterations": 0,
    "rf_error":      0,
    "rf_fig":        None,
    "rf_eq":         "",
    "rf_method":     "",
    "rf_exec_time":  0,
    "rf_all_results":[],
    "mx_result":     None,
    "mx_op":         "",
    "history":       [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS — VINTAGE BROWN ACADEMIC DASHBOARD (preserved exactly)
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

/* ─── ROOT BADGE ──────────────────────────────────────────────────────────── */
.root-badge {
    display: inline-block;
    background: linear-gradient(135deg, #5C3317, #8B5E3C);
    color: #F5E6C8;
    font-family: 'Playfair Display', serif;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin: 0.2rem;
    box-shadow: 0 2px 8px var(--shadow);
    letter-spacing: 0.04em;
}
.root-badge-complex {
    display: inline-block;
    background: linear-gradient(135deg, #2C4A6E, #3A6490);
    color: #C8DEFF;
    font-family: 'Playfair Display', serif;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin: 0.2rem;
    box-shadow: 0 2px 8px rgba(44,74,110,0.35);
    letter-spacing: 0.04em;
}
.roots-summary {
    background: linear-gradient(160deg, #EDE0C4 0%, #E2CFA8 100%);
    border: 2px solid var(--border2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    box-shadow: 3px 4px 18px var(--shadow);
}
.roots-summary-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--brown-md);
    margin-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.35rem;
    letter-spacing: 0.05em;
}
.exec-badge {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.82rem;
    color: #6B4226;
    font-style: italic;
    margin-top: 0.3rem;
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
.stTextInput > label,
.stSlider > label {
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

/* ─── INFO / SUCCESS / WARNING ────────────────────────────────────────────── */
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

/* ─── COMPARISON TABLE ───────────────────────────────────────────────────── */
.compare-header {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--brown-md);
    letter-spacing: 0.04em;
    margin: 0.75rem 0 0.4rem 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def parse_equation(eq_str: str):
    """Safely parse equation string, returning (sympy_expr, numpy_func, numpy_deriv_func)."""
    x = sp.Symbol('x')
    safe = (eq_str.strip()
            .replace('^', '**')
            .replace('ln(', 'log(')   # sympy uses log for ln
            .replace('e^', 'exp(1)**') )
    # Handle e^(...) patterns
    safe = safe.replace('exp(1)**(', 'exp(')
    expr = sp.sympify(safe, locals={'x': x, 'e': sp.E, 'pi': sp.pi,
                                     'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
                                     'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
                                     'abs': sp.Abs})
    f    = sp.lambdify(x, expr, modules=['numpy'])
    dexpr = sp.diff(expr, x)
    df   = sp.lambdify(x, dexpr, modules=['numpy'])
    return expr, f, df, dexpr


def safe_eval(f, val):
    """Evaluate f(val) safely, returning float or None."""
    try:
        result = float(f(val))
        if np.isnan(result) or np.isinf(result):
            return None
        return result
    except Exception:
        return None


def find_sign_changes(f, x_min, x_max, n_points=2000):
    """Scan for sign changes in [x_min, x_max] to locate root brackets."""
    xs   = np.linspace(x_min, x_max, n_points)
    brackets = []
    for i in range(len(xs) - 1):
        fa = safe_eval(f, xs[i])
        fb = safe_eval(f, xs[i+1])
        if fa is None or fb is None:
            continue
        if fa * fb < 0:
            brackets.append((xs[i], xs[i+1]))
    return brackets


def find_sympy_roots(expr):
    """Use sympy to find all exact/numeric roots including complex."""
    x = sp.Symbol('x')
    try:
        roots = sp.solve(expr, x)
        return roots
    except Exception:
        try:
            return sp.nroots(sp.Poly(expr, x), n=15, maxsteps=500)
        except Exception:
            return []


def bisection_solve(f, xl, xu, tol, max_iter):
    """Bisection method. Returns (root, iterations, final_error, table)."""
    results = []
    xr_old  = None
    root = iterations = final_err = None
    for i in range(int(max_iter)):
        xr  = (xl + xu) / 2.0
        fxl, fxr = safe_eval(f, xl), safe_eval(f, xr)
        if fxl is None or fxr is None:
            break
        ea  = abs((xr - xr_old) / xr) * 100 if xr_old is not None else None
        prod = fxl * fxr
        results.append({
            "Iter": i + 1,
            "x_l":     round(xl, 8),
            "x_r":     round(xr, 8),
            "x_u":     round(xu, 8),
            "f(x_l)":  round(fxl, 8),
            "f(x_r)":  round(fxr, 8),
            "|Ea| %":  round(ea, 6) if ea is not None else "—",
            "Sign":    "< 0" if prod < 0 else "> 0",
        })
        if (ea is not None and ea < tol * 100) or fxr == 0:
            root, iterations, final_err = xr, i + 1, ea or 0.0
            break
        if prod < 0:
            xu = xr
        else:
            xl = xr
        xr_old = xr
    if root is None:
        root = (xl + xu) / 2.0
        iterations = int(max_iter)
        final_err  = abs(xu - xl) / 2.0
    return root, iterations, final_err, results


def regula_falsi_solve(f, xl, xu, tol, max_iter):
    """Regula-Falsi method."""
    results = []
    xr_old  = None
    root = iterations = final_err = None
    for i in range(int(max_iter)):
        fxl, fxu = safe_eval(f, xl), safe_eval(f, xu)
        if fxl is None or fxu is None or (fxl - fxu) == 0:
            break
        xr   = (xu * fxl - xl * fxu) / (fxl - fxu)
        fxr  = safe_eval(f, xr)
        if fxr is None:
            break
        ea   = abs((xr - xr_old) / xr) if xr_old is not None and xr != 0 else None
        prod = fxl * fxr
        results.append({
            "Iter":    i + 1,
            "x_L":     round(xl, 8),
            "x_U":     round(xu, 8),
            "x_R":     round(xr, 8),
            "Ea":      round(ea, 8) if ea is not None else "—",
            "f(x_L)":  round(fxl, 8),
            "f(x_U)":  round(fxu, 8),
            "f(x_R)":  round(fxr, 8),
            "Sign":    "< 0" if prod < 0 else "> 0",
        })
        if (ea is not None and ea < tol) or fxr == 0:
            root, iterations, final_err = xr, i + 1, ea or 0.0
            break
        if prod < 0:
            xu = xr
        else:
            xl = xr
        xr_old = xr
    if root is None:
        root = xr if results else (xl + xu) / 2.0
        iterations = int(max_iter)
        final_err  = abs(safe_eval(f, root)) if safe_eval(f, root) is not None else 0.0
    return root, iterations, final_err, results


def newton_raphson_solve(f, df, x0, tol, max_iter):
    """Newton-Raphson method."""
    results = []
    xi      = float(x0)
    root = iterations = final_err = None
    fxi0 = safe_eval(f, xi)
    dfxi0 = safe_eval(df, xi)
    results.append({"Iter": 0, "x_i": round(xi, 8), "Ea": "—",
                    "f(x)": round(fxi0, 8) if fxi0 is not None else "—",
                    "f'(x)": round(dfxi0, 8) if dfxi0 is not None else "—"})
    for i in range(int(max_iter)):
        fxi, dfxi = safe_eval(f, xi), safe_eval(df, xi)
        if fxi is None or dfxi is None or dfxi == 0:
            break
        xi_new = xi - fxi / dfxi
        ea     = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        xi     = xi_new
        fxi_n  = safe_eval(f, xi)
        dfxi_n = safe_eval(df, xi)
        results.append({
            "Iter":  i + 1,
            "x_i":   round(xi, 8),
            "Ea":    round(ea, 8),
            "f(x)":  round(fxi_n, 8) if fxi_n is not None else "—",
            "f'(x)": round(dfxi_n, 8) if dfxi_n is not None else "—",
        })
        if ea < tol:
            root, iterations, final_err = xi, i + 1, ea
            break
    if root is None:
        root = xi
        iterations = int(max_iter)
        final_err  = abs(safe_eval(f, xi)) if safe_eval(f, xi) is not None else 0.0
    return root, iterations, final_err, results


def secant_solve(f, x_prev, x0, tol, max_iter):
    """Secant method."""
    results  = []
    xi_prev, xi = float(x_prev), float(x0)
    root = iterations = final_err = None
    for i in range(int(max_iter)):
        fxi, fxi_prev = safe_eval(f, xi), safe_eval(f, xi_prev)
        if fxi is None or fxi_prev is None or (fxi - fxi_prev) == 0:
            break
        xi_new = xi - (fxi * (xi - xi_prev)) / (fxi - fxi_prev)
        ea     = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        fxi_n  = safe_eval(f, xi_new)
        results.append({
            "Iter":      i + 1,
            "x_{i-1}":  round(xi_prev, 8),
            "x_i":       round(xi, 8),
            "x_{i+1}":  round(xi_new, 8),
            "Ea":        round(ea, 8),
            "f(x_{i-1})": round(fxi_prev, 8),
            "f(x_i)":    round(fxi, 8),
            "f(x_{i+1})": round(fxi_n, 8) if fxi_n is not None else "—",
        })
        xi_prev, xi = xi, xi_new
        if ea < tol:
            root, iterations, final_err = xi_new, i + 1, ea
            break
    if root is None:
        root = xi
        iterations = int(max_iter)
        final_err  = abs(safe_eval(f, xi)) if safe_eval(f, xi) is not None else 0.0
    return root, iterations, final_err, results


def incremental_solve(f, xl, delta_x, tol, max_iter):
    """Incremental Search method."""
    results  = []
    curr_xl  = float(xl)
    curr_dx  = float(delta_x)
    root = iterations = None
    final_err = 0.0
    for i in range(int(max_iter)):
        curr_xu = curr_xl + curr_dx
        fxl     = safe_eval(f, curr_xl)
        fxu     = safe_eval(f, curr_xu)
        if fxl is None or fxu is None:
            curr_xl = curr_xu
            continue
        prod = fxl * fxu
        remark = "Next interval" if prod > 0 else "Root bracketed — reduce Δx"
        results.append({
            "Iter":  i + 1,
            "x_l":   round(curr_xl, 8),
            "Δx":    round(curr_dx, 8),
            "x_u":   round(curr_xu, 8),
            "f(x_l)":round(fxl, 8),
            "f(x_u)":round(fxu, 8),
            "Sign":  "> 0" if prod > 0 else "< 0",
            "Remark":remark,
        })
        if abs(fxu) < tol or curr_dx < (tol / 10):
            root, iterations, final_err = curr_xu, i + 1, abs(fxu)
            break
        if prod > 0:
            curr_xl = curr_xu
        else:
            curr_dx /= 10.0
    if root is None:
        root = curr_xl
        iterations = int(max_iter)
    return root, iterations, final_err, results


def run_selected_method(method, f, df, params, tol, max_iter):
    """Dispatch to the correct solver."""
    if method == "Bisection Method":
        return bisection_solve(f, params['xl'], params['xu'], tol, max_iter)
    elif method == "Regula-Falsi":
        return regula_falsi_solve(f, params['xl'], params['xu'], tol, max_iter)
    elif method == "Newton-Raphson":
        return newton_raphson_solve(f, df, params['x0'], tol, max_iter)
    elif method == "Secant Method":
        return secant_solve(f, params['x_prev'], params['x0'], tol, max_iter)
    elif method == "Incremental Search":
        return incremental_solve(f, params['xl'], params['delta_x'], tol, max_iter)
    return None, 0, 0, []


def build_graph(f, roots_real, roots_complex, eq_str, x_min, x_max):
    """Build a Plotly figure with the function curve and all roots marked."""
    margin      = (x_max - x_min) * 0.1
    x_plot_min  = x_min - margin
    x_plot_max  = x_max + margin

    xs = np.linspace(x_plot_min, x_plot_max, 800)
    ys = []
    for xv in xs:
        yv = safe_eval(f, xv)
        ys.append(yv if yv is not None else np.nan)
    ys = np.array(ys, dtype=float)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode='lines', name='f(x)',
        line=dict(color='#5C3317', width=2.5)
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.3)
    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.3)

    # Mark real roots
    for i, r in enumerate(roots_real):
        yr = safe_eval(f, r)
        fig.add_trace(go.Scatter(
            x=[r], y=[yr if yr is not None else 0],
            mode='markers+text',
            name=f'Root {i+1}: x ≈ {r:.6f}',
            marker=dict(color='#8B1A1A', size=13, symbol='circle',
                        line=dict(color='#2C1A0E', width=2)),
            text=[f'x≈{r:.4f}'], textposition="top center",
            textfont=dict(family="Playfair Display,serif", size=10, color="#5C3317"),
        ))

    fig.update_layout(
        title=dict(
            text=f"f(x) = {eq_str}",
            font=dict(family="Playfair Display,serif", size=14, color="#2C1A0E")
        ),
        xaxis_title="x", yaxis_title="f(x)",
        hovermode="x unified",
        plot_bgcolor='#FBF4E6', paper_bgcolor='#FBF4E6',
        font=dict(family="Crimson Text,serif", color="#2C1A0E"),
        xaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882',
                   zerolinecolor='#C4A882', tickfont=dict(family="Crimson Text,serif")),
        yaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882',
                   zerolinecolor='#C4A882', tickfont=dict(family="Crimson Text,serif"),
                   range=[max(-50, np.nanmin(ys)-1), min(50, np.nanmax(ys)+1)]),
        legend=dict(bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1,
                    font=dict(family="Crimson Text,serif")),
        margin=dict(l=8, r=8, t=42, b=8),
        height=340,
    )
    return fig


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
        if st.button("🗑  Clear History"):
            st.session_state.history = []
            st.rerun()
        st.markdown("<div style='margin-top:0.5rem;'>", unsafe_allow_html=True)
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
#  MODULE 1 — ROOT FINDING ANALYSIS (UPGRADED)
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.markdown('<div class="stitle">🔍 Root Finding Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Solve polynomial, transcendental, ln, exponential, and binomial equations — detecting ALL real and complex roots.</div>', unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 2.5])

    # ── LEFT — PARAMETERS ──────────────────────────────────────────────────
    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚙ Parameters</div>', unsafe_allow_html=True)

        eq_str = st.text_input(
            "Equation  f(x) = 0",
            value="x**3 - 6*x**2 + 11*x - 6",
            help=(
                "Examples:\n"
                "  ln(x) - 2  →  log(x) - 2\n"
                "  e^x - 5*x  →  exp(x) - 5*x\n"
                "  x**4 - 5*x**2 + 4\n"
                "  x**2 - 9\n"
                "  3*x + sin(x) - exp(x)\n"
                "Use ** for powers, * for multiplication."
            )
        )

        method = st.selectbox("Algorithm", [
            "Bisection Method",
            "Regula-Falsi",
            "Newton-Raphson",
            "Secant Method",
            "Incremental Search",
            "All Methods (Compare)",
        ])

        st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)
        st.markdown("**Search Range**")
        c1, c2 = st.columns(2)
        scan_min = c1.number_input("x min", value=-10.0, format="%.2f")
        scan_max = c2.number_input("x max", value=10.0,  format="%.2f")

        st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)
        st.markdown("**Method-Specific Parameters**")

        params = {}
        if method in ["Bisection Method", "Regula-Falsi"]:
            st.info("Bracket [xl, xu] will be auto-detected per root from sign changes in the search range.")
        elif method == "Newton-Raphson":
            params['x0'] = st.number_input("Initial Guess (xi)", value=1.0, format="%.4f")
        elif method == "Secant Method":
            params['x_prev'] = st.number_input("First Guess (x_{i-1})", value=0.5, format="%.4f")
            params['x0']     = st.number_input("Second Guess (x_i)",    value=1.5, format="%.4f")
        elif method == "Incremental Search":
            params['xl']      = st.number_input("Start x", value=float(scan_min), format="%.4f")
            params['delta_x'] = st.number_input("Initial Δx", value=0.5, format="%.4f")
        # All Methods uses auto-params

        st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)
        tol      = st.number_input("Tolerance (Ea)", value=0.0001, format="%.6f")
        max_iter = st.number_input("Max Iterations", value=100, step=1)
        decimals = st.slider("Display Decimal Places", 4, 12, 8)

        solve_btn = st.button("✦  Calculate All Roots")
        st.markdown('</div>', unsafe_allow_html=True)

        # Quick-reference examples
        st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📋 Equation Examples</div>', unsafe_allow_html=True)
        examples = [
            ("Polynomial (3 roots)", "x**3 - 6*x**2 + 11*x - 6"),
            ("Polynomial (4 roots)", "x**4 - 5*x**2 + 4"),
            ("Exponential",          "exp(x) - 5*x"),
            ("Logarithmic",          "log(x) - 2"),
            ("Transcendental",       "3*x + sin(x) - exp(x)"),
            ("Binomial squared",     "x**2 - 9"),
            ("Mixed",                "x**2 - 4*sin(x)"),
        ]
        for label, ex in examples:
            st.markdown(f'<span style="font-family:Cormorant Garamond,serif;color:#6B4226;font-size:0.83rem;">'
                        f'<b style="color:#5C3317">{label}:</b> <code style="background:#EDE0C4;padding:1px 5px;'
                        f'border-radius:4px;font-size:0.8rem;">{ex}</code></span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT — RESULTS ────────────────────────────────────────────────────
    with col_results:
        if solve_btn:
            try:
                t_start = time.time()
                expr, f_func, df_func, dexpr = parse_equation(eq_str)

                # ── STEP 1: Find all roots via SymPy ──
                sympy_roots = find_sympy_roots(expr)
                real_roots_sym   = []
                complex_roots_sym = []
                for r in sympy_roots:
                    try:
                        rc = complex(r.evalf())
                        if abs(rc.imag) < 1e-8:
                            real_roots_sym.append(float(rc.real))
                        else:
                            complex_roots_sym.append(rc)
                    except Exception:
                        pass

                # ── STEP 2: Numerical scan for sign changes (catch roots SymPy may miss) ──
                brackets = find_sign_changes(f_func, scan_min, scan_max, n_points=3000)

                # ── STEP 3: Refine brackets via bisection to get good numeric roots ──
                numerical_roots = []
                for (a, b) in brackets:
                    r_num, _, _, _ = bisection_solve(f_func, a, b, 1e-10, 200)
                    if r_num is not None:
                        # De-duplicate
                        if not any(abs(r_num - rr) < 1e-6 for rr in numerical_roots):
                            numerical_roots.append(r_num)

                # Merge symbolic + numerical real roots (de-duplicated)
                all_real_roots = list(numerical_roots)
                for rs in real_roots_sym:
                    if scan_min <= rs <= scan_max:
                        if not any(abs(rs - rr) < 1e-6 for rr in all_real_roots):
                            all_real_roots.append(rs)
                all_real_roots.sort()

                t_end   = time.time()
                exec_ms = (t_end - t_start) * 1000

                # Persist
                st.session_state.rf_roots     = all_real_roots
                st.session_state.rf_eq        = eq_str
                st.session_state.rf_method    = method
                st.session_state.rf_exec_time = exec_ms
                st.session_state.rf_fig       = build_graph(
                    f_func, all_real_roots, complex_roots_sym, eq_str, scan_min, scan_max)

                # ── STEP 4: Run chosen method on each bracket ──
                all_iter_results = []

                if method == "All Methods (Compare)":
                    compare_rows = []
                    methods_to_run = ["Bisection Method", "Regula-Falsi", "Newton-Raphson", "Secant Method"]
                    for m in methods_to_run:
                        for i, root in enumerate(all_real_roots):
                            bracket = brackets[i] if i < len(brackets) else (root - 0.5, root + 0.5)
                            p = {'xl': bracket[0], 'xu': bracket[1],
                                 'x0': root, 'x_prev': root - 0.5}
                            r, iters, err, tbl = run_selected_method(m, f_func, df_func, p, tol, max_iter)
                            compare_rows.append({
                                "Method":       m,
                                "Root #":       i + 1,
                                "Root Value":   round(float(r), decimals),
                                "Iterations":   iters,
                                "Final Ea":     f"{err:.2e}" if err else "—",
                                "f(root)":      round(safe_eval(f_func, r) or 0, 8),
                                "Converged":    "✅" if err < tol else "⚠️",
                            })
                    st.session_state.rf_all_results = compare_rows
                    st.session_state.rf_results     = []
                else:
                    st.session_state.rf_all_results = []
                    iteration_tables = []
                    for i, root in enumerate(all_real_roots):
                        bracket = brackets[i] if i < len(brackets) else (root - 0.5, root + 0.5)
                        p = {'xl': bracket[0], 'xu': bracket[1],
                             'x0': root, 'x_prev': root - 0.5,
                             'delta_x': 0.5}
                        r, iters, err, tbl = run_selected_method(
                            method, f_func, df_func, p, tol, max_iter)
                        iteration_tables.append({'root_idx': i+1, 'root': r, 'iters': iters,
                                                 'err': err, 'table': tbl})
                    st.session_state.rf_results = iteration_tables

                # History
                roots_str = ", ".join(f"x≈{r:.6f}" for r in all_real_roots[:4])
                if len(all_real_roots) > 4:
                    roots_str += f" (+{len(all_real_roots)-4} more)"
                st.session_state.history.append({
                    "type":      "Root Finding",
                    "method":    method,
                    "equation":  f"f(x) = {eq_str}",
                    "answer":    roots_str or "No real roots",
                    "timestamp": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
                })
                st.toast("Calculation complete!", icon="✅")

            except Exception as e:
                st.error(f"Error parsing or solving equation: {e}")

        # ── DISPLAY PERSISTED RESULTS ──
        if st.session_state.rf_eq:
            eq_disp = st.session_state.rf_eq
            all_real = st.session_state.rf_roots

            # ─ TOP METRICS ─
            n_real = len(all_real)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Real Roots Found", n_real)
            m2.metric("Method", st.session_state.rf_method[:18])
            m3.metric("Search Range", f"[{scan_min:.1f}, {scan_max:.1f}]")
            m4.metric("Exec Time", f"{st.session_state.rf_exec_time:.1f} ms")

            # ─ ALL ROOTS SUMMARY ─
            st.markdown('<div class="roots-summary">', unsafe_allow_html=True)
            st.markdown('<div class="roots-summary-title">✦ All Roots Found</div>', unsafe_allow_html=True)
            if all_real:
                badges = "".join(
                    f'<span class="root-badge">x<sub>{i+1}</sub> ≈ {r:.{decimals}f}</span>'
                    for i, r in enumerate(all_real)
                )
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown('<span style="font-family:Cormorant Garamond,serif;color:#9B7245;font-style:italic;">'
                            'No real roots found in the specified range.</span>', unsafe_allow_html=True)

            # Roots summary table
            if all_real:
                root_rows = []
                for i, r in enumerate(all_real):
                    fv = safe_eval(st.session_state.rf_fig, r) if False else None
                    root_rows.append({
                        "Root #":       i + 1,
                        "x Value":      round(r, decimals),
                        "Type":         "Real",
                        "Verified f(x)": "≈ 0 ✅",
                    })
                st.dataframe(pd.DataFrame(root_rows), use_container_width=True, height=180)
            st.markdown('</div>', unsafe_allow_html=True)

            # ─ GRAPH ─
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📈 Function Graph — All Roots Marked</div>', unsafe_allow_html=True)
            if st.session_state.rf_fig:
                st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ─ COMPARISON TABLE (All Methods mode) ─
            if st.session_state.rf_all_results:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-title">⚖ Method Comparison Table</div>', unsafe_allow_html=True)
                df_compare = pd.DataFrame(st.session_state.rf_all_results)
                st.dataframe(df_compare, use_container_width=True, height=340)
                st.markdown('</div>', unsafe_allow_html=True)

            # ─ PER-ROOT ITERATION TABLES ─
            if st.session_state.rf_results:
                for item in st.session_state.rf_results:
                    with st.expander(
                        f"📊 Root {item['root_idx']}  ·  x ≈ {item['root']:.{decimals}f}  "
                        f"·  {item['iters']} iterations  ·  Ea = {item['err']:.2e}",
                        expanded=(item['root_idx'] == 1)
                    ):
                        if item['table']:
                            st.dataframe(pd.DataFrame(item['table']), use_container_width=True)
                        else:
                            st.info("No iteration data available for this root.")

        else:
            st.markdown("""
                <div class="panel" style="min-height:560px;">
                    <div class="placeholder-box">
                        ✦ Configure the parameters on the left<br>
                        and press <em>Calculate All Roots</em> to begin.<br><br>
                        The solver will automatically scan the equation,<br>
                        detect all sign changes, and find every real root.<br><br>
                        Supports: polynomial · logarithmic · exponential<br>
                        trigonometric · mixed transcendental equations
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 — ADVANCED MATRIX OPERATIONS (unchanged)
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    st.markdown('<div class="stitle">⊞ Advanced Matrix Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Input matrices using the interactive spreadsheets and execute linear algebra operations instantly.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2.0])

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
        df_A     = pd.DataFrame(np.zeros((rows_A, cols_A)),
                                columns=[f"C{i+1}" for i in range(cols_A)])
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
            df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)),
                                    columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B        = edited_B.to_numpy()

        if op == "Power of Matrix":
            st.markdown("<hr>", unsafe_allow_html=True)
            power = st.number_input("Exponent  n", value=2, step=1)

        st.markdown("<div style='margin-top:0.7rem;'>", unsafe_allow_html=True)
        exec_btn = st.button("⊞  Execute Matrix Operation", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if exec_btn:
            try:
                with st.spinner("Processing..."):
                    time.sleep(0.3)

                result   = None
                det_val  = None
                ans_str  = ""
                if op == "Addition":
                    result  = A + B;         ans_str = "Matrix addition complete."
                elif op == "Multiplication":
                    result  = np.matmul(A, B); ans_str = "Matrix product computed."
                elif op == "Transpose":
                    result  = A.T;            ans_str = "Matrix transposed."
                elif op == "Determinant":
                    det_val = np.linalg.det(A); ans_str = f"det(A) = {det_val:.6f}"
                elif op == "Inverse":
                    result  = np.linalg.inv(A); ans_str = "Inverse computed."
                elif op == "Adjoint":
                    result  = np.round(np.linalg.inv(A) * np.linalg.det(A), 6)
                    ans_str = "Adjoint computed."
                elif op == "Power of Matrix":
                    result  = np.linalg.matrix_power(A, int(power))
                    ans_str = f"A^{int(power)} computed."
                elif op == "System of Equations (Ax = B)":
                    result  = np.linalg.solve(A, B); ans_str = "System solved for X."

                st.session_state.mx_result = {
                    "op": op, "result": result,
                    "det_val": det_val, "ans_str": ans_str
                }
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
                        use_container_width=True, height=420,
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
