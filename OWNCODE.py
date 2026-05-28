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
    "rf_iterations": 0,
    "rf_error":      0,
    "rf_fig":        None,
    "rf_eq":         "",
    "rf_method":     "",
    "rf_all_roots":  [],
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

.nav-strip {
    background: linear-gradient(135deg, #EDE0C4 0%, #E2D0AA 50%, #EDE0C4 100%);
    border: 1.5px solid var(--border);
    border-radius: 11px;
    padding: 0.6rem 1.3rem 0.45rem 1.3rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 2px 12px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.45);
}

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

hr {
    border: none !important;
    border-top: 1.5px solid var(--border) !important;
    margin: 0.6rem 0 !important;
}

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

.placeholder-box {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #9B7245;
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-style: italic;
    line-height: 1.7;
}

.root-summary-card {
    background: linear-gradient(135deg, #EDE0C4, #E2CFA8);
    border: 1.5px solid var(--border2);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.45rem;
    box-shadow: 2px 3px 11px var(--shadow);
    display: flex;
    align-items: center;
    gap: 0.9rem;
}
.root-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #8B1A1A;
    min-width: 28px;
}
.root-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--brown-dk);
    flex: 1;
}
.root-meta {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.82rem;
    color: #6B4226;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ENHANCED EQUATION PARSER
# ══════════════════════════════════════════════════════════════════════════════
def parse_equation(eq_str):
    """
    Parse equation string to a safe callable, supporting:
    - ln(x), log(x), exp(x), e^x, e**x
    - trig functions: sin, cos, tan, asin, acos, atan
    - ^ as ** operator
    - implicit multiplication (e.g. 2x -> 2*x)
    - polynomials, binomials like (x+2)(x-4)
    """
    import re

    s = eq_str.strip()

    # Replace ^ with **
    s = s.replace('^', '**')

    # Replace e** with exp() — handle e**x -> exp(x)
    s = re.sub(r'\be\*\*\(([^)]+)\)', r'exp(\1)', s)
    s = re.sub(r'\be\*\*([A-Za-z0-9_.]+)', r'exp(\1)', s)

    # Implicit multiplication: 2x -> 2*x, 2(x -> 2*(x, )(x -> )*(x
    s = re.sub(r'(\d)([A-Za-z(])', r'\1*\2', s)
    s = re.sub(r'\)(\()', r')*\1', s)
    s = re.sub(r'\)([A-Za-z0-9])', r')*\1', s)

    # Alias ln -> log (sympy uses log for natural log)
    s = re.sub(r'\bln\s*\(', 'log(', s)

    x = sp.Symbol('x')
    expr = sp.sympify(s, locals={
        'x': x,
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
        'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
        'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
        'pi': sp.pi, 'E': sp.E, 'e': sp.E,
        'abs': sp.Abs,
    })
    return expr, x


def make_safe_f(expr, x_sym):
    """Create a safe numpy-lambdified function with domain checking."""
    f_raw = sp.lambdify(x_sym, expr, modules=[
        {'log': np.log, 'exp': np.exp, 'sqrt': np.sqrt,
         'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
         'asin': np.arcsin, 'acos': np.arccos, 'atan': np.arctan,
         'sinh': np.sinh, 'cosh': np.cosh, 'tanh': np.tanh,
         'Abs': np.abs, 'pi': np.pi}, 'numpy'
    ])

    def safe_f(val):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = f_raw(val)
                if np.isscalar(result):
                    if not np.isfinite(result):
                        return np.nan
                    return float(result)
                else:
                    arr = np.array(result, dtype=float)
                    arr[~np.isfinite(arr)] = np.nan
                    return arr
        except Exception:
            if np.isscalar(val):
                return np.nan
            return np.full(np.asarray(val).shape, np.nan)

    return safe_f


def make_safe_df(expr, x_sym):
    """Create safe derivative function."""
    dexpr = sp.diff(expr, x_sym)
    df_raw = sp.lambdify(x_sym, dexpr, modules=[
        {'log': np.log, 'exp': np.exp, 'sqrt': np.sqrt,
         'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
         'asin': np.arcsin, 'acos': np.arccos, 'atan': np.arctan,
         'Abs': np.abs, 'pi': np.pi}, 'numpy'
    ])

    def safe_df(val):
        try:
            result = df_raw(val)
            if np.isscalar(result):
                return float(result) if np.isfinite(result) else np.nan
            return result
        except Exception:
            return np.nan

    return safe_df


# ══════════════════════════════════════════════════════════════════════════════
#  AUTOMATIC INTERVAL SCANNER — DETECTS ALL SIGN-CHANGE BRACKETS
# ══════════════════════════════════════════════════════════════════════════════
def scan_intervals(f, x_start, x_end, step=0.1):
    """
    Scan [x_start, x_end] with given step.
    Returns list of (xl, xu) pairs where sign change occurs.
    Also handles near-zero crossings for repeated/touching roots.
    """
    brackets = []
    xs = np.arange(x_start, x_end, step)
    if len(xs) == 0:
        return brackets

    fvals = np.array([f(xi) for xi in xs])

    for i in range(len(xs) - 1):
        fl, fr = fvals[i], fvals[i + 1]
        xl, xu = xs[i], xs[i + 1]

        # Skip NaN
        if np.isnan(fl) or np.isnan(fr):
            continue

        # Sign change
        if fl * fr < 0:
            brackets.append((xl, xu))
        # Very close to zero at a point (potential repeated root)
        elif abs(fl) < 1e-8:
            # Check it's not already covered
            if not any(abs(xl - b[0]) < step * 0.5 for b in brackets):
                brackets.append((max(xl - step, x_start), xl + step))

    # Deduplicate brackets that are too close
    deduped = []
    for b in brackets:
        if not any(abs(b[0] - d[0]) < step for d in deduped):
            deduped.append(b)

    return deduped


# ══════════════════════════════════════════════════════════════════════════════
#  NUMERICAL METHODS — ALL RETURN (root, iterations, final_ea, table_rows)
# ══════════════════════════════════════════════════════════════════════════════

def method_bisection(f, xl, xu, tol, max_iter):
    results = []
    xr_old = None
    root, iterations, final_err = None, 0, 0
    for i in range(int(max_iter)):
        xr = (xl + xu) / 2.0
        fxl, fxr = f(xl), f(xr)
        if any(np.isnan(v) for v in [fxl, fxr]):
            break
        prod = fxl * fxr
        ea = abs((xr - xr_old) / xr) * 100 if xr_old is not None and xr != 0 else None
        results.append({
            "Iteration": i + 1, "x_l": round(xl, 8), "x_r": round(xr, 8), "x_u": round(xu, 8),
            "f(x_l)": round(float(fxl), 8), "f(x_r)": round(float(fxr), 8),
            "|E_a| %": round(ea, 6) if ea is not None else "",
            "f(x_l)*f(x_r)": "< 0" if prod < 0 else "> 0",
            "Remark": "1st subinterval" if prod < 0 else "2nd subinterval"
        })
        if (ea is not None and ea < tol) or fxr == 0:
            root, iterations, final_err = xr, i + 1, ea if ea else 0
            break
        if prod < 0:
            xu = xr
        else:
            xl = xr
        xr_old = xr
    if root is None and results:
        root = results[-1]["x_r"]
        iterations = len(results)
        final_err = results[-1]["|E_a| %"] or 0
    return root, iterations, final_err, results


def method_regula_falsi(f, xl, xu, tol, max_iter):
    results = []
    xr_old = None
    root, iterations, final_err = None, 0, 0
    for i in range(int(max_iter)):
        fxl, fxu = f(xl), f(xu)
        if np.isnan(fxl) or np.isnan(fxu) or (fxl - fxu) == 0:
            break
        xr = (xu * fxl - xl * fxu) / (fxl - fxu)
        fxr = f(xr)
        if np.isnan(fxr):
            break
        prod = fxl * fxr
        ea = abs((xr - xr_old) / xr) if xr_old is not None and xr != 0 else None
        results.append({
            "No. of Iteration": i + 1, "x_L": round(xl, 8), "x_U": round(xu, 8), "x_R": round(xr, 8),
            "E_a": round(ea, 8) if ea is not None else "",
            "f(x_L)": round(float(fxl), 8), "f(x_U)": round(float(fxu), 8), "f(x_R)": round(float(fxr), 8),
            "f(x_L)*f(x_R)": "< 0" if prod < 0 else "> 0"
        })
        if (ea is not None and ea < tol) or abs(fxr) < tol:
            root, iterations, final_err = xr, i + 1, ea if ea else 0
            break
        if prod < 0:
            xu = xr
        else:
            xl = xr
        xr_old = xr
    if root is None and results:
        root = results[-1]["x_R"]
        iterations = len(results)
        final_err = results[-1]["E_a"] or 0
    return root, iterations, final_err, results


def method_newton_raphson(f, df, x0, tol, max_iter):
    results = []
    xi = x0
    root, iterations, final_err = None, 0, 0
    results.append({
        "No. of iteration": 0, "x_i": round(xi, 8), "E_a": "",
        "f(x)": round(float(f(xi)), 8) if not np.isnan(f(xi)) else "NaN",
        "f'(x)": round(float(df(xi)), 8) if not np.isnan(df(xi)) else "NaN"
    })
    for i in range(int(max_iter)):
        fxi, dfxi = f(xi), df(xi)
        if np.isnan(fxi) or np.isnan(dfxi) or dfxi == 0:
            break
        xi_new = xi - fxi / dfxi
        if np.isnan(xi_new) or not np.isfinite(xi_new):
            break
        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        xi = xi_new
        results.append({
            "No. of iteration": i + 1, "x_i": round(xi, 8), "E_a": round(ea, 8),
            "f(x)": round(float(f(xi)), 8) if not np.isnan(f(xi)) else "NaN",
            "f'(x)": round(float(df(xi)), 8) if not np.isnan(df(xi)) else "NaN"
        })
        if ea < tol:
            root, iterations, final_err = xi, i + 1, ea
            break
    if root is None and len(results) > 1:
        root = results[-1]["x_i"]
        iterations = len(results) - 1
        final_err = results[-1]["E_a"] or 0
    return root, iterations, final_err, results


def method_secant(f, x_prev, x0, tol, max_iter):
    results = []
    xi_prev, xi = x_prev, x0
    root, iterations, final_err = None, 0, 0
    for i in range(int(max_iter)):
        fxi, fxi_prev = f(xi), f(xi_prev)
        if np.isnan(fxi) or np.isnan(fxi_prev) or (fxi - fxi_prev) == 0:
            break
        xi_new = xi - (fxi * (xi - xi_prev)) / (fxi - fxi_prev)
        if np.isnan(xi_new) or not np.isfinite(xi_new):
            break
        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        results.append({
            "Iteration Number": i + 1, "x_{i-1}": round(xi_prev, 8), "x_i": round(xi, 8),
            "x_{i+1}": round(xi_new, 8), "E_a": round(ea, 8),
            "f(x_{i-1})": round(float(fxi_prev), 8), "f(x_i)": round(float(fxi), 8),
            "f(x_{i+1})": round(float(f(xi_new)), 8) if not np.isnan(f(xi_new)) else "NaN"
        })
        xi_prev, xi = xi, xi_new
        if ea < tol:
            root, iterations, final_err = xi_new, i + 1, ea
            break
    if root is None and results:
        root = results[-1]["x_{i+1}"]
        iterations = len(results)
        final_err = results[-1]["E_a"] or 0
    return root, iterations, final_err, results


def method_incremental(f, xl, delta_x, tol, max_iter):
    results = []
    curr_xl = xl
    curr_dx = delta_x
    root, iterations, final_err = None, 0, 0
    for i in range(int(max_iter)):
        curr_xu = curr_xl + curr_dx
        fxl, fxu = f(curr_xl), f(curr_xu)
        if np.isnan(fxl) or np.isnan(fxu):
            curr_xl = curr_xu
            continue
        prod = fxl * fxu
        remark = "Go to next interval" if prod > 0 else "Revert back to xl & consider smaller interval"
        results.append({
            "Iteration": i + 1, "x_l": round(curr_xl, 8), "Δx": round(curr_dx, 8),
            "x_u": round(curr_xu, 8), "f(x_l)": round(float(fxl), 8), "f(x_u)": round(float(fxu), 8),
            "f(x_l)*f(x_u)": "> 0" if prod > 0 else "< 0", "Remark": remark
        })
        if abs(fxu) < tol or curr_dx < (tol / 100):
            root, iterations = curr_xu, i + 1
            break
        if prod > 0:
            curr_xl = curr_xu
        else:
            curr_dx = curr_dx / 10.0
    if root is None and results:
        root = results[-1]["x_u"]
        iterations = len(results)
    return root, iterations, 0, results


def solve_on_bracket(method_name, f, df, xl, xu, tol, max_iter, x_prev_sec=None, x0_sec=None, delta_x_inc=None):
    """Dispatch to the correct method for a given bracket."""
    mid = (xl + xu) / 2.0
    if method_name == "Bisection Method":
        return method_bisection(f, xl, xu, tol, max_iter)
    elif method_name == "Regula-Falsi":
        return method_regula_falsi(f, xl, xu, tol, max_iter)
    elif method_name == "Newton-Raphson":
        return method_newton_raphson(f, df, mid, tol, max_iter)
    elif method_name == "Secant Method":
        x0 = xl if x_prev_sec is None else x_prev_sec
        x1 = xu if x0_sec is None else x0_sec
        return method_secant(f, xl, xu, tol, max_iter)
    elif method_name == "Incremental Search":
        dx = delta_x_inc if delta_x_inc else (xu - xl) / 10.0
        return method_incremental(f, xl, dx, tol, max_iter)
    return None, 0, 0, []


# ══════════════════════════════════════════════════════════════════════════════
#  GRAPH BUILDER — FULL CURVE + ALL ROOTS
# ══════════════════════════════════════════════════════════════════════════════
def build_full_graph(f, eq_str, all_roots, x_start, x_end):
    """
    Build a Plotly figure showing the complete curve across [x_start, x_end]
    with all detected roots marked.
    """
    # Dense x values for smooth curve
    x_vals = np.linspace(x_start, x_end, 1200)
    y_vals = f(x_vals)

    # Clip extreme values for display clarity
    if np.any(np.isfinite(y_vals)):
        finite_y = y_vals[np.isfinite(y_vals)]
        if len(finite_y) > 0:
            q_low = np.percentile(finite_y, 2)
            q_high = np.percentile(finite_y, 98)
            margin = max(abs(q_high - q_low) * 0.5, 1.0)
            y_lo = q_low - margin
            y_hi = q_high + margin
            y_display = np.clip(y_vals, y_lo, y_hi)
        else:
            y_display = y_vals
    else:
        y_display = y_vals

    # Mask NaN with None for plotly (creates breaks)
    y_plot = [float(v) if np.isfinite(v) else None for v in y_display]

    fig = go.Figure()

    # Main curve
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_plot,
        mode='lines', name='f(x)',
        line=dict(color='#5C3317', width=2.5),
        connectgaps=False
    ))

    # Zero axes
    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.3)
    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.3)

    # Root markers — distinct colors
    root_colors = ['#8B1A1A', '#1A4A8B', '#1A6B2A', '#6B1A6B', '#8B5E1A',
                   '#1A6B6B', '#8B3A1A', '#3A1A8B', '#6B6B1A', '#1A8B4A']

    for idx, root_info in enumerate(all_roots):
        r = root_info['root']
        color = root_colors[idx % len(root_colors)]
        fig.add_trace(go.Scatter(
            x=[r], y=[0],
            mode='markers+text',
            name=f'Root {idx+1}: x ≈ {r:.6f}',
            marker=dict(color=color, size=13, symbol='circle',
                        line=dict(color='#2C1A0E', width=2)),
            text=[f'  x≈{r:.4f}'],
            textposition='top right',
            textfont=dict(family='Crimson Text, serif', size=11, color=color),
        ))

    # Auto-range to show all roots nicely
    if all_roots:
        root_xs = [r['root'] for r in all_roots]
        rmin, rmax = min(root_xs), max(root_xs)
        pad = max((rmax - rmin) * 0.3, 2.0)
        x_lo = max(x_start, rmin - pad)
        x_hi = min(x_end, rmax + pad)
    else:
        x_lo, x_hi = x_start, x_end

    fig.update_layout(
        title=dict(text=f"f(x) = {eq_str}", font=dict(family="Playfair Display,serif", size=14, color="#2C1A0E")),
        xaxis_title="x", yaxis_title="f(x)",
        hovermode="x unified",
        plot_bgcolor='#FBF4E6', paper_bgcolor='#FBF4E6',
        font=dict(family="Crimson Text,serif", color="#2C1A0E"),
        xaxis=dict(
            gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882',
            tickfont=dict(family="Crimson Text,serif"),
            range=[x_lo, x_hi]
        ),
        yaxis=dict(
            gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882',
            tickfont=dict(family="Crimson Text,serif")
        ),
        legend=dict(bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1,
                    font=dict(family="Crimson Text,serif"), orientation='v',
                    x=1.01, y=1),
        margin=dict(l=8, r=8, t=42, b=8),
        height=370,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
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
#  MODULE 1: ROOT FINDING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.markdown('<div class="stitle">⊛ Root Finding Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Complete multi-root detection with automatic interval scanning and full equation support.</div>', unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 2.5])

    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚙ Parameters</div>', unsafe_allow_html=True)

        eq_str = st.text_input(
            "Equation f(x)",
            value="x^3 - 6*x + 2",
            help="Supports: ln(x), log(x), exp(x), e^x, sin/cos/tan, polynomials, ^, **, implicit multiplication. Example: ln(x) - 2, (x+2)(x-4), x^5 - 6x^3 + x"
        )

        method = st.selectbox("Algorithm", [
            "Bisection Method", "Regula-Falsi", "Newton-Raphson",
            "Secant Method", "Incremental Search"
        ])

        st.markdown("**Scanning Interval**")
        sc1, sc2 = st.columns(2)
        x_start = sc1.number_input("Start", value=-10.0, format="%.2f")
        x_end   = sc2.number_input("End",   value=10.0,  format="%.2f")
        scan_step = st.number_input("Scan Step (Δ)", value=0.5, format="%.4f",
                                    help="Smaller = more roots detected, slower scan")

        tol      = st.number_input("Tolerance", value=0.0001, format="%.6f")
        max_iter = st.number_input("Max Iterations per Root", value=100, step=1)

        # Method-specific initial guesses (used as fallback / single-root mode)
        if method == "Newton-Raphson":
            x0_nr = st.number_input("Initial Guess (xi)", value=1.0, format="%.4f",
                                     help="Used when scanning cannot bracket a root")
        elif method == "Secant Method":
            x_prev_s = st.number_input("First Guess (x_{i-1})", value=0.5, format="%.4f")
            x0_s     = st.number_input("Second Guess (x_i)",    value=2.0, format="%.4f")
        elif method == "Incremental Search":
            delta_x_inc = st.number_input("Increment (Δx)", value=0.5, format="%.4f")

        solve_btn = st.button("⊛  Calculate All Roots")
        st.markdown('</div>', unsafe_allow_html=True)

    # ──────────────── RIGHT COLUMN ────────────────
    with col_results:

        if solve_btn:
            try:
                expr, x_sym = parse_equation(eq_str)
                f  = make_safe_f(expr, x_sym)
                df = make_safe_df(expr, x_sym)

                # 1. Scan full interval for brackets
                brackets = scan_intervals(f, x_start, x_end, scan_step)

                if not brackets:
                    st.warning(f"No sign changes detected in [{x_start}, {x_end}] with step {scan_step}. "
                               "Try widening the interval or using a smaller scan step.")
                else:
                    all_roots = []
                    all_tables = []

                    progress = st.progress(0, text="Scanning for roots...")
                    for idx, (xl, xu) in enumerate(brackets):
                        progress.progress(int((idx + 1) / len(brackets) * 100),
                                          text=f"Solving bracket {idx+1}/{len(brackets)}: [{xl:.3f}, {xu:.3f}]")

                        try:
                            if method == "Newton-Raphson":
                                root, iters, ea, rows = method_newton_raphson(
                                    f, df, (xl + xu) / 2.0, tol, max_iter)
                            elif method == "Secant Method":
                                root, iters, ea, rows = method_secant(f, xl, xu, tol, max_iter)
                            elif method == "Incremental Search":
                                dx = delta_x_inc if 'delta_x_inc' in dir() else scan_step / 5
                                root, iters, ea, rows = method_incremental(f, xl, dx, tol, max_iter)
                            else:
                                root, iters, ea, rows = solve_on_bracket(
                                    method, f, df, xl, xu, tol, max_iter)

                            if root is not None:
                                froot = f(root)
                                if froot is None or np.isnan(froot):
                                    continue
                                # Dedup roots that are very close to each other
                                if not any(abs(root - r['root']) < tol * 100 for r in all_roots):
                                    all_roots.append({
                                        'root': root, 'f_root': float(froot),
                                        'iterations': iters, 'error': ea,
                                        'method': method, 'bracket': (xl, xu)
                                    })
                                    all_tables.append(rows)
                        except Exception as inner_e:
                            continue

                    progress.empty()

                    # Sort roots by value
                    combined = sorted(zip(all_roots, all_tables), key=lambda z: z[0]['root'])
                    all_roots = [c[0] for c in combined]
                    all_tables = [c[1] for c in combined]

                    # Persist
                    st.session_state.rf_all_roots  = all_roots
                    st.session_state.rf_results    = all_tables[0] if all_tables else []
                    st.session_state.rf_root       = all_roots[0]['root'] if all_roots else None
                    st.session_state.rf_iterations = all_roots[0]['iterations'] if all_roots else 0
                    st.session_state.rf_error      = all_roots[0]['error'] if all_roots else 0
                    st.session_state.rf_eq         = eq_str
                    st.session_state.rf_method     = method

                    if all_roots:
                        fig = build_full_graph(f, eq_str, all_roots, x_start, x_end)
                        st.session_state.rf_fig = fig

                        # History
                        root_str = ", ".join([f"x≈{r['root']:.6f}" for r in all_roots])
                        st.session_state.history.append({
                            "type":      "Root Finding",
                            "method":    method,
                            "equation":  f"f(x) = {eq_str}",
                            "answer":    f"{len(all_roots)} root(s): {root_str}",
                            "timestamp": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
                        })
                        st.toast(f"Found {len(all_roots)} root(s)!", icon="✅")
                    else:
                        st.warning("Brackets detected but no roots converged. Try adjusting tolerance or iteration count.")

            except Exception as e:
                st.error(f"Error parsing or solving equation: {e}")

        # ── DISPLAY RESULTS ──
        if st.session_state.rf_all_roots:
            all_roots  = st.session_state.rf_all_roots
            all_tables = st.session_state.rf_results  # first table only for legacy compat

            # METRICS
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Roots Found", len(all_roots))
            m2.metric("Primary Root",      f"{all_roots[0]['root']:.8f}")
            m3.metric("Scan Method",       st.session_state.rf_method)

            # ROOT SUMMARY PANEL
            st.markdown('<div class="panel" style="margin-top:0.7rem;">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">✦ Complete Root Summary</div>', unsafe_allow_html=True)
            summary_rows = []
            for idx, r in enumerate(all_roots):
                summary_rows.append({
                    "Root #": idx + 1,
                    "Approximate Root": f"{r['root']:.10f}",
                    "f(root)": f"{r['f_root']:.4e}",
                    "Error (E_a)": f"{r['error']:.4e}" if r['error'] else "—",
                    "Method": r['method'],
                    "Iterations": r['iterations'],
                    "Bracket": f"[{r['bracket'][0]:.3f}, {r['bracket'][1]:.3f}]"
                })
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # GRAPH
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📈 Full Function Graph — All Roots</div>', unsafe_allow_html=True)
            st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ITERATION TABLES PER ROOT — stored as all_tables in session is lossy; rebuild display
            if st.session_state.rf_results:
                with st.expander("📊 View Iteration Table (Primary Root)", expanded=False):
                    st.dataframe(pd.DataFrame(st.session_state.rf_results), use_container_width=True)

        elif st.session_state.rf_root is not None:
            # Legacy single-root display fallback
            m1, m2, m3 = st.columns(3)
            m1.metric("Calculated Root",  f"{st.session_state.rf_root:.8f}")
            m2.metric("Total Iterations", st.session_state.rf_iterations)
            m3.metric("Final Error",      f"{st.session_state.rf_error:.3e}" if st.session_state.rf_error else "—")
            if st.session_state.rf_fig:
                st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            if st.session_state.rf_results:
                with st.expander("📊 Iteration Table", expanded=False):
                    st.dataframe(pd.DataFrame(st.session_state.rf_results), use_container_width=True)
        else:
            st.markdown("""
                <div class="panel" style="min-height:520px;">
                    <div class="placeholder-box">
                        ✦ Configure the parameters on the left<br>
                        and press <em>Calculate All Roots</em> to begin.<br><br>
                        The system will automatically scan the full interval,<br>
                        detect every root, and display complete results.
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

                result = None
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

                st.session_state.mx_result = {"op": op, "result": result,
                                               "det_val": det_val,
                                               "ans_str": ans_str}
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
