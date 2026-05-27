import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import re
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
    "rf_results":      [],
    "rf_root":         None,
    "rf_iterations":   0,
    "rf_error":        0,
    "rf_fig":          None,
    "rf_eq":           "",
    "rf_method":       "",
    "rf_all_roots":    [],
    "rf_selected_idx": 0,
    "mx_result":       None,
    "mx_op":           "",
    "history":         [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS  —  VINTAGE BROWN ACADEMIC DASHBOARD  (UNCHANGED)
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
.vhdr-name  { font-family:'Cormorant Garamond',serif; font-size:0.88rem; color:var(--gold); letter-spacing:0.07em; line-height:1.55; font-style:italic; text-shadow:0 1px 4px rgba(0,0,0,0.5); min-width:185px; }
.vhdr-title { font-family:'Playfair Display',serif; font-size:1.95rem; font-weight:700; color:#F5E6C8; letter-spacing:0.25em; text-align:center; text-shadow:0 2px 8px rgba(0,0,0,0.55); flex:1; }
.vhdr-right { font-family:'Cormorant Garamond',serif; font-size:0.8rem; color:#B8936A; text-align:right; letter-spacing:0.05em; line-height:1.6; min-width:185px; }

.ornament { text-align:center; color:#9B7245; letter-spacing:0.55em; margin:0.35rem 0 0.55rem 0; font-size:0.95rem; user-select:none; }

.nav-strip {
    background: linear-gradient(135deg,#EDE0C4 0%,#E2D0AA 50%,#EDE0C4 100%);
    border:1.5px solid var(--border); border-radius:11px; padding:0.6rem 1.3rem 0.45rem 1.3rem;
    margin-bottom:0.85rem; box-shadow:0 2px 12px var(--shadow),inset 0 1px 0 rgba(255,255,255,0.45);
}

.stitle { font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:700; color:var(--brown-dk); border-bottom:2px solid var(--brown-lt); padding-bottom:0.28rem; margin-bottom:0.75rem; letter-spacing:0.04em; }
.ssub   { font-family:'Cormorant Garamond',serif; font-size:1rem; color:#6B4226; font-style:italic; margin-bottom:0.85rem; }

.panel {
    background: linear-gradient(160deg,var(--cream) 0%,var(--cream2) 100%);
    border:1.5px solid var(--border); border-radius:12px; padding:1.1rem 1.25rem;
    box-shadow:3px 4px 18px var(--shadow),inset 0 1px 0 rgba(255,255,255,0.55);
    margin-bottom:0.75rem;
}
.panel-dark { background:linear-gradient(160deg,#EDE0C4 0%,#E5D4AE 100%); border:1.5px solid var(--border2); border-radius:12px; padding:1rem 1.25rem; box-shadow:3px 4px 18px var(--shadow); margin-bottom:0.75rem; }
.panel-title { font-family:'Playfair Display',serif; font-size:0.98rem; font-weight:600; color:var(--brown-md); letter-spacing:0.04em; margin-bottom:0.5rem; display:flex; align-items:center; gap:0.4rem; }

div[data-testid="stRadio"] label > div p { font-family:'Playfair Display',serif !important; font-size:0.97rem !important; color:var(--brown-dk) !important; font-weight:600 !important; }
.stSelectbox > label, .stNumberInput > label, .stTextInput > label { font-family:'Crimson Text',serif !important; color:#4A2A12 !important; font-size:0.95rem !important; font-weight:600 !important; letter-spacing:0.02em !important; }
.stSelectbox [data-baseweb="select"] > div, .stTextInput input, .stNumberInput input { border:1.5px solid var(--border) !important; border-radius:7px !important; background-color:var(--cream) !important; color:var(--brown-dk) !important; font-family:'Crimson Text',serif !important; font-size:0.97rem !important; box-shadow:inset 0 1px 5px rgba(59,31,12,0.07) !important; transition:border-color 0.2s,box-shadow 0.2s !important; }
.stSelectbox [data-baseweb="select"] > div:focus-within, .stTextInput input:focus, .stNumberInput input:focus { border-color:var(--brown-lt) !important; box-shadow:0 0 0 2.5px rgba(139,94,60,0.2) !important; }

.stButton > button { width:100%; border-radius:8px; background:linear-gradient(135deg,var(--brown-md) 0%,var(--brown-lt) 55%,#7A4F2E 100%); color:#F5E6C8; font-family:'Playfair Display',serif; font-size:0.97rem; font-weight:700; border:1px solid #9B7245; letter-spacing:0.09em; padding:0.55rem 1rem; box-shadow:0 3px 14px var(--shadow-dk),inset 0 1px 0 rgba(255,255,255,0.1); transition:all 0.25s ease; text-shadow:0 1px 3px rgba(0,0,0,0.35); }
.stButton > button:hover { background:linear-gradient(135deg,#1E0F06 0%,var(--brown-md) 100%); transform:translateY(-1.5px); box-shadow:0 5px 20px var(--shadow-dk); color:var(--gold-lt); }
.stButton > button:active { transform:translateY(0px); }

[data-testid="metric-container"] { background:linear-gradient(135deg,#EDE0C4,#E2CFA8) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; padding:0.7rem 0.9rem !important; box-shadow:2px 3px 11px var(--shadow) !important; }
[data-testid="stMetricLabel"] p { font-family:'Cormorant Garamond',serif !important; color:#6B4226 !important; font-size:0.78rem !important; letter-spacing:0.08em !important; text-transform:uppercase !important; }
[data-testid="stMetricValue"] { font-family:'Playfair Display',serif !important; color:var(--brown-dk) !important; font-size:1.45rem !important; }

[data-testid="stDataFrame"] { border:1.5px solid var(--border) !important; border-radius:9px !important; overflow:hidden !important; }
[data-testid="stDataFrame"] table { font-family:'Crimson Text',serif !important; }
[data-testid="stDataFrame"] th { background-color:#5C3317 !important; color:#F5E6C8 !important; font-family:'Playfair Display',serif !important; font-size:0.82rem !important; letter-spacing:0.05em !important; }
[data-testid="stDataFrame"] tr:hover { background-color:#EDE0C4 !important; }

[data-testid="stInfo"]    { background-color:#EDE0C4 !important; border-left:4px solid var(--brown-lt) !important; border-radius:7px !important; font-family:'Crimson Text',serif !important; }
[data-testid="stSuccess"] { background-color:#E4D8C0 !important; border-left:4px solid var(--brown-md) !important; border-radius:7px !important; font-family:'Crimson Text',serif !important; }
[data-testid="stAlert"]   { font-family:'Crimson Text',serif !important; border-radius:7px !important; }

hr { border:none !important; border-top:1.5px solid var(--border) !important; margin:0.6rem 0 !important; }

[data-testid="stSidebar"] { background:linear-gradient(180deg,#1E0F06 0%,#2C1A0E 40%,#3B2210 100%) !important; border-right:2px solid #5C3317 !important; }
[data-testid="stSidebar"] * { color:#E8D5B0 !important; }
[data-testid="stSidebar"] .stButton > button { background:linear-gradient(135deg,#3B2210,#5C3317) !important; border-color:#7A4F2E !important; color:#F5E6C8 !important; font-size:0.85rem !important; }
[data-testid="stSidebar"] .stButton > button:hover { background:linear-gradient(135deg,#5C3317,#8B5E3C) !important; }

.hist-card { background:rgba(92,51,23,0.35); border:1px solid rgba(200,169,122,0.35); border-radius:9px; padding:0.7rem 0.85rem; margin-bottom:0.6rem; box-shadow:0 2px 8px rgba(0,0,0,0.25); transition:background 0.2s; }
.hist-card:hover { background:rgba(92,51,23,0.55); }
.hist-method { font-family:'Playfair Display',serif; font-size:0.82rem; font-weight:700; color:#E8C98A; letter-spacing:0.05em; margin-bottom:0.2rem; }
.hist-eq     { font-family:'Crimson Text',serif; font-size:0.88rem; color:#D4BC96; font-style:italic; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:0.15rem; }
.hist-ans    { font-family:'Playfair Display',serif; font-size:0.9rem; color:#F5E6C8; font-weight:600; }
.hist-ts     { font-family:'Cormorant Garamond',serif; font-size:0.75rem; color:#9B7A55; margin-top:0.2rem; letter-spacing:0.04em; }
.hist-empty  { text-align:center; padding:1.5rem 0.5rem; font-family:'Cormorant Garamond',serif; font-size:0.95rem; font-style:italic; color:#7A5A3A; }
.sidebar-hdr { font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:700; color:#E8C98A; letter-spacing:0.1em; text-align:center; padding:0.2rem 0 0.6rem 0; border-bottom:1px solid rgba(200,169,122,0.35); margin-bottom:0.7rem; }

.placeholder-box { text-align:center; padding:2.5rem 1rem; color:#9B7245; font-family:'Playfair Display',serif; font-size:1rem; font-style:italic; line-height:1.7; }

/* ── Root badges ── */
.root-badge {
    display:inline-block; padding:0.35rem 0.85rem; border-radius:20px;
    font-family:'Playfair Display',serif; font-size:0.82rem; font-weight:600;
    margin:0.2rem 0.2rem; letter-spacing:0.04em;
    border:1.5px solid var(--border2);
    background:linear-gradient(135deg,#EDE0C4,#E2CFA8);
    color:var(--brown-dk);
}
.root-badge-conv  { border-color:#5C8A3C; background:linear-gradient(135deg,#E8F0DC,#D5E8C0); }
.root-badge-nconv { border-color:#B85C3C; background:linear-gradient(135deg,#F0E0DC,#E8D0C0); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ENHANCED EQUATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

ROOT_COLORS = [
    '#8B1A1A', '#1A5C8B', '#2C7A3A', '#7A5C1A',
    '#5C1A7A', '#1A7A6C', '#7A2C1A', '#1A3C7A'
]

def preprocess_equation(eq_str: str) -> str:
    """
    Convert user-friendly notation to valid SymPy/Python syntax.
    Handles: ln, e^x, e^(expr), implicit multiplication (2x, 3(x+1)), ^→**
    """
    eq = eq_str.strip()

    # ── 1. ln → log (SymPy natural log is log())
    eq = re.sub(r'\bln\b', 'log', eq)

    # ── 2. e^(expr) → exp(expr)  [complex exponent in parens first]
    eq = re.sub(r'\be\^(\([^)]*\))', r'exp\1', eq)
    # ── 2b. e^simple_term (e^x, e^-x, e^2, e^n)
    eq = re.sub(r'\be\^(-?[a-zA-Z_]\w*)', r'exp(\1)', eq)
    eq = re.sub(r'\be\^(-?\d+(?:\.\d*)?)', r'exp(\1)', eq)

    # ── 3. Implicit multiplication
    # digit before letter or opening paren: 2x→2*x, 2(→2*(
    eq = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', eq)
    # closing paren before opening paren or alphanumeric: )(→)*(
    eq = re.sub(r'\)\(', ')*(', eq)
    eq = re.sub(r'\)([a-zA-Z\d])', r')*\1', eq)

    # ── 4. ^ → **
    eq = eq.replace('^', '**')

    return eq


def validate_and_parse(eq_str: str):
    """
    Returns (ok: bool, message: str, f_callable, df_callable, normalized_str)
    """
    try:
        normalized = preprocess_equation(eq_str)
        x = sp.Symbol('x')
        local_dict = {
            'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'sqrt': sp.sqrt, 'pi': sp.pi, 'e': sp.E,
            'abs': sp.Abs, 'Abs': sp.Abs,
        }
        expr   = sp.sympify(normalized, locals=local_dict)
        dexpr  = sp.diff(expr, x)
        # lambdify with numpy backend
        modules = ['numpy', {'log': np.log, 'exp': np.exp, 'sqrt': np.sqrt,
                              'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 'Abs': np.abs}]
        f_func  = sp.lambdify(x, expr,  modules=modules)
        df_func = sp.lambdify(x, dexpr, modules=modules)
        # sanity test
        _ = float(f_func(1.5))
        return True, normalized, f_func, df_func
    except Exception as err:
        return False, str(err), None, None


def safe_eval(func, xval) -> float | None:
    """Evaluate func at xval; return None if undefined/non-finite."""
    try:
        v = float(func(xval))
        return v if np.isfinite(v) else None
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
#  AUTOMATIC ROOT / BRACKET SCANNER
# ══════════════════════════════════════════════════════════════════════════════

def scan_brackets(f_func, xmin: float, xmax: float, n_points: int = 2000) -> list:
    """
    Scan [xmin, xmax] and return a list of [a, b] intervals where a sign change
    is detected (each bracket likely contains exactly one root).
    """
    xs = np.linspace(xmin, xmax, n_points)
    brackets, prev_x, prev_fy = [], None, None

    for xi in xs:
        fyi = safe_eval(f_func, xi)
        if fyi is None:
            prev_x, prev_fy = None, None
            continue
        if prev_fy is not None:
            if prev_fy * fyi < 0:
                brackets.append([float(prev_x), float(xi)])
            elif abs(fyi) < 1e-10 and abs(prev_fy) > 1e-8:
                brackets.append([float(xi) - (xi - prev_x), float(xi) + (xi - prev_x)])
        prev_x, prev_fy = xi, fyi

    # Deduplicate brackets whose midpoints are very close
    step = (xmax - xmin) / n_points
    unique = []
    for b in brackets:
        mid = (b[0] + b[1]) / 2
        if not any(abs((u[0] + u[1]) / 2 - mid) < step * 4 for u in unique):
            unique.append(b)

    return unique


# ══════════════════════════════════════════════════════════════════════════════
#  NUMERICAL METHODS  (each returns root, rows_list, final_err, converged, msg)
# ══════════════════════════════════════════════════════════════════════════════

def do_bisection(f, xl, xu, tol, max_iter):
    fxl0 = safe_eval(f, xl)
    fxu0 = safe_eval(f, xu)
    if fxl0 is None or fxu0 is None:
        return None, [], None, False, "Cannot evaluate f at interval endpoints."
    if fxl0 * fxu0 > 0:
        return None, [], None, False, "f(xₗ)·f(xᵤ) must be < 0 (opposite signs required)."

    rows, _xl, _xu, prev_xr = [], xl, xu, None

    for i in range(int(max_iter)):
        xr   = (_xl + _xu) / 2.0
        fxl  = safe_eval(f, _xl) or 0.0
        fxr  = safe_eval(f, xr)  or 0.0
        prod = fxl * fxr
        ea   = abs((xr - prev_xr) / xr) * 100 if prev_xr is not None and xr != 0 else None

        rows.append({
            "Iteration":  i + 1,
            "x_l":        round(_xl, 7),
            "x_r":        round(xr,  7),
            "x_u":        round(_xu, 7),
            "f(x_l)":     round(fxl, 7),
            "f(x_r)":     round(fxr, 7),
            "|E_a| %":    round(ea, 6) if ea is not None else "—",
            "f(xl)·f(xr)": "< 0" if prod < 0 else "> 0",
            "Subinterval": "[xₗ,xᵣ]" if prod < 0 else "[xᵣ,xᵤ]",
        })

        if (ea is not None and ea < tol) or abs(fxr) < 1e-12:
            return xr, rows, ea, True, ""

        if prod < 0:
            _xu = xr
        else:
            _xl = xr
        prev_xr = xr

    last_xr = rows[-1]["x_r"] if rows else (_xl + _xu) / 2
    return last_xr, rows, None, False, "Max iterations reached."


def do_regula_falsi(f, xl, xu, tol, max_iter):
    fxl0 = safe_eval(f, xl)
    fxu0 = safe_eval(f, xu)
    if fxl0 is None or fxu0 is None:
        return None, [], None, False, "Cannot evaluate f at interval endpoints."
    if fxl0 * fxu0 > 0:
        return None, [], None, False, "f(xₗ)·f(xᵤ) must be < 0."

    rows, _xl, _xu, prev_xr = [], xl, xu, None

    for i in range(int(max_iter)):
        fxl = safe_eval(f, _xl) or 0.0
        fxu = safe_eval(f, _xu) or 0.0
        if abs(fxl - fxu) < 1e-15:
            break

        xr  = (_xu * fxl - _xl * fxu) / (fxl - fxu)
        fxr = safe_eval(f, xr) or 0.0
        prod = fxl * fxr
        ea  = abs((xr - prev_xr) / xr) if prev_xr is not None and xr != 0 else None

        rows.append({
            "No. of Iter": i + 1,
            "x_L":         round(_xl, 7),
            "x_U":         round(_xu, 7),
            "x_R":         round(xr,  7),
            "E_a":         round(ea, 8) if ea is not None else "—",
            "f(x_L)":      round(fxl, 7),
            "f(x_U)":      round(fxu, 7),
            "f(x_R)":      round(fxr, 7),
            "f(xL)·f(xR)": "< 0" if prod < 0 else "> 0",
        })

        if (ea is not None and ea < tol) or abs(fxr) < 1e-12:
            return xr, rows, ea, True, ""

        if prod < 0:
            _xu = xr
        else:
            _xl = xr
        prev_xr = xr

    last_xr = rows[-1]["x_R"] if rows else (_xl + _xu) / 2
    return last_xr, rows, None, False, "Max iterations reached."


def do_newton_raphson(f, df, x0_val, tol, max_iter):
    xi = float(x0_val)
    rows = []

    fxi  = safe_eval(f,  xi)
    dfxi = safe_eval(df, xi)
    if fxi is None or dfxi is None:
        return None, [], None, False, "Cannot evaluate f or f′ at x₀."

    rows.append({"Iteration": 0, "x_i": round(xi, 7), "E_a": "—",
                 "f(x)": round(fxi, 8), "f'(x)": round(dfxi, 8)})

    for i in range(int(max_iter)):
        fxi  = safe_eval(f,  xi)
        dfxi = safe_eval(df, xi)
        if fxi is None or dfxi is None:
            break
        if abs(dfxi) < 1e-14:
            return None, rows, None, False, "Derivative became zero — Newton-Raphson fails."

        xi_new = xi - fxi / dfxi
        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        xi = xi_new

        fxi_n  = safe_eval(f,  xi) or 0.0
        dfxi_n = safe_eval(df, xi) or 0.0
        rows.append({"Iteration": i + 1, "x_i": round(xi, 7), "E_a": round(ea, 8),
                     "f(x)": round(fxi_n, 8), "f'(x)": round(dfxi_n, 8)})

        if ea < tol or abs(fxi_n) < 1e-12:
            return xi, rows, ea, True, ""

    last_xi = rows[-1]["x_i"] if rows else x0_val
    return last_xi, rows, None, False, "Max iterations reached."


def do_secant(f, xp_val, x0_val, tol, max_iter):
    xi_prev, xi = float(xp_val), float(x0_val)
    rows = []

    for i in range(int(max_iter)):
        fxi      = safe_eval(f, xi)
        fxi_prev = safe_eval(f, xi_prev)
        if fxi is None or fxi_prev is None:
            break
        if abs(fxi - fxi_prev) < 1e-15:
            break

        xi_new = xi - (fxi * (xi - xi_prev)) / (fxi - fxi_prev)
        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        fxi_new = safe_eval(f, xi_new) or 0.0

        rows.append({
            "Iteration":   i + 1,
            "x_{i-1}":     round(xi_prev, 7),
            "x_i":         round(xi,      7),
            "x_{i+1}":     round(xi_new,  7),
            "E_a":         round(ea, 8),
            "f(x_{i-1})":  round(fxi_prev, 7),
            "f(x_i)":      round(fxi,      7),
            "f(x_{i+1})":  round(fxi_new,  7),
        })

        xi_prev, xi = xi, xi_new
        if ea < tol or abs(fxi_new) < 1e-12:
            return xi_new, rows, ea, True, ""

    last = rows[-1]["x_{i+1}"] if rows else x0_val
    return last, rows, None, False, "Max iterations reached."


def do_incremental(f, xl_val, dx_val, tol, max_iter):
    curr_xl = float(xl_val)
    curr_dx = float(dx_val)
    rows    = []

    for i in range(int(max_iter)):
        curr_xu = curr_xl + curr_dx
        fxl = safe_eval(f, curr_xl)
        fxu = safe_eval(f, curr_xu)

        if fxl is None or fxu is None:
            curr_xl = curr_xu
            continue

        prod = fxl * fxu
        rows.append({
            "Iteration":    i + 1,
            "x_l":          round(curr_xl, 6),
            "Δx":           round(curr_dx, 6),
            "x_u":          round(curr_xu, 6),
            "f(x_l)":       round(fxl, 6),
            "f(x_u)":       round(fxu, 6),
            "f(xl)·f(xu)":  "> 0" if prod > 0 else "< 0",
            "Remark":       "Next interval →" if prod > 0 else "Root bracketed ✦",
        })

        if abs(fxu) < tol or curr_dx < tol / 10:
            return curr_xu, rows, abs(fxu), True, ""

        if np.isfinite(prod) and prod > 0:
            curr_xl = curr_xu
        else:
            curr_dx /= 10.0

    last_xu = rows[-1]["x_u"] if rows else xl_val
    return last_xu, rows, None, False, "Max iterations reached."


# ══════════════════════════════════════════════════════════════════════════════
#  ORCHESTRATE MULTI-ROOT SOLVE
# ══════════════════════════════════════════════════════════════════════════════

def solve_all_roots(method, f_func, df_func,
                    brackets, xl, xu, x_prev, x0, delta_x, tol, max_iter):
    """
    Apply `method` to every detected bracket and return a deduplicated list of
    {root, rows, error, converged, bracket, n_iters}.
    Falls back to user-supplied parameters if no brackets were found.
    """
    all_roots_data = []

    def apply_method(a, b):
        mid = (a + b) / 2.0
        if method == "Bisection Method":
            return do_bisection(f_func, a, b, tol, max_iter)
        elif method == "Regula-Falsi":
            return do_regula_falsi(f_func, a, b, tol, max_iter)
        elif method == "Newton-Raphson":
            return do_newton_raphson(f_func, df_func, mid, tol, max_iter)
        elif method == "Secant Method":
            return do_secant(f_func, a, b, tol, max_iter)
        elif method == "Incremental Search":
            return do_incremental(f_func, a, delta_x, tol, max_iter)
        return None, [], None, False, "Unknown method"

    for br in brackets:
        root, rows, err, conv, msg = apply_method(br[0], br[1])
        if root is not None and np.isfinite(root):
            if not any(abs(r['root'] - root) < 1e-4 for r in all_roots_data):
                all_roots_data.append({
                    'root': float(root), 'rows': rows, 'error': err,
                    'converged': conv, 'bracket': br, 'n_iters': len(rows),
                    'msg': msg,
                })

    # Fallback: no brackets or all failed → use user params
    if not all_roots_data:
        if method == "Bisection Method":
            root, rows, err, conv, msg = do_bisection(f_func, xl, xu, tol, max_iter)
        elif method == "Regula-Falsi":
            root, rows, err, conv, msg = do_regula_falsi(f_func, xl, xu, tol, max_iter)
        elif method == "Newton-Raphson":
            root, rows, err, conv, msg = do_newton_raphson(f_func, df_func, x0, tol, max_iter)
        elif method == "Secant Method":
            root, rows, err, conv, msg = do_secant(f_func, x_prev, x0, tol, max_iter)
        elif method == "Incremental Search":
            root, rows, err, conv, msg = do_incremental(f_func, xl, delta_x, tol, max_iter)
        else:
            root = None

        if root is not None and np.isfinite(root):
            all_roots_data.append({
                'root': float(root), 'rows': rows, 'error': err,
                'converged': conv, 'bracket': [xl, xu], 'n_iters': len(rows),
                'msg': msg,
            })

    return all_roots_data


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD PLOTLY FIGURE  (vintage palette + all roots marked)
# ══════════════════════════════════════════════════════════════════════════════

def build_figure(eq_str, f_func, all_roots_data, scan_min, scan_max):
    x_lo = scan_min - 0.5
    x_hi = scan_max + 0.5
    xs   = np.linspace(x_lo, x_hi, 800)
    ys   = np.array([safe_eval(f_func, v) for v in xs], dtype=object)

    # Break curve at None (domain gaps like ln(x))
    x_plot, y_plot = [], []
    for xi, yi in zip(xs, ys):
        if yi is None or abs(float(yi if yi is not None else 0)) > 150:
            x_plot.append(None)
            y_plot.append(None)
        else:
            x_plot.append(float(xi))
            y_plot.append(float(yi))

    fig = go.Figure()

    # Function curve
    fig.add_trace(go.Scatter(
        x=x_plot, y=y_plot,
        mode='lines', name=f'f(x) = {eq_str}',
        line=dict(color='#5C3317', width=2.5),
        connectgaps=False,
    ))

    # Zero axis
    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.3)
    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.0)

    # Root markers
    for idx, rd in enumerate(all_roots_data):
        root_val = rd['root']
        color    = ROOT_COLORS[idx % len(ROOT_COLORS)]
        conv_sym = "✓" if rd['converged'] else "⚠"
        fig.add_trace(go.Scatter(
            x=[root_val], y=[0],
            mode='markers+text',
            name=f'Root {idx+1}: x ≈ {root_val:.6f} {conv_sym}',
            marker=dict(color=color, size=14, symbol='circle',
                        line=dict(color='#2C1A0E', width=2)),
            text=[f'x{idx+1}={root_val:.4f}'],
            textposition='top center',
            textfont=dict(size=10, color=color, family='Playfair Display, serif'),
        ))
        # Vertical guide line
        fig.add_vline(x=root_val, line_dash="dot",
                      line_color=color, line_width=1.0, opacity=0.55)

    fig.update_layout(
        title=dict(text=f"f(x) = {eq_str}",
                   font=dict(family="Playfair Display, serif", size=14, color="#2C1A0E")),
        xaxis_title="x", yaxis_title="f(x)",
        hovermode="x unified",
        plot_bgcolor='#FBF4E6', paper_bgcolor='#FBF4E6',
        font=dict(family="Crimson Text, serif", color="#2C1A0E"),
        xaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882',
                   zerolinecolor='#C4A882', tickfont=dict(family="Crimson Text, serif")),
        yaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882',
                   zerolinecolor='#C4A882', tickfont=dict(family="Crimson Text, serif"),
                   range=[-50, 50]),
        legend=dict(bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1,
                    font=dict(family="Crimson Text, serif")),
        margin=dict(l=8, r=8, t=42, b=8),
        height=330,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — CALCULATION HISTORY  (UNCHANGED)
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
#  HEADER  (UNCHANGED)
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
#  NAVIGATION  (UNCHANGED)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="nav-strip">', unsafe_allow_html=True)
app_mode = st.radio(
    "**Select Module**",
    ["Root Finding Analysis", "Advanced Matrix Operations"],
    horizontal=True,
    label_visibility="visible",
)
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 — ENHANCED ROOT FINDING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.title("Root Finding Analysis")
    st.markdown("Analyze equations and find **all** roots automatically using numerical methods.")

    col_input, col_results = st.columns([1, 2.5])

    # ─────────────────────── LEFT — PARAMETERS ───────────────────────────────
    with col_input:
        st.subheader("Parameters")

        eq_str = st.text_input(
            "Equation  f(x)",
            value="x^3 - 6*x^2 + 11*x - 6",
            help=(
                "Supports: x^n · ln(x) · e^x · exp(x) · sin(x) · cos(x) · sqrt(x)\n"
                "Implicit mult: 2x → 2*x · 3(x+1) → 3*(x+1)"
            ),
        )

        method = st.selectbox(
            "Algorithm",
            ["Incremental Search", "Bisection Method", "Regula-Falsi",
             "Newton-Raphson", "Secant Method"],
        )

        # ── Method-specific inputs (same layout as original) ──
        if method == "Incremental Search":
            xl      = st.number_input("Initial Value (xl)", value=0.0,  format="%.4f")
            delta_x = st.number_input("Step Size (Δx)",     value=0.5,  format="%.4f")
            xu, x_prev, x0 = xl + delta_x, xl, xl + delta_x
        elif method in ["Bisection Method", "Regula-Falsi"]:
            xl = st.number_input("Lower Bound (xl)", value=-0.5 if method == "Regula-Falsi" else 0.4, format="%.4f")
            xu = st.number_input("Upper Bound (xu)", value= 1.0 if method == "Regula-Falsi" else 0.6, format="%.4f")
            delta_x, x_prev, x0 = 0.5, xl, (xl + xu) / 2
        elif method == "Newton-Raphson":
            x0   = st.number_input("Initial Guess (xᵢ)", value=0.5, format="%.4f")
            xl, xu, x_prev, delta_x = x0 - 1, x0 + 1, x0 - 0.5, 0.5
        elif method == "Secant Method":
            x_prev = st.number_input("First Guess  (xᵢ₋₁)", value=0.5, format="%.4f")
            x0     = st.number_input("Second Guess (xᵢ)",   value=1.5, format="%.4f")
            xl, xu, delta_x = min(x_prev, x0), max(x_prev, x0), 0.5

        st.markdown("---")
        st.markdown("**Auto Root-Detection Range**")
        sc1, sc2 = st.columns(2)
        scan_min = sc1.number_input("Scan From", value=-10.0, format="%.2f",
                                    help="Left bound for automatic root scanning")
        scan_max = sc2.number_input("Scan To",   value= 10.0, format="%.2f",
                                    help="Right bound for automatic root scanning")

        tol      = st.number_input("Tolerance (Stopping Criterion)", value=0.0001, format="%.6f")
        max_iter = st.number_input("Max Iterations", value=100, step=10)
        solve_btn = st.button("✦  Calculate Root(s)")

    # ─────────────────────── RIGHT — RESULTS ─────────────────────────────────
    with col_results:

        if solve_btn:
            # ── Validate equation ──────────────────────────────────────────
            ok, norm_or_err, f_func, df_func = validate_and_parse(eq_str)

            if not ok:
                st.error(
                    f"**Invalid equation syntax.**  \n"
                    f"Details: `{norm_or_err}`  \n\n"
                    "**Tips:** Use `*` for multiplication (e.g. `2*x`), `^` or `**` for powers, "
                    "`ln(x)` or `log(x)` for natural log, `exp(x)` or `e^x` for exponential."
                )
            else:
                with st.spinner("Scanning for roots…"):
                    # ── Auto-scan for all sign-change brackets ─────────────
                    brackets = scan_brackets(f_func, scan_min, scan_max, n_points=2000)

                    # ── Apply chosen method to every bracket ───────────────
                    all_roots_data = solve_all_roots(
                        method, f_func, df_func,
                        brackets, xl, xu, x_prev, x0, delta_x, tol, max_iter,
                    )

                if all_roots_data:
                    st.session_state.rf_all_roots    = all_roots_data
                    st.session_state.rf_root         = all_roots_data[0]['root']
                    st.session_state.rf_results      = all_roots_data[0]['rows']
                    st.session_state.rf_iterations   = all_roots_data[0]['n_iters']
                    st.session_state.rf_error        = all_roots_data[0]['error']
                    st.session_state.rf_eq           = eq_str
                    st.session_state.rf_method       = method
                    st.session_state.rf_selected_idx = 0

                    # Build figure
                    st.session_state.rf_fig = build_figure(
                        eq_str, f_func, all_roots_data, scan_min, scan_max
                    )

                    # History entry
                    root_summary = ", ".join(
                        f"x≈{r['root']:.6f}" for r in all_roots_data
                    )
                    st.session_state.history.append({
                        "type":      "Root Finding",
                        "method":    method,
                        "equation":  f"f(x) = {eq_str}",
                        "answer":    f"{len(all_roots_data)} root(s): {root_summary}",
                        "timestamp": datetime.now().strftime("%b %d, %Y  %H:%M:%S"),
                    })
                    st.toast(
                        f"Found {len(all_roots_data)} root(s)!",
                        icon="✅" if all_roots_data[0]['converged'] else "⚠️",
                    )
                else:
                    st.warning(
                        "No roots found in the specified scan range with the selected method.  \n"
                        "Try widening the scan range or choosing a different method."
                    )

        # ── RENDER STORED RESULTS ──────────────────────────────────────────
        if st.session_state.rf_all_roots:
            all_roots_data = st.session_state.rf_all_roots
            n_roots        = len(all_roots_data)
            sel_idx        = st.session_state.rf_selected_idx

            # ── DETECTED ROOTS PANEL ───────────────────────────────────────
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="panel-title">🎯 Detected Roots — '
                f'{n_roots} root{"s" if n_roots != 1 else ""} found</div>',
                unsafe_allow_html=True,
            )

            badge_html = ""
            for idx, rd in enumerate(all_roots_data):
                cls   = "root-badge-conv" if rd['converged'] else "root-badge-nconv"
                sym   = "✓" if rd['converged'] else "⚠"
                color = ROOT_COLORS[idx % len(ROOT_COLORS)]
                badge_html += (
                    f'<span class="root-badge {cls}" '
                    f'style="border-color:{color};">'
                    f'Root&nbsp;{idx+1}:&nbsp;x&nbsp;≈&nbsp;{rd["root"]:.8f}&nbsp;{sym}'
                    f'</span>'
                )
            st.markdown(badge_html, unsafe_allow_html=True)

            # Detail table for all roots
            summary_rows = []
            for idx, rd in enumerate(all_roots_data):
                err_str = (f"{rd['error']:.2e}" if isinstance(rd['error'], float) else "—")
                summary_rows.append({
                    "#":          idx + 1,
                    "Root Value": round(rd['root'], 10),
                    "Iterations": rd['n_iters'],
                    "Error (Eₐ)": err_str,
                    "Converged":  "Yes ✓" if rd['converged'] else "No ⚠",
                    "Bracket":    f"[{rd['bracket'][0]:.4f}, {rd['bracket'][1]:.4f}]",
                    "Method":     st.session_state.rf_method,
                })
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── METRICS for primary / selected root ───────────────────────
            rd  = all_roots_data[sel_idx]
            m1, m2, m3 = st.columns(3)
            m1.metric("Calculated Root", f"{rd['root']:.8f}")
            m2.metric("Total Iterations", rd['n_iters'])
            m3.metric(
                "Final Error (Eₐ)",
                f"{rd['error']:.4e}" if isinstance(rd['error'], float) else "N/A",
            )
            st.divider()

            # ── PLOTLY GRAPH ──────────────────────────────────────────────
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📈 Function Graph — All Roots</div>',
                        unsafe_allow_html=True)
            if st.session_state.rf_fig:
                st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── ITERATION TABLE ───────────────────────────────────────────
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            table_header = "📊 Iteration History"
            if n_roots > 1:
                tab_options  = [
                    f"Root {i+1}: x≈{r['root']:.6f}" for i, r in enumerate(all_roots_data)
                ]
                chosen_label = st.selectbox(
                    "View iteration table for:",
                    tab_options,
                    index=sel_idx,
                    key="root_select",
                )
                sel_idx = tab_options.index(chosen_label)
                st.session_state.rf_selected_idx = sel_idx
                rd = all_roots_data[sel_idx]
                table_header = f"📊 Iteration History — Root {sel_idx+1}"

            st.markdown(f'<div class="panel-title">{table_header}</div>',
                        unsafe_allow_html=True)

            if rd['rows']:
                st.dataframe(pd.DataFrame(rd['rows']), use_container_width=True, height=280)
                conv_msg = (
                    f"✅ Converged in {rd['n_iters']} iteration(s). "
                    f"Root ≈ {rd['root']:.10f}. "
                    f"Final Eₐ = {rd['error']:.4e}" if isinstance(rd['error'], float) and rd['converged']
                    else f"⚠️ {rd.get('msg','Max iterations reached.')}"
                )
                if rd['converged']:
                    st.success(conv_msg)
                else:
                    st.warning(conv_msg)
            else:
                st.info("No iteration data available for this root.")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
                <div class="panel" style="min-height:540px;">
                    <div class="placeholder-box">
                        ✦ Configure the parameters on the left<br>
                        and press <em>Calculate Root(s)</em> to begin.<br><br>
                        The solver will automatically scan for<br>
                        all roots in the specified range.<br><br>
                        Supports: polynomials · ln(x) · e^x · sin/cos
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 — ADVANCED MATRIX OPERATIONS  (UNCHANGED)
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    import numpy as np

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
                with st.spinner("Processing…"):
                    time.sleep(0.25)

                result, ans_str, det_val = None, "", None

                if op == "Addition":
                    result  = A + B;             ans_str = "Matrix addition complete."
                elif op == "Multiplication":
                    result  = np.matmul(A, B);   ans_str = "Matrix product computed."
                elif op == "Transpose":
                    result  = A.T;               ans_str = "Matrix transposed."
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
            st.markdown(f'<div class="panel-title">⊞ Result — {r["op"]}</div>',
                        unsafe_allow_html=True)
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
