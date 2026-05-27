import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

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
    "rf_all_roots":  [],
    "rf_iterations": 0,
    "rf_error":      0,
    "rf_fig":        None,
    "rf_eq":         "",
    "rf_method":     "",
    "rf_summary":    [],
    "mx_result":     None,
    "mx_op":         "",
    "history":       [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS — VINTAGE BROWN ACADEMIC DASHBOARD (UNCHANGED)
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

/* ─── ROOT SUMMARY TABLE ─────────────────────────────────────────────────── */
.root-summary-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.6rem;
    background: rgba(196,168,130,0.18);
    border-radius: 6px;
    margin-bottom: 0.35rem;
    font-family: 'Crimson Text', serif;
    font-size: 0.92rem;
    color: var(--brown-dk);
}
.root-badge {
    background: var(--brown-md);
    color: #F5E6C8;
    border-radius: 50%;
    width: 22px; height: 22px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ENHANCED EQUATION PARSER & SAFE EVALUATOR
# ══════════════════════════════════════════════════════════════════════════════

def parse_equation(eq_str: str):
    """
    Parse equation string to sympy expression with full support for:
    ln, log, exp, e^x, trig, polynomials, binomials, implicit multiplication.
    Returns (sympy_expr, lambdified_f, lambdified_df) or raises.
    """
    x = sp.Symbol('x')

    # Preprocessing
    s = eq_str.strip()
    s = s.replace('^', '**')                      # ^ → **
    s = s.replace('e**x', 'exp(x)')               # common shorthand
    # Implicit multiplication: e.g. 2x → 2*x, (x+1)(x-2) → (x+1)*(x-2)
    import re
    s = re.sub(r'(\d)(x)', r'\1*\2', s)           # 3x → 3*x
    s = re.sub(r'(x)(\d)', r'\1*\2', s)           # x3 → x*3 (rare)
    s = re.sub(r'\)(\()', r')*(', s)              # )(  → )*(
    s = re.sub(r'(\d)\(', r'\1*(', s)             # 2( → 2*(
    # ln → log in sympy
    s = re.sub(r'\bln\b', 'log', s)

    local_dict = {
        'x': x, 'pi': sp.pi, 'e': sp.E,
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
        'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
        'exp': sp.exp, 'log': sp.log, 'log10': lambda a: sp.log(a, 10),
        'sqrt': sp.sqrt, 'Abs': sp.Abs, 'abs': sp.Abs,
    }

    expr = sp.sympify(s, locals=local_dict, evaluate=True)
    f_sym  = expr
    df_sym = sp.diff(expr, x)

    # Create safe numpy lambdify with domain protection
    modules = ['numpy', {'log': np.log, 'exp': np.exp, 'sqrt': np.sqrt,
                          'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                          'asin': np.arcsin, 'acos': np.arccos, 'atan': np.arctan,
                          'Abs': np.abs}]

    f_raw  = sp.lambdify(x, f_sym,  modules)
    df_raw = sp.lambdify(x, df_sym, modules)

    def f_safe(val):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = f_raw(val)
                if np.isscalar(result):
                    return float(result) if np.isfinite(result) else np.nan
                arr = np.array(result, dtype=float)
                arr[~np.isfinite(arr)] = np.nan
                return arr
        except Exception:
            if np.isscalar(val):
                return np.nan
            return np.full(np.shape(val), np.nan)

    def df_safe(val):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = df_raw(val)
                if np.isscalar(result):
                    return float(result) if np.isfinite(result) else np.nan
                arr = np.array(result, dtype=float)
                arr[~np.isfinite(arr)] = np.nan
                return arr
        except Exception:
            return np.nan if np.isscalar(val) else np.full(np.shape(val), np.nan)

    return expr, f_safe, df_safe


# ══════════════════════════════════════════════════════════════════════════════
#  INTERVAL SCANNER — find ALL bracketing intervals
# ══════════════════════════════════════════════════════════════════════════════

def scan_for_brackets(f, x_start, x_end, step=0.5):
    """
    Scan [x_start, x_end] with given step size.
    Returns list of (a, b) pairs where sign change occurs (potential roots).
    Handles domain gaps (NaN) gracefully.
    """
    brackets = []
    pts = np.arange(x_start, x_end + step * 0.01, step)
    vals = np.array([f(p) for p in pts], dtype=float)

    last_valid_i = None
    for i in range(len(pts)):
        if not np.isfinite(vals[i]):
            last_valid_i = None
            continue
        if last_valid_i is not None:
            a, b = pts[last_valid_i], pts[i]
            fa, fb = vals[last_valid_i], vals[i]
            if fa * fb < 0:
                brackets.append((a, b))
            elif abs(fa) < 1e-10:  # direct root near a
                # Already captured or will be captured elsewhere
                pass
        last_valid_i = i

    return brackets


def deduplicate_roots(roots, tol=1e-6):
    """Remove duplicate roots that are closer than tol."""
    if not roots:
        return []
    sorted_r = sorted(roots, key=lambda r: r[0])
    deduped = [sorted_r[0]]
    for r in sorted_r[1:]:
        if abs(r[0] - deduped[-1][0]) > tol:
            deduped.append(r)
    return deduped


# ══════════════════════════════════════════════════════════════════════════════
#  NUMERICAL METHOD SOLVERS (upgraded — multi-root aware, domain-safe)
# ══════════════════════════════════════════════════════════════════════════════

def solve_bisection(f, a, b, tol, max_iter):
    results = []
    xr_old  = None
    root    = None
    final_err = 0.0

    for i in range(int(max_iter)):
        xr  = (a + b) / 2.0
        fxl = f(a); fxr = f(xr)

        if not (np.isfinite(fxl) and np.isfinite(xr)):
            break

        ea  = abs((xr - xr_old) / xr) * 100 if xr_old is not None and xr != 0 else None
        prod = fxl * fxr

        results.append({
            "Iter": i + 1,
            "x_l":     round(float(a),  8),
            "x_r":     round(float(xr), 8),
            "x_u":     round(float(b),  8),
            "f(x_l)":  round(float(fxl), 8),
            "f(x_r)":  round(float(fxr), 8),
            "|E_a| %": round(ea, 6) if ea is not None else "",
            "Sign(f_l·f_r)": "< 0" if prod < 0 else ("> 0" if prod > 0 else "= 0"),
            "Remark":  "1st sub-interval" if prod < 0 else "2nd sub-interval",
        })

        if fxr == 0 or (ea is not None and ea < tol):
            root, final_err = xr, ea or 0.0
            break

        if prod < 0:
            b = xr
        else:
            a = xr
        xr_old = xr

    if root is None and results:
        root = results[-1]["x_r"]
        final_err = results[-1]["|E_a| %"] or 0.0

    return root, len(results), final_err, results


def solve_regula_falsi(f, a, b, tol, max_iter):
    results  = []
    xr_old   = None
    root     = None
    final_err = 0.0

    for i in range(int(max_iter)):
        fxl = f(a); fxu = f(b)
        denom = fxl - fxu
        if not np.isfinite(denom) or abs(denom) < 1e-15:
            break

        xr  = (b * fxl - a * fxu) / denom
        fxr = f(xr)

        if not np.isfinite(xr) or not np.isfinite(fxr):
            break

        ea   = abs((xr - xr_old) / xr) if (xr_old is not None and xr != 0) else None
        prod = fxl * fxr

        results.append({
            "Iter":      i + 1,
            "x_L":       round(float(a),   8),
            "x_U":       round(float(b),   8),
            "x_R":       round(float(xr),  8),
            "E_a":       round(float(ea),  8) if ea is not None else "",
            "f(x_L)":    round(float(fxl), 8),
            "f(x_U)":    round(float(fxu), 8),
            "f(x_R)":    round(float(fxr), 8),
            "f(xL)·f(xR)": "< 0" if prod < 0 else "> 0",
        })

        if (ea is not None and ea < tol) or abs(fxr) < 1e-12:
            root, final_err = xr, float(ea) if ea else 0.0
            break

        if prod < 0:
            b = xr
        else:
            a = xr
        xr_old = xr

    if root is None and results:
        root = results[-1]["x_R"]
        final_err = results[-1]["E_a"] if results[-1]["E_a"] != "" else 0.0

    return root, len(results), final_err, results


def solve_newton_raphson(f, df, x0, tol, max_iter):
    results   = []
    xi        = float(x0)
    root      = None
    final_err = 0.0

    fxi = f(xi); dfxi = df(xi)
    results.append({
        "Iter":   0,
        "x_i":    round(xi, 8),
        "E_a":    "",
        "f(x)":   round(float(fxi),  8) if np.isfinite(fxi)  else "NaN",
        "f'(x)":  round(float(dfxi), 8) if np.isfinite(dfxi) else "NaN",
    })

    for i in range(int(max_iter)):
        fxi  = f(xi)
        dfxi = df(xi)

        if not (np.isfinite(fxi) and np.isfinite(dfxi)):
            break
        if abs(dfxi) < 1e-14:
            break

        xi_new = xi - fxi / dfxi
        if not np.isfinite(xi_new):
            break

        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)

        xi = xi_new
        results.append({
            "Iter":   i + 1,
            "x_i":    round(float(xi),  8),
            "E_a":    round(float(ea),  8),
            "f(x)":   round(float(f(xi)),  8) if np.isfinite(f(xi))  else "NaN",
            "f'(x)":  round(float(df(xi)), 8) if np.isfinite(df(xi)) else "NaN",
        })

        if ea < tol:
            root, final_err = xi, float(ea)
            break

    if root is None and len(results) > 1:
        root = results[-1]["x_i"]
        final_err = results[-1]["E_a"] if results[-1]["E_a"] != "" else 0.0

    return root, max(0, len(results) - 1), final_err, results


def solve_secant(f, x_prev, x0, tol, max_iter):
    results   = []
    xi_prev   = float(x_prev)
    xi        = float(x0)
    root      = None
    final_err = 0.0

    for i in range(int(max_iter)):
        fxi      = f(xi)
        fxi_prev = f(xi_prev)

        if not (np.isfinite(fxi) and np.isfinite(fxi_prev)):
            break
        denom = fxi - fxi_prev
        if abs(denom) < 1e-14:
            break

        xi_new = xi - (fxi * (xi - xi_prev)) / denom
        if not np.isfinite(xi_new):
            break

        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)

        results.append({
            "Iter":        i + 1,
            "x_{i-1}":    round(float(xi_prev), 8),
            "x_i":        round(float(xi),      8),
            "x_{i+1}":   round(float(xi_new),  8),
            "E_a":        round(float(ea),      8),
            "f(x_{i-1})": round(float(fxi_prev), 8),
            "f(x_i)":     round(float(fxi),      8),
            "f(x_{i+1})": round(float(f(xi_new)),8) if np.isfinite(f(xi_new)) else "NaN",
        })

        xi_prev, xi = xi, xi_new

        if ea < tol:
            root, final_err = xi_new, float(ea)
            break

    if root is None and results:
        root = results[-1]["x_{i+1}"]
        final_err = results[-1]["E_a"] if results[-1]["E_a"] != "" else 0.0

    return root, len(results), final_err, results


def solve_incremental(f, xl, delta_x, tol, max_iter):
    """Incremental search: returns all found brackets + detailed table."""
    results  = []
    curr_xl  = float(xl)
    curr_dx  = float(delta_x)
    root     = None
    final_err = 0.0

    for i in range(int(max_iter)):
        curr_xu = curr_xl + curr_dx
        fxl = f(curr_xl); fxu = f(curr_xu)

        if not (np.isfinite(fxl) and np.isfinite(fxu)):
            curr_xl = curr_xu
            continue

        prod  = fxl * fxu
        remark = "Go to next interval" if prod > 0 else "Root bracketed — reduce interval"

        results.append({
            "Iter":          i + 1,
            "x_l":           round(float(curr_xl),  8),
            "Δx":            round(float(curr_dx),  8),
            "x_u":           round(float(curr_xu),  8),
            "f(x_l)":        round(float(fxl),      8),
            "f(x_u)":        round(float(fxu),      8),
            "f(xl)·f(xu)":   "> 0" if prod > 0 else "< 0",
            "Remark":        remark,
        })

        if abs(fxu) < tol or curr_dx < tol / 100:
            root, final_err = curr_xu, abs(fxu)
            break

        if prod > 0:
            curr_xl = curr_xu
        else:
            curr_dx /= 10.0

    if root is None and results:
        root = results[-1]["x_u"]
        final_err = abs(f(root)) if np.isfinite(f(root)) else 0.0

    return root, len(results), final_err, results


# ══════════════════════════════════════════════════════════════════════════════
#  MULTI-ROOT SOLVER — orchestrates scanning + per-bracket method calls
# ══════════════════════════════════════════════════════════════════════════════

def solve_all_roots(f, df, method, x_start, x_end, scan_step,
                    tol, max_iter,
                    x0=None, x_prev=None, xl_single=None, xu_single=None,
                    delta_x=0.5):
    """
    1. Scan [x_start, x_end] for sign-change brackets.
    2. Apply chosen method to each bracket.
    3. Return list of (root, iters, error, table) tuples.
    """
    brackets = scan_for_brackets(f, x_start, x_end, step=scan_step)

    all_root_data = []

    for (a, b) in brackets:
        try:
            if method == "Bisection Method":
                root, iters, err, tbl = solve_bisection(f, a, b, tol, max_iter)
            elif method == "Regula-Falsi":
                root, iters, err, tbl = solve_regula_falsi(f, a, b, tol, max_iter)
            elif method == "Newton-Raphson":
                midpoint = (a + b) / 2.0
                root, iters, err, tbl = solve_newton_raphson(f, df, midpoint, tol, max_iter)
            elif method == "Secant Method":
                root, iters, err, tbl = solve_secant(f, a, b, tol, max_iter)
            elif method == "Incremental Search":
                root, iters, err, tbl = solve_incremental(f, a, delta_x, tol, max_iter)
            else:
                continue

            if root is not None and np.isfinite(root):
                fval = f(root)
                if np.isfinite(fval) and abs(fval) < max(tol * 100, 1e-4):
                    all_root_data.append({
                        "root": float(root),
                        "iters": iters,
                        "error": err,
                        "table": tbl,
                        "bracket": (a, b),
                        "fval": float(fval),
                    })
        except Exception:
            continue

    # Deduplicate
    deduped = []
    seen = []
    for rd in all_root_data:
        is_dup = any(abs(rd["root"] - s) < max(tol * 10, 1e-5) for s in seen)
        if not is_dup:
            deduped.append(rd)
            seen.append(rd["root"])

    return sorted(deduped, key=lambda r: r["root"])


# ══════════════════════════════════════════════════════════════════════════════
#  GRAPH BUILDER — auto-scale, all roots, domain-aware
# ══════════════════════════════════════════════════════════════════════════════

VINTAGE_COLORS = [
    '#8B1A1A', '#1A5C8B', '#2E7D32', '#6B3A6B',
    '#B8600A', '#2C5C5C', '#7A4F2E', '#1E5C1E',
]

def build_graph(f, eq_str, roots_data, x_start, x_end):
    """Build full vintage-themed Plotly figure showing entire function + all roots."""
    # Dense x grid for smooth rendering
    N = 1000
    raw_x = np.linspace(x_start, x_end, N)
    raw_y = np.array([f(xi) for xi in raw_x], dtype=float)

    # Clip extreme values for display (don't let asymptotes dominate)
    valid_y = raw_y[np.isfinite(raw_y)]
    if len(valid_y) == 0:
        st.warning("No finite values found in the scanning interval.")
        return None

    y_med  = np.nanmedian(valid_y)
    y_std  = np.nanstd(valid_y)
    y_clip = max(abs(y_med) + 5 * y_std, 20.0)
    display_y = np.where(np.isfinite(raw_y), np.clip(raw_y, -y_clip, y_clip), np.nan)

    fig = go.Figure()

    # Split into segments at NaN gaps for proper discontinuity rendering
    segs_x, segs_y = [], []
    sx, sy = [], []
    for xi, yi in zip(raw_x, display_y):
        if np.isnan(yi):
            if sx:
                segs_x.append(sx); segs_y.append(sy)
                sx, sy = [], []
        else:
            sx.append(xi); sy.append(yi)
    if sx:
        segs_x.append(sx); segs_y.append(sy)

    first_trace = True
    for sx, sy in segs_x:
        fig.add_trace(go.Scatter(
            x=sx, y=sy, mode='lines',
            name='f(x)' if first_trace else None,
            showlegend=first_trace,
            line=dict(color='#5C3317', width=2.5),
            hovertemplate='x=%{x:.5f}<br>f(x)=%{y:.5f}<extra></extra>',
        ))
        first_trace = False

    # Zero axes
    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.2)
    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.2)

    # Root markers
    for idx, rd in enumerate(roots_data):
        r = rd["root"]
        color = VINTAGE_COLORS[idx % len(VINTAGE_COLORS)]
        fig.add_trace(go.Scatter(
            x=[r], y=[0],
            mode='markers+text',
            name=f'Root {idx+1}: x≈{r:.5f}',
            marker=dict(color=color, size=13, symbol='circle',
                        line=dict(color='#2C1A0E', width=2)),
            text=[f' x≈{r:.4f}'],
            textposition='top right',
            textfont=dict(family='Playfair Display, serif', size=11, color=color),
            hovertemplate=f'Root {idx+1}<br>x = {r:.8f}<br>f(x) ≈ {rd["fval"]:.2e}<extra></extra>',
        ))

    # Auto y-range: show roots + some function context
    visible_ys = [yi for yi in display_y if np.isfinite(yi)]
    y_lo = min(visible_ys) * 1.1 if visible_ys else -10
    y_hi = max(visible_ys) * 1.1 if visible_ys else 10

    fig.update_layout(
        title=dict(
            text=f"f(x) = {eq_str}",
            font=dict(family="Playfair Display,serif", size=14, color="#2C1A0E"),
        ),
        xaxis_title="x", yaxis_title="f(x)",
        hovermode="x unified",
        plot_bgcolor='#FBF4E6', paper_bgcolor='#FBF4E6',
        font=dict(family="Crimson Text,serif", color="#2C1A0E"),
        xaxis=dict(
            gridcolor='#E2CFA8', linecolor='#C4A882',
            zerolinecolor='#C4A882',
            tickfont=dict(family="Crimson Text,serif"),
            range=[x_start, x_end],
        ),
        yaxis=dict(
            gridcolor='#E2CFA8', linecolor='#C4A882',
            zerolinecolor='#C4A882',
            tickfont=dict(family="Crimson Text,serif"),
            range=[y_lo, y_hi],
        ),
        legend=dict(
            bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1,
            font=dict(family="Crimson Text,serif"),
            orientation='v', x=1.01, xanchor='left',
        ),
        margin=dict(l=8, r=10, t=45, b=8),
        height=370,
    )

    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — CALCULATION HISTORY
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
    st.markdown('<div class="ssub">Automatically scan the full interval, detect all real roots, and solve using your chosen numerical method.</div>', unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 2.5])

    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚙ Parameters</div>', unsafe_allow_html=True)

        eq_str = st.text_input(
            "Equation  f(x)",
            value="3*x + sin(x) - exp(x)",
            help=(
                "Supports: ln(x), log(x), exp(x), e^x, sin/cos/tan, polynomials, "
                "binomials like (x+2)(x-4), mixed equations. Use ^ or ** for powers."
            )
        )

        method = st.selectbox("Algorithm", [
            "Bisection Method",
            "Regula-Falsi",
            "Newton-Raphson",
            "Secant Method",
            "Incremental Search",
        ])

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**🔭 Automatic Interval Scanning**", unsafe_allow_html=False)

        sc1, sc2 = st.columns(2)
        x_start = sc1.number_input("Scan Start", value=-10.0, format="%.2f")
        x_end   = sc2.number_input("Scan End",   value=10.0,  format="%.2f")
        scan_step = st.number_input(
            "Scan Step Size",
            value=0.5, min_value=0.001, max_value=10.0, format="%.4f",
            help="Smaller step = more roots detected but slower. 0.1–0.5 recommended."
        )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Method Parameters**")

        if method == "Incremental Search":
            xl_in = st.number_input("Initial Value (xl)", value=float(x_start), format="%.4f")
            delta_x_in = st.number_input("Initial Δx", value=0.5, format="%.4f")
        elif method in ["Bisection Method", "Regula-Falsi"]:
            xl_in = st.number_input("Override Lower Bound (optional)", value=float(x_start), format="%.4f",
                                    help="Used only if no brackets are auto-detected. Otherwise auto-brackets are used.")
            xu_in = st.number_input("Override Upper Bound (optional)", value=float(x_end), format="%.4f")
        elif method == "Newton-Raphson":
            x0_in = st.number_input(
                "Initial Guess (used per-bracket midpoint by default)", value=1.0, format="%.4f",
                help="The solver uses bracket midpoints automatically for multi-root detection."
            )
        elif method == "Secant Method":
            x_prev_in = st.number_input("First Guess Override", value=float(x_start), format="%.4f")
            x0_in     = st.number_input("Second Guess Override", value=float(x_end),  format="%.4f")

        tol      = st.number_input("Tolerance", value=0.0001, format="%.6f", min_value=1e-10)
        max_iter = st.number_input("Max Iterations", value=100, step=1, min_value=5, max_value=5000)

        solve_btn = st.button("🔍  Calculate All Roots")
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── RESULTS COLUMN ───────────────────────────────────────────────────────
    with col_results:

        if solve_btn:
            try:
                expr, f, df = parse_equation(eq_str)

                # Build kwargs for specific methods
                kwargs = dict(
                    delta_x=delta_x_in if method == "Incremental Search" else 0.5,
                )

                with st.spinner("Scanning interval and solving..."):
                    roots_data = solve_all_roots(
                        f, df, method,
                        x_start=float(x_start),
                        x_end=float(x_end),
                        scan_step=float(scan_step),
                        tol=float(tol),
                        max_iter=int(max_iter),
                        **kwargs,
                    )

                # If no roots via scan, fall back to direct user bounds
                if not roots_data:
                    if method in ["Bisection Method", "Regula-Falsi"]:
                        fa, fb = f(xl_in), f(xu_in)
                        if np.isfinite(fa) and np.isfinite(fb) and fa * fb < 0:
                            if method == "Bisection Method":
                                root, iters, err, tbl = solve_bisection(f, xl_in, xu_in, tol, max_iter)
                            else:
                                root, iters, err, tbl = solve_regula_falsi(f, xl_in, xu_in, tol, max_iter)
                            if root is not None:
                                roots_data = [{"root": root, "iters": iters, "error": err,
                                               "table": tbl, "bracket": (xl_in, xu_in),
                                               "fval": float(f(root))}]
                    elif method == "Newton-Raphson":
                        root, iters, err, tbl = solve_newton_raphson(f, df, x0_in, tol, max_iter)
                        if root is not None:
                            roots_data = [{"root": root, "iters": iters, "error": err,
                                           "table": tbl, "bracket": (x0_in, x0_in),
                                           "fval": float(f(root))}]
                    elif method == "Secant Method":
                        root, iters, err, tbl = solve_secant(f, x_prev_in, x0_in, tol, max_iter)
                        if root is not None:
                            roots_data = [{"root": root, "iters": iters, "error": err,
                                           "table": tbl, "bracket": (x_prev_in, x0_in),
                                           "fval": float(f(root))}]

                # Build graph
                fig = build_graph(f, eq_str, roots_data, float(x_start), float(x_end))

                # Summary table
                summary = []
                for idx, rd in enumerate(roots_data):
                    summary.append({
                        "Root #":          idx + 1,
                        "Approx. Root":    round(rd["root"],  8),
                        "f(root)":         f"{rd['fval']:.3e}",
                        "Error (E_a)":     f"{rd['error']:.3e}" if rd["error"] else "—",
                        "Method":          method,
                        "Iterations":      rd["iters"],
                    })

                # Persist
                primary_root = roots_data[0]["root"] if roots_data else None
                primary_err  = roots_data[0]["error"] if roots_data else 0.0
                primary_iters = roots_data[0]["iters"] if roots_data else 0

                st.session_state.rf_results    = roots_data[0]["table"] if roots_data else []
                st.session_state.rf_root       = primary_root
                st.session_state.rf_all_roots  = roots_data
                st.session_state.rf_iterations = primary_iters
                st.session_state.rf_error      = primary_err
                st.session_state.rf_fig        = fig
                st.session_state.rf_eq         = eq_str
                st.session_state.rf_method     = method
                st.session_state.rf_summary    = summary

                # History
                roots_str = ", ".join([f"x≈{rd['root']:.5f}" for rd in roots_data]) if roots_data else "None found"
                st.session_state.history.append({
                    "type":      "Root Finding",
                    "method":    method,
                    "equation":  f"f(x) = {eq_str}",
                    "answer":    roots_str,
                    "timestamp": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
                })

                if roots_data:
                    st.toast(f"✅  {len(roots_data)} root(s) found!", icon="✅")
                else:
                    st.toast("⚠️  No roots detected in the interval.", icon="⚠️")

            except Exception as e:
                st.error(f"**Parse / Solve Error:** {e}\n\nTip: Check your equation syntax. Use `*` for multiplication, `**` or `^` for powers, `ln(x)`, `exp(x)`, `sin(x)` etc.")

        # ── DISPLAY PERSISTED RESULTS ──────────────────────────────────────────
        if st.session_state.rf_root is not None:
            all_roots = st.session_state.rf_all_roots

            # METRICS ROW
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Primary Root",     f"{st.session_state.rf_root:.8f}")
            m2.metric("Roots Found",      len(all_roots))
            m3.metric("Iterations (1st)", st.session_state.rf_iterations)
            m4.metric("Error (E_a)",
                      f"{st.session_state.rf_error:.3e}" if st.session_state.rf_error else "—")

            # ROOT SUMMARY PANEL
            if st.session_state.rf_summary:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-title">✦ Root Summary</div>', unsafe_allow_html=True)
                df_summary = pd.DataFrame(st.session_state.rf_summary)
                st.dataframe(df_summary, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # GRAPH
            if st.session_state.rf_fig:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-title">📈 Function Graph — All Roots</div>', unsafe_allow_html=True)
                st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ITERATION TABLES (one per root, collapsible)
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📊 Iteration Tables</div>', unsafe_allow_html=True)
            for idx, rd in enumerate(all_roots):
                with st.expander(f"Root {idx+1}: x ≈ {rd['root']:.8f}   (bracket [{rd['bracket'][0]:.4f}, {rd['bracket'][1]:.4f}])", expanded=(idx == 0)):
                    st.dataframe(pd.DataFrame(rd["table"]), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
                <div class="panel" style="min-height:520px;">
                    <div class="placeholder-box">
                        ✦ Configure the parameters on the left<br>
                        and press <em>Calculate All Roots</em> to begin.<br><br>
                        The solver will automatically scan the full interval,<br>
                        detect every root, and display the iteration tables<br>
                        and complete function graph here.
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 — ADVANCED MATRIX OPERATIONS (UNCHANGED)
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
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if exec_btn:
            try:
                with st.spinner("Processing..."):
                    time.sleep(0.35)

                result  = None
                ans_str = ""
                det_val = None

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

                st.session_state.mx_result = {
                    "op": op, "result": result,
                    "det_val": det_val,
                    "ans_str": ans_str,
                }
                st.session_state.mx_op = op

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
