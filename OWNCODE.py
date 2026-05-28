import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time
import re
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Numerical Project",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

for key, val in {
    "rf_all_roots":  [],
    "rf_all_tables": [],
    "rf_fig":        None,
    "rf_eq":         "",
    "rf_method":     "",
    "mx_result":     None,
    "mx_op":         "",
    "history":       [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

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
.main .block-container { padding: 0.6rem 1.8rem 2rem 1.8rem; max-width: 100%; }
#MainMenu, footer { visibility: hidden; }
::-webkit-scrollbar            { width: 6px; height: 6px; }
::-webkit-scrollbar-track      { background: var(--bg2); }
::-webkit-scrollbar-thumb      { background: var(--brown-lt); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover{ background: var(--brown-md); }

.vhdr {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 2rem 0.9rem 2rem;
    background: linear-gradient(120deg, #1E0F06 0%, #3B2210 30%, #5C3317 60%, #3B2210 85%, #1E0F06 100%);
    border-radius: 14px; margin-bottom: 0.2rem;
    box-shadow: 0 6px 28px var(--shadow-dk), inset 0 1px 0 rgba(212,169,106,0.25);
    border: 1px solid #6A3E20; position: relative; overflow: hidden;
}
.vhdr::after {
    content: ''; position: absolute; inset: 0;
    background: repeating-linear-gradient(60deg, transparent, transparent 18px,
        rgba(212,169,106,0.04) 18px, rgba(212,169,106,0.04) 36px);
    pointer-events: none;
}
.vhdr-name {
    font-family: 'Cormorant Garamond', serif; font-size: 0.88rem; color: var(--gold);
    letter-spacing: 0.07em; line-height: 1.55; font-style: italic;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5); min-width: 185px;
}
.vhdr-title {
    font-family: 'Playfair Display', serif; font-size: 1.95rem; font-weight: 700;
    color: #F5E6C8; letter-spacing: 0.25em; text-align: center;
    text-shadow: 0 2px 8px rgba(0,0,0,0.55); flex: 1;
}
.vhdr-right {
    font-family: 'Cormorant Garamond', serif; font-size: 0.8rem; color: #B8936A;
    text-align: right; letter-spacing: 0.05em; line-height: 1.6; min-width: 185px;
}
.ornament {
    text-align: center; color: #9B7245; letter-spacing: 0.55em;
    margin: 0.35rem 0 0.55rem 0; font-size: 0.95rem; user-select: none;
}
.nav-strip {
    background: linear-gradient(135deg, #EDE0C4 0%, #E2D0AA 50%, #EDE0C4 100%);
    border: 1.5px solid var(--border); border-radius: 11px;
    padding: 0.6rem 1.3rem 0.45rem 1.3rem; margin-bottom: 0.85rem;
    box-shadow: 0 2px 12px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.45);
}
.stitle {
    font-family: 'Playfair Display', serif; font-size: 1.15rem; font-weight: 700;
    color: var(--brown-dk); border-bottom: 2px solid var(--brown-lt);
    padding-bottom: 0.28rem; margin-bottom: 0.75rem; letter-spacing: 0.04em;
}
.ssub {
    font-family: 'Cormorant Garamond', serif; font-size: 1rem;
    color: #6B4226; font-style: italic; margin-bottom: 0.85rem;
}
.panel {
    background: linear-gradient(160deg, var(--cream) 0%, var(--cream2) 100%);
    border: 1.5px solid var(--border); border-radius: 12px; padding: 1.1rem 1.25rem;
    box-shadow: 3px 4px 18px var(--shadow), inset 0 1px 0 rgba(255,255,255,0.55);
    margin-bottom: 0.75rem;
}
.panel-dark {
    background: linear-gradient(160deg, #EDE0C4 0%, #E5D4AE 100%);
    border: 1.5px solid var(--border2); border-radius: 12px; padding: 1rem 1.25rem;
    box-shadow: 3px 4px 18px var(--shadow); margin-bottom: 0.75rem;
}
.panel-title {
    font-family: 'Playfair Display', serif; font-size: 0.98rem; font-weight: 600;
    color: var(--brown-md); letter-spacing: 0.04em; margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 0.4rem;
}
div[data-testid="stRadio"] label > div p {
    font-family: 'Playfair Display', serif !important;
    font-size: 0.97rem !important; color: var(--brown-dk) !important; font-weight: 600 !important;
}
.stSelectbox > label, .stNumberInput > label, .stTextInput > label {
    font-family: 'Crimson Text', serif !important; color: #4A2A12 !important;
    font-size: 0.95rem !important; font-weight: 600 !important; letter-spacing: 0.02em !important;
}
.stSelectbox [data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
    border: 1.5px solid var(--border) !important; border-radius: 7px !important;
    background-color: var(--cream) !important; color: var(--brown-dk) !important;
    font-family: 'Crimson Text', serif !important; font-size: 0.97rem !important;
    box-shadow: inset 0 1px 5px rgba(59,31,12,0.07) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within,
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--brown-lt) !important;
    box-shadow: 0 0 0 2.5px rgba(139,94,60,0.2) !important;
}
.stButton > button {
    width: 100%; border-radius: 8px;
    background: linear-gradient(135deg, var(--brown-md) 0%, var(--brown-lt) 55%, #7A4F2E 100%);
    color: #F5E6C8; font-family: 'Playfair Display', serif; font-size: 0.97rem;
    font-weight: 700; border: 1px solid #9B7245; letter-spacing: 0.09em;
    padding: 0.55rem 1rem;
    box-shadow: 0 3px 14px var(--shadow-dk), inset 0 1px 0 rgba(255,255,255,0.1);
    transition: all 0.25s ease; text-shadow: 0 1px 3px rgba(0,0,0,0.35);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1E0F06 0%, var(--brown-md) 100%);
    transform: translateY(-1.5px); box-shadow: 0 5px 20px var(--shadow-dk); color: var(--gold-lt);
}
.stButton > button:active { transform: translateY(0px); }
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #EDE0C4, #E2CFA8) !important;
    border: 1.5px solid var(--border) !important; border-radius: 10px !important;
    padding: 0.7rem 0.9rem !important; box-shadow: 2px 3px 11px var(--shadow) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Cormorant Garamond', serif !important; color: #6B4226 !important;
    font-size: 0.78rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: var(--brown-dk) !important; font-size: 1.45rem !important;
}
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important; border-radius: 9px !important; overflow: hidden !important;
}
[data-testid="stDataFrame"] table { font-family: 'Crimson Text', serif !important; }
[data-testid="stDataFrame"] th {
    background-color: #5C3317 !important; color: #F5E6C8 !important;
    font-family: 'Playfair Display', serif !important; font-size: 0.82rem !important; letter-spacing: 0.05em !important;
}
[data-testid="stDataFrame"] tr:hover { background-color: #EDE0C4 !important; }
[data-testid="stInfo"] {
    background-color: #EDE0C4 !important; border-left: 4px solid var(--brown-lt) !important;
    border-radius: 7px !important; font-family: 'Crimson Text', serif !important;
}
[data-testid="stSuccess"] {
    background-color: #E4D8C0 !important; border-left: 4px solid var(--brown-md) !important;
    border-radius: 7px !important; font-family: 'Crimson Text', serif !important;
}
[data-testid="stAlert"] { font-family: 'Crimson Text', serif !important; border-radius: 7px !important; }
hr { border: none !important; border-top: 1.5px solid var(--border) !important; margin: 0.6rem 0 !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E0F06 0%, #2C1A0E 40%, #3B2210 100%) !important;
    border-right: 2px solid #5C3317 !important;
}
[data-testid="stSidebar"] * { color: #E8D5B0 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #3B2210, #5C3317) !important;
    border-color: #7A4F2E !important; color: #F5E6C8 !important; font-size: 0.85rem !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #5C3317, #8B5E3C) !important;
}
.hist-card {
    background: rgba(92,51,23,0.35); border: 1px solid rgba(200,169,122,0.35);
    border-radius: 9px; padding: 0.7rem 0.85rem; margin-bottom: 0.6rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25); transition: background 0.2s;
}
.hist-card:hover { background: rgba(92,51,23,0.55); }
.hist-method {
    font-family: 'Playfair Display', serif; font-size: 0.82rem; font-weight: 700;
    color: #E8C98A; letter-spacing: 0.05em; margin-bottom: 0.2rem;
}
.hist-eq {
    font-family: 'Crimson Text', serif; font-size: 0.88rem; color: #D4BC96;
    font-style: italic; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 0.15rem;
}
.hist-ans { font-family: 'Playfair Display', serif; font-size: 0.9rem; color: #F5E6C8; font-weight: 600; }
.hist-ts {
    font-family: 'Cormorant Garamond', serif; font-size: 0.75rem;
    color: #9B7A55; margin-top: 0.2rem; letter-spacing: 0.04em;
}
.hist-empty {
    text-align: center; padding: 1.5rem 0.5rem; font-family: 'Cormorant Garamond', serif;
    font-size: 0.95rem; font-style: italic; color: #7A5A3A;
}
.sidebar-hdr {
    font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700;
    color: #E8C98A; letter-spacing: 0.1em; text-align: center;
    padding: 0.2rem 0 0.6rem 0; border-bottom: 1px solid rgba(200,169,122,0.35); margin-bottom: 0.7rem;
}
.placeholder-box {
    text-align: center; padding: 2.5rem 1rem; color: #9B7245;
    font-family: 'Playfair Display', serif; font-size: 1rem; font-style: italic; line-height: 1.7;
}
.root-badge {
    display: inline-block;
    background: linear-gradient(135deg, #5C3317, #8B5E3C);
    color: #F5E6C8; font-family: 'Playfair Display', serif;
    font-size: 0.85rem; font-weight: 700; padding: 0.25rem 0.75rem;
    border-radius: 20px; margin: 0.2rem;
    box-shadow: 0 2px 8px rgba(44,26,14,0.25); letter-spacing: 0.04em;
}
.roots-summary {
    background: linear-gradient(160deg, #EDE0C4 0%, #E2CFA8 100%);
    border: 2px solid var(--border2); border-radius: 12px;
    padding: 1rem 1.25rem; margin-bottom: 0.75rem;
    box-shadow: 3px 4px 18px var(--shadow);
}
.roots-summary-title {
    font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700;
    color: var(--brown-md); margin-bottom: 0.6rem;
    border-bottom: 1px solid var(--border); padding-bottom: 0.35rem; letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  EQUATION PARSER — robust: handles f(x)=, LaTeX braces, ln, e^{x}, implicit mult
# ══════════════════════════════════════════════════════════════════════════════
def parse_equation(eq_str):
    s = eq_str.strip()

    # Strip leading "f(x)=", "y=", "0=" style prefixes
    s = re.sub(r'^[fFyY]\s*\([xX]\)\s*=\s*', '', s)
    s = re.sub(r'^[yY]\s*=\s*', '', s)
    s = re.sub(r'^0\s*=\s*', '', s)

    # LaTeX curly braces → parentheses  e.g. e^{-x} → e**(-(x))
    s = re.sub(r'\{([^}]*)\}', r'(\1)', s)

    # ^ → **
    s = s.replace('^', '**')

    # e**(...)  or  e**scalar  →  exp(...)
    s = re.sub(r'\be\s*\*\*\s*\(([^)]+)\)', r'exp(\1)', s)
    s = re.sub(r'\be\s*\*\*\s*([A-Za-z0-9_.+-]+)', r'exp(\1)', s)

    # Standalone 'e' not followed by 'x' or 'p' (i.e. not 'exp') → E (Euler's number)
    s = re.sub(r'(?<![a-zA-Z])e(?![xXpP\*])', 'E', s)

    # ln( → log(
    s = re.sub(r'\bln\s*\(', 'log(', s)

    # Implicit multiplication: 2x → 2*x, 3( → 3*(, )x → )*x, )(→)*(
    s = re.sub(r'(\d)([A-Za-z(])', r'\1*\2', s)
    s = re.sub(r'\)\s*\(', r')*(', s)
    s = re.sub(r'\)\s*([A-Za-z0-9])', r')*\1', s)

    x = sp.Symbol('x')
    local_ns = {
        'x': x, 'X': x,
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
        'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
        'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
        'pi': sp.pi, 'E': sp.E, 'e': sp.E, 'abs': sp.Abs,
    }
    try:
        expr = sp.sympify(s, locals=local_ns)
    except Exception as err:
        raise ValueError(
            f"Could not parse '{eq_str}'.\n"
            f"Processed as: '{s}'\n"
            f"Hint: Use ** for powers, * for multiplication, log(x) or ln(x), exp(x) or e^x.\n"
            f"Original error: {err}"
        )
    return expr, x


def make_safe_f(expr, x_sym):
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
                    return float(result) if np.isfinite(result) else np.nan
                arr = np.array(result, dtype=float)
                arr[~np.isfinite(arr)] = np.nan
                return arr
        except Exception:
            if np.isscalar(val):
                return np.nan
            return np.full(np.asarray(val).shape, np.nan)
    return safe_f


def make_safe_df(expr, x_sym):
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
#  INTERVAL SCANNER
# ══════════════════════════════════════════════════════════════════════════════
def scan_intervals(f, x_start, x_end, step):
    xs = np.arange(x_start, x_end + step, step)
    if len(xs) == 0:
        return []
    fvals = np.array([f(xi) for xi in xs], dtype=float)
    deduped = []
    for i in range(len(xs) - 1):
        fl, fr = fvals[i], fvals[i + 1]
        if np.isnan(fl) or np.isnan(fr):
            continue
        if fl * fr < 0:
            b = (float(xs[i]), float(xs[i + 1]))
            if not any(abs(b[0] - d[0]) < step * 0.5 for d in deduped):
                deduped.append(b)
        elif abs(fl) < 1e-10:
            b = (float(xs[i]) - step, float(xs[i]) + step)
            if not any(abs(b[0] - d[0]) < step * 0.5 for d in deduped):
                deduped.append(b)
    return deduped


# ══════════════════════════════════════════════════════════════════════════════
#  NUMERICAL METHODS — original table column names preserved exactly
# ══════════════════════════════════════════════════════════════════════════════

def method_incremental(f, xl, delta_x, tol, max_iter):
    results = []
    curr_xl, curr_dx = xl, delta_x
    root, iterations = None, 0
    for i in range(int(max_iter)):
        curr_xu = curr_xl + curr_dx
        fxl, fxu = f(curr_xl), f(curr_xu)
        if np.isnan(fxl) or np.isnan(fxu):
            curr_xl = curr_xu
            continue
        prod = fxl * fxu
        remark = "Go to next interval" if prod > 0 else "Revert back to xl & consider smaller interval"
        results.append({
            "Iteration":      i + 1,
            "x_l":            curr_xl,
            "Δx":             curr_dx,
            "x_u":            curr_xu,
            "f(x_l)":         fxl,
            "f(x_u)":         fxu,
            "f(x_l)*f(x_u)": "> 0" if prod > 0 else "< 0",
            "Remark":         remark,
        })
        if abs(fxu) < tol or curr_dx < (tol / 10):
            root, iterations = curr_xu, i + 1
            break
        curr_xl = curr_xu if prod > 0 else curr_xl
        curr_dx = curr_dx if prod > 0 else curr_dx / 10.0
    if root is None and results:
        root, iterations = results[-1]["x_u"], len(results)
    return root, iterations, 0, results


def method_bisection(f, xl, xu, tol, max_iter):
    results = []
    xr_old  = None
    root, iterations, final_err = None, 0, 0
    for i in range(int(max_iter)):
        xr = (xl + xu) / 2.0
        fxl, fxr = f(xl), f(xr)
        if np.isnan(fxl) or np.isnan(fxr):
            break
        prod = fxl * fxr
        ea   = abs((xr - xr_old) / xr) * 100 if (xr_old is not None and xr != 0) else None
        results.append({
            "Iteration":      i + 1,
            "x_l":            xl,
            "x_r":            xr,
            "x_u":            xu,
            "f(x_l)":         fxl,
            "f(x_r)":         fxr,
            "|E_a| %":        ea if ea is not None else "",
            "f(x_l)*f(x_r)": "< 0" if prod < 0 else "> 0",
            "Remark":         "1st subinterval" if prod < 0 else "2nd subinterval",
        })
        if (ea is not None and ea < tol) or fxr == 0:
            root, iterations, final_err = xr, i + 1, ea or 0
            break
        xu = xr if prod < 0 else xu
        xl = xr if prod >= 0 else xl
        xr_old = xr
    if root is None and results:
        root = results[-1]["x_r"]
        iterations = len(results)
        raw = results[-1]["|E_a| %"]
        final_err = raw if isinstance(raw, float) else 0
    return root, iterations, final_err, results


def method_regula_falsi(f, xl, xu, tol, max_iter):
    results = []
    xr_old  = None
    root, iterations, final_err = None, 0, 0
    for i in range(int(max_iter)):
        fxl, fxu = f(xl), f(xu)
        if np.isnan(fxl) or np.isnan(fxu) or (fxl - fxu) == 0:
            break
        xr  = (xu * fxl - xl * fxu) / (fxl - fxu)
        fxr = f(xr)
        if np.isnan(fxr):
            break
        prod = fxl * fxr
        ea   = abs((xr - xr_old) / xr) if (xr_old is not None and xr != 0) else None
        results.append({
            "No. of Iteration": i + 1,
            "x_L":              xl,
            "x_U":              xu,
            "x_R":              xr,
            "E_a":              ea if ea is not None else "",
            "f(x_L)":           fxl,
            "f(x_U)":           fxu,
            "f(x_R)":           fxr,
            "f(x_L)*f(x_R)":   "< 0" if prod < 0 else "> 0",
        })
        if (ea is not None and ea < tol) or abs(fxr) < tol:
            root, iterations, final_err = xr, i + 1, ea or 0
            break
        xu = xr if prod < 0 else xu
        xl = xr if prod >= 0 else xl
        xr_old = xr
    if root is None and results:
        root = results[-1]["x_R"]
        iterations = len(results)
        raw = results[-1]["E_a"]
        final_err = raw if isinstance(raw, float) else 0
    return root, iterations, final_err, results


def method_newton_raphson(f, df, x0, tol, max_iter):
    results = []
    xi      = x0
    root, iterations, final_err = None, 0, 0
    results.append({
        "No. of iteration": 0,
        "x_i":              xi,
        "E_a":              "",
        "f(x)":             f(xi)  if not np.isnan(f(xi))  else "NaN",
        "f'(x)":            df(xi) if not np.isnan(df(xi)) else "NaN",
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
            "No. of iteration": i + 1,
            "x_i":              xi,
            "E_a":              ea,
            "f(x)":             f(xi)  if not np.isnan(f(xi))  else "NaN",
            "f'(x)":            df(xi) if not np.isnan(df(xi)) else "NaN",
        })
        if ea < tol:
            root, iterations, final_err = xi, i + 1, ea
            break
    if root is None and len(results) > 1:
        root = results[-1]["x_i"]
        iterations = len(results) - 1
        raw = results[-1]["E_a"]
        final_err = raw if isinstance(raw, float) else 0
    return root, iterations, final_err, results


def method_secant(f, x_prev, x0, tol, max_iter):
    results   = []
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
        fxi_new = f(xi_new)
        results.append({
            "Iteration Number": i + 1,
            "x_{i-1}":          xi_prev,
            "x_i":              xi,
            "x_{i+1}":          xi_new,
            "E_a":              ea,
            "f(x_{i-1})":       fxi_prev,
            "f(x_i)":           fxi,
            "f(x_{i+1})":       fxi_new if not np.isnan(fxi_new) else "NaN",
        })
        xi_prev, xi = xi, xi_new
        if ea < tol:
            root, iterations, final_err = xi_new, i + 1, ea
            break
    if root is None and results:
        root = results[-1]["x_{i+1}"]
        iterations = len(results)
        final_err  = results[-1]["E_a"]
    return root, iterations, final_err, results


# ══════════════════════════════════════════════════════════════════════════════
#  GRAPH BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_full_graph(f, eq_str, all_roots, x_start, x_end):
    x_vals = np.linspace(x_start, x_end, 1200)
    y_vals = f(x_vals)

    if np.any(np.isfinite(y_vals)):
        finite_y = y_vals[np.isfinite(y_vals)]
        q_lo  = np.percentile(finite_y, 2)
        q_hi  = np.percentile(finite_y, 98)
        marg  = max(abs(q_hi - q_lo) * 0.5, 1.0)
        y_display = np.clip(y_vals, q_lo - marg, q_hi + marg)
    else:
        y_display = y_vals

    y_plot = [float(v) if np.isfinite(v) else None for v in y_display]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_plot, mode='lines', name='f(x)',
        line=dict(color='#5C3317', width=2.5), connectgaps=False
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.3)
    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.3)

    root_colors = ['#8B1A1A','#1A4A8B','#1A6B2A','#6B1A6B','#8B5E1A',
                   '#1A6B6B','#8B3A1A','#3A1A8B','#6B6B1A','#1A8B4A']
    for idx, ri in enumerate(all_roots):
        r     = ri['root']
        color = root_colors[idx % len(root_colors)]
        fig.add_trace(go.Scatter(
            x=[r], y=[0], mode='markers+text',
            name=f'Root {idx+1}: x ≈ {r:.6f}',
            marker=dict(color=color, size=13, symbol='circle',
                        line=dict(color='#2C1A0E', width=2)),
            text=[f'  x≈{r:.4f}'], textposition='top right',
            textfont=dict(family='Crimson Text, serif', size=11, color=color),
        ))

    if all_roots:
        rxs = [ri['root'] for ri in all_roots]
        rmin, rmax = min(rxs), max(rxs)
        pad  = max((rmax - rmin) * 0.35, 2.5)
        x_lo = max(x_start, rmin - pad)
        x_hi = min(x_end,   rmax + pad)
    else:
        x_lo, x_hi = x_start, x_end

    fig.update_layout(
        title=dict(text=f"f(x) = {eq_str}",
                   font=dict(family="Playfair Display,serif", size=14, color="#2C1A0E")),
        xaxis_title="x", yaxis_title="f(x)",
        hovermode="x unified",
        plot_bgcolor='#FBF4E6', paper_bgcolor='#FBF4E6',
        font=dict(family="Crimson Text,serif", color="#2C1A0E"),
        xaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882',
                   tickfont=dict(family="Crimson Text,serif"), range=[x_lo, x_hi]),
        yaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882',
                   tickfont=dict(family="Crimson Text,serif")),
        legend=dict(bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1,
                    font=dict(family="Crimson Text,serif"), orientation='v', x=1.01, y=1),
        margin=dict(l=8, r=8, t=42, b=8), height=370,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="padding-top:0.4rem;"><div class="sidebar-hdr">✦ CALCULATION HISTORY ✦</div></div>',
                unsafe_allow_html=True)
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
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="hist-empty">✦ No calculations yet.<br>Results will appear here after solving.</div>',
                    unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER + NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div class="vhdr">
        <div class="vhdr-name">DIOSAMABEL B. PENASO<br>BSCOMPE-2</div>
        <div class="vhdr-title">✦ &nbsp; NUMERICAL PROJECT &nbsp; ✦</div>
        <div class="vhdr-right">Numerical Methods<br>Analysis</div>
    </div>
    <div class="ornament">— ✦ ◆ ✦ —</div>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-strip">', unsafe_allow_html=True)
app_mode = st.radio("**Select Module**",
                    ["Root Finding Analysis", "Advanced Matrix Operations"],
                    horizontal=True, label_visibility="visible")
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 — ROOT FINDING
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.markdown('<div class="stitle">⊛ Root Finding Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Automatic interval scanning · All real roots detected · Complete iteration tables preserved</div>',
                unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 2.5])

    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚙ Parameters</div>', unsafe_allow_html=True)

        eq_str = st.text_input(
            "Equation f(x)",
            value="x^3 - 6*x + 2",
            help=(
                "Supported formats:\n"
                "  x^3 - 6*x + 2\n"
                "  ln(x) - 2  or  log(x) - 2\n"
                "  e^{-x} - x  or  exp(-x) - x\n"
                "  (x+2)*(x-3)\n"
                "  sin(x) - x/2\n"
                "  2x^2 - 5  (implicit multiplication OK)\n"
                "  f(x) = ... prefix is stripped automatically"
            )
        )

        method = st.selectbox("Algorithm", [
            "Incremental Search",
            "Bisection Method",
            "Regula-Falsi",
            "Newton-Raphson",
            "Secant Method",
        ])

        st.markdown("**Scanning Interval**")
        sc1, sc2 = st.columns(2)
        x_start   = sc1.number_input("Start", value=-10.0, format="%.2f")
        x_end     = sc2.number_input("End",   value=10.0,  format="%.2f")
        scan_step = st.number_input("Scan Step (Δ)", value=0.25, format="%.4f",
                                    help="Smaller = more roots found. Recommended: 0.1–0.5")

        tol      = st.number_input("Tolerance (Stopping Criterion)", value=0.001, format="%.6f")
        max_iter = st.number_input("Max Iterations", value=50, step=1)

        if method == "Incremental Search":
            xl_inc      = st.number_input("Initial Value (xl)", value=float(x_start), format="%.4f")
            delta_x_inc = st.number_input("Initial Increment (Δx)", value=0.5, format="%.4f")
        elif method in ["Bisection Method", "Regula-Falsi"]:
            xl_bf = st.number_input("Lower Bound (xl)",
                                    value=-0.5 if method == "Regula-Falsi" else 0.4, format="%.4f")
            xu_bf = st.number_input("Upper Bound (xu)",
                                    value=1.0  if method == "Regula-Falsi" else 0.6, format="%.4f")
        elif method == "Newton-Raphson":
            x0_nr = st.number_input("Initial Guess (xi)", value=-5.0, format="%.4f")
        elif method == "Secant Method":
            x_prev_s = st.number_input("First Guess (x_{i-1})", value=0.5, format="%.4f")
            x0_s     = st.number_input("Second Guess (x_i)",    value=5.0, format="%.4f")

        solve_btn = st.button("⊛  Calculate All Roots")

        # Quick examples panel
        st.markdown('<div class="panel-dark" style="margin-top:0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📋 Equation Examples</div>', unsafe_allow_html=True)
        examples = [
            ("Polynomial",    "x^3 - 6*x + 2"),
            ("Quartic",       "x^4 - 5*x^2 + 4"),
            ("Quadratic",     "x^2 - 9"),
            ("Logarithmic",   "ln(x) - 2"),
            ("Exponential",   "e^{-x} - x"),
            ("Transcendental","3*x + sin(x) - exp(x)"),
            ("Mixed",         "x^2 - 4*sin(x)"),
            ("Binomial",      "(x-2)*(x+3)"),
        ]
        for label, ex in examples:
            st.markdown(
                f'<span style="font-family:Cormorant Garamond,serif;color:#6B4226;font-size:0.83rem;">'
                f'<b style="color:#5C3317">{label}:</b> '
                f'<code style="background:#EDE0C4;padding:1px 5px;border-radius:4px;font-size:0.79rem;">'
                f'{ex}</code></span><br>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # /panel

    with col_results:
        if solve_btn:
            try:
                expr, x_sym = parse_equation(eq_str)
                f  = make_safe_f(expr, x_sym)
                df = make_safe_df(expr, x_sym)

                brackets = scan_intervals(f, x_start, x_end, scan_step)

                if not brackets:
                    st.warning(
                        f"No sign changes detected in [{x_start}, {x_end}] with step {scan_step}. "
                        "Try widening the interval or reducing the scan step."
                    )
                else:
                    all_roots, all_tables = [], []
                    prog = st.progress(0, text="Scanning for roots…")

                    for idx, (xl, xu) in enumerate(brackets):
                        prog.progress(
                            int((idx + 1) / len(brackets) * 100),
                            text=f"Solving bracket {idx+1}/{len(brackets)}: [{xl:.3f}, {xu:.3f}]"
                        )
                        try:
                            if method == "Incremental Search":
                                root, iters, ea, rows = method_incremental(f, xl, delta_x_inc, tol, max_iter)
                            elif method == "Bisection Method":
                                root, iters, ea, rows = method_bisection(f, xl, xu, tol, max_iter)
                            elif method == "Regula-Falsi":
                                root, iters, ea, rows = method_regula_falsi(f, xl, xu, tol, max_iter)
                            elif method == "Newton-Raphson":
                                root, iters, ea, rows = method_newton_raphson(f, df, (xl + xu) / 2.0, tol, max_iter)
                            elif method == "Secant Method":
                                root, iters, ea, rows = method_secant(f, xl, xu, tol, max_iter)

                            if root is not None:
                                froot = f(root)
                                if np.isnan(froot):
                                    continue
                                if not any(abs(root - ri['root']) < tol * 100 for ri in all_roots):
                                    all_roots.append({
                                        'root': root, 'f_root': float(froot),
                                        'iterations': iters, 'error': ea, 'method': method,
                                    })
                                    all_tables.append(rows)
                        except Exception:
                            continue

                    prog.empty()

                    if all_roots:
                        combined   = sorted(zip(all_roots, all_tables), key=lambda z: z[0]['root'])
                        all_roots  = [c[0] for c in combined]
                        all_tables = [c[1] for c in combined]

                    st.session_state.rf_all_roots  = all_roots
                    st.session_state.rf_all_tables = all_tables
                    st.session_state.rf_eq         = eq_str
                    st.session_state.rf_method     = method

                    if all_roots:
                        st.session_state.rf_fig = build_full_graph(f, eq_str, all_roots, x_start, x_end)
                        root_str = ", ".join(f"x≈{ri['root']:.6f}" for ri in all_roots)
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

            except ValueError as ve:
                st.error(str(ve))
            except Exception as e:
                st.error(f"Unexpected error: {e}")

        # ── DISPLAY RESULTS ──
        if st.session_state.rf_all_roots:
            all_roots  = st.session_state.rf_all_roots
            all_tables = st.session_state.rf_all_tables

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Roots Found", len(all_roots))
            m2.metric("Primary Root",      f"{all_roots[0]['root']:.8f}")
            m3.metric("Method",            st.session_state.rf_method)

            # Graph
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📈 Full Function Graph — All Roots</div>', unsafe_allow_html=True)
            st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Per-root expandable iteration tables
            for idx, (ri, tbl) in enumerate(zip(all_roots, all_tables)):
                ea_str = f"{ri['error']:.4e}" if isinstance(ri['error'], float) and ri['error'] else "—"
                with st.expander(
                    f"📊 Root {idx+1}  ·  x ≈ {ri['root']:.8f}  "
                    f"·  {ri['iterations']} iterations  ·  Ea = {ea_str}",
                    expanded=(idx == 0)
                ):
                    if tbl:
                        st.dataframe(pd.DataFrame(tbl), use_container_width=True)
                    else:
                        st.info("No iteration data for this root.")

        else:
            st.markdown("""
                <div class="panel" style="min-height:520px;">
                    <div class="placeholder-box">
                        ✦ Configure the parameters on the left<br>
                        and press <em>Calculate All Roots</em> to begin.<br><br>
                        The system will automatically scan the full interval,<br>
                        detect every root, and display the complete<br>
                        iteration table for each root found.<br><br>
                        <span style="font-size:0.88rem;">Supports: polynomial · ln · e^x · sin/cos · mixed</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 — ADVANCED MATRIX OPERATIONS (completely unchanged)
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    st.markdown('<div class="stitle">⊞ Advanced Matrix Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Input matrices using the interactive spreadsheets and execute linear algebra operations instantly.</div>',
                unsafe_allow_html=True)

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

                result, ans_str, det_val = None, "", None

                if op == "Addition":
                    result  = A + B;            ans_str = "Matrix addition complete."
                elif op == "Multiplication":
                    result  = np.matmul(A, B);  ans_str = "Matrix product computed."
                elif op == "Transpose":
                    result  = A.T;              ans_str = "Matrix transposed."
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
                    "op": op, "result": result, "det_val": det_val, "ans_str": ans_str
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
