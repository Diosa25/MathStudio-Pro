import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NumerixPro — Root Finder",
    page_icon="∿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k, v in {
    "results": [], "history": [], "eq_valid": True,
    "last_eq": "", "last_fig": None, "compare_data": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── TOKENS ── */
:root {
  --bg:       #0A0E1A;
  --bg1:      #0F1526;
  --bg2:      #141C31;
  --bg3:      #1A2440;
  --bg4:      #1F2B4D;
  --surface:  #232E50;
  --border:   rgba(99,130,255,0.15);
  --border2:  rgba(99,130,255,0.30);
  --blue:     #6382FF;
  --blue2:    #4A6AFF;
  --blue3:    #3050DD;
  --cyan:     #22D3EE;
  --cyan2:    #06B6D4;
  --teal:     #2DD4BF;
  --green:    #34D399;
  --amber:    #FBBF24;
  --red:      #F87171;
  --purple:   #A78BFA;
  --pink:     #F472B6;
  --text:     #CBD5E1;
  --text2:    #64748B;
  --text3:    #94A3B8;
  --white:    #F1F5F9;
  --glow:     0 0 20px rgba(99,130,255,0.18);
  --glow2:    0 0 40px rgba(99,130,255,0.30);
  --shadow:   0 4px 24px rgba(0,0,0,0.4);
}

/* ── GLOBAL ── */
html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}
.main .block-container { padding: 0.5rem 1.4rem 2rem 1.4rem; max-width: 100%; }
#MainMenu, footer { visibility: hidden; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb { background: var(--blue3); border-radius: 3px; }

/* ── HEADER ── */
.nx-header {
  background: linear-gradient(135deg, #0A0E1A 0%, #0F1931 40%, #141F3D 70%, #0D1428 100%);
  border: 1px solid var(--border2);
  border-radius: 12px;
  padding: 1.2rem 2rem;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--glow2), var(--shadow);
}
.nx-header::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent 0%, var(--blue) 25%, var(--cyan) 50%, var(--teal) 75%, transparent 100%);
}
.nx-header::after {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 50%, rgba(99,130,255,0.06) 0%, transparent 65%);
  pointer-events: none;
}
.nx-logo {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.9rem; font-weight: 700;
  background: linear-gradient(135deg, #6382FF, #22D3EE, #2DD4BF);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; letter-spacing: -0.02em; line-height: 1;
}
.nx-tagline {
  font-size: 0.78rem; color: var(--text2); letter-spacing: 0.12em;
  text-transform: uppercase; margin-top: 0.25rem;
  font-family: 'JetBrains Mono', monospace;
}
.nx-badges { display: flex; gap: 0.5rem; margin-top: 0.6rem; flex-wrap: wrap; }
.nx-badge {
  background: rgba(99,130,255,0.1); border: 1px solid var(--border2);
  border-radius: 20px; padding: 0.2rem 0.7rem;
  font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
  color: var(--blue); letter-spacing: 0.08em; text-transform: uppercase;
}
.nx-badge.cyan { background: rgba(34,211,238,0.08); border-color: rgba(34,211,238,0.25); color: var(--cyan); }
.nx-badge.teal { background: rgba(45,212,191,0.08); border-color: rgba(45,212,191,0.25); color: var(--teal); }
.nx-badge.green { background: rgba(52,211,153,0.08); border-color: rgba(52,211,153,0.25); color: var(--green); }
.nx-stat { text-align: right; }
.nx-stat-val { font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--white); line-height: 1; }
.nx-stat-lbl { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: var(--text2); letter-spacing: 0.1em; text-transform: uppercase; }

/* ── CARDS ── */
.nx-card {
  background: linear-gradient(145deg, var(--bg2) 0%, var(--bg3) 100%);
  border: 1px solid var(--border);
  border-radius: 10px; padding: 1.1rem 1.2rem;
  box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,0.03);
  margin-bottom: 0.8rem; position: relative; overflow: hidden;
}
.nx-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,130,255,0.4), transparent);
}
.nx-card-title {
  font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem;
  font-weight: 600; color: var(--blue); letter-spacing: 0.08em;
  text-transform: uppercase; margin-bottom: 0.9rem;
  display: flex; align-items: center; gap: 0.5rem;
}
.nx-card-title::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--border2), transparent);
}

/* ── ROOT RESULT CARD ── */
.root-result {
  background: linear-gradient(135deg, rgba(99,130,255,0.07), rgba(34,211,238,0.04));
  border: 1px solid var(--border2);
  border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.5rem;
  transition: all 0.25s ease; cursor: default;
}
.root-result:hover { border-color: var(--blue); box-shadow: var(--glow); transform: translateY(-1px); }
.rr-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem; }
.rr-num { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: var(--text2); letter-spacing: 0.15em; }
.rr-status-ok { background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3); border-radius: 12px; padding: 0.1rem 0.55rem; font-size: 0.62rem; font-family: 'JetBrains Mono', monospace; color: var(--green); letter-spacing: 0.08em; }
.rr-status-warn { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3); border-radius: 12px; padding: 0.1rem 0.55rem; font-size: 0.62rem; font-family: 'JetBrains Mono', monospace; color: var(--amber); letter-spacing: 0.08em; }
.rr-val { font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 700; color: var(--white); }
.rr-meta { display: flex; gap: 1.2rem; margin-top: 0.35rem; flex-wrap: wrap; }
.rr-meta-item { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--text2); }
.rr-meta-item span { color: var(--cyan); }
.rr-bar { height: 2px; border-radius: 1px; margin-top: 0.55rem; }

/* ── FORMULA CHIP ── */
.formula-chip {
  background: rgba(0,0,0,0.35); border: 1px solid var(--border);
  border-left: 2px solid var(--blue); border-radius: 6px;
  padding: 0.7rem 0.9rem; font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem; color: var(--cyan); line-height: 1.85;
  margin-bottom: 0.7rem; white-space: pre;
}
.info-chip {
  background: rgba(99,130,255,0.06); border: 1px solid var(--border);
  border-left: 2px solid var(--blue); border-radius: 6px;
  padding: 0.6rem 0.9rem; font-size: 0.83rem; color: var(--text3);
  margin-bottom: 0.65rem; line-height: 1.5;
}
.warn-chip {
  background: rgba(251,191,36,0.06); border: 1px solid rgba(251,191,36,0.25);
  border-left: 2px solid var(--amber); border-radius: 6px;
  padding: 0.6rem 0.9rem; font-size: 0.83rem; color: #f0cc70;
  margin-bottom: 0.65rem;
}
.success-chip {
  background: rgba(52,211,153,0.06); border: 1px solid rgba(52,211,153,0.25);
  border-left: 2px solid var(--green); border-radius: 6px;
  padding: 0.6rem 0.9rem; font-size: 0.83rem; color: #86efac;
  margin-bottom: 0.65rem;
}
.error-chip {
  background: rgba(248,113,113,0.07); border: 1px solid rgba(248,113,113,0.25);
  border-left: 2px solid var(--red); border-radius: 6px;
  padding: 0.6rem 0.9rem; font-size: 0.83rem; color: #fca5a5;
  margin-bottom: 0.65rem;
}

/* ── SEC TITLE ── */
.sec-title {
  font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem;
  font-weight: 600; color: var(--blue); letter-spacing: 0.1em;
  text-transform: uppercase; padding: 0.5rem 0 0.45rem 0;
  border-bottom: 1px solid var(--border); margin-bottom: 0.8rem;
  display: flex; align-items: center; gap: 0.5rem;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
  background: var(--bg2) !important; border: 1px solid var(--border) !important;
  border-radius: 8px !important; padding: 0.75rem 1rem !important;
  box-shadow: var(--shadow) !important;
}
[data-testid="stMetricLabel"] p {
  font-family: 'JetBrains Mono', monospace !important; color: var(--text2) !important;
  font-size: 0.66rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Space Grotesk', sans-serif !important; color: var(--white) !important;
  font-size: 1.35rem !important; font-weight: 700 !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 8px !important; }
[data-testid="stDataFrame"] th {
  background: #0B1020 !important; color: var(--blue) !important;
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.68rem !important;
  letter-spacing: 0.08em !important; border-bottom: 1px solid var(--border2) !important;
}
[data-testid="stDataFrame"] td {
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.74rem !important;
  color: var(--text) !important; background: var(--bg1) !important;
}
[data-testid="stDataFrame"] tr:hover td { background: var(--bg3) !important; }

/* ── TABS ── */
[data-testid="stTabs"] button {
  font-family: 'Space Grotesk', sans-serif !important; font-size: 0.72rem !important;
  font-weight: 600 !important; letter-spacing: 0.06em !important;
  color: var(--text2) !important; text-transform: uppercase !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--blue) !important; border-bottom: 2px solid var(--blue) !important;
}

/* ── WIDGETS ── */
.stSelectbox>label, .stNumberInput>label, .stTextInput>label,
.stSlider>label, .stCheckbox>label, .stRadio>label {
  font-family: 'Inter', sans-serif !important; color: var(--text3) !important;
  font-size: 0.78rem !important; font-weight: 500 !important; letter-spacing: 0.04em !important;
}
.stSelectbox [data-baseweb="select"]>div {
  background: var(--bg3) !important; border: 1px solid var(--border2) !important;
  border-radius: 7px !important; color: var(--white) !important;
  font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important;
}
.stTextInput input, .stNumberInput input {
  background: var(--bg3) !important; border: 1px solid var(--border2) !important;
  border-radius: 7px !important; color: var(--cyan) !important;
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.9rem !important;
  caret-color: var(--blue) !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color: var(--blue) !important; box-shadow: 0 0 0 2px rgba(99,130,255,0.2) !important;
}
div[data-testid="stRadio"] label>div p {
  font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important; color: var(--text) !important;
}
.stCheckbox label p {
  font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important; color: var(--text) !important;
}

/* ── BUTTON ── */
.stButton>button {
  border-radius: 8px !important; width: 100% !important;
  background: linear-gradient(135deg, var(--blue3) 0%, var(--blue2) 50%, var(--blue) 100%) !important;
  color: #fff !important; font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.82rem !important; font-weight: 600 !important;
  border: none !important; letter-spacing: 0.06em !important; text-transform: uppercase !important;
  padding: 0.6rem 1.2rem !important;
  box-shadow: 0 4px 15px rgba(99,130,255,0.25), inset 0 1px 0 rgba(255,255,255,0.1) !important;
  transition: all 0.2s ease !important;
}
.stButton>button:hover {
  background: linear-gradient(135deg, var(--blue2) 0%, var(--blue) 100%) !important;
  transform: translateY(-1px) !important; box-shadow: 0 6px 22px rgba(99,130,255,0.4) !important;
}
.stButton>button:active { transform: translateY(0) !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #080C18 0%, #0C1120 50%, #080C18 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stButton>button {
  background: linear-gradient(135deg, var(--bg3), var(--bg4)) !important;
  border: 1px solid var(--border2) !important; color: var(--cyan) !important;
  font-size: 0.74rem !important; box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
  background: linear-gradient(135deg, var(--bg4), var(--surface)) !important;
  box-shadow: 0 0 12px rgba(99,130,255,0.2) !important;
}

/* ── SIDEBAR COMPONENTS ── */
.sb-logo {
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem;
  background: linear-gradient(135deg, #6382FF, #22D3EE);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  letter-spacing: 0.02em; margin-bottom: 0.2rem;
}
.sb-tagline { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--text2); letter-spacing: 0.15em; margin-bottom: 1rem; }
.sb-section { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 600; color: var(--blue); letter-spacing: 0.12em; text-transform: uppercase; border-bottom: 1px solid var(--border); padding-bottom: 0.35rem; margin: 0.8rem 0 0.6rem 0; }
.sb-method-info { background: rgba(99,130,255,0.06); border: 1px solid var(--border); border-radius: 6px; padding: 0.55rem 0.7rem; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text3); line-height: 1.75; margin-top: 0.5rem; white-space: pre; }
.hist-card { background: rgba(99,130,255,0.05); border: 1px solid var(--border); border-radius: 7px; padding: 0.6rem 0.8rem; margin-bottom: 0.45rem; transition: all 0.2s; }
.hist-card:hover { background: rgba(99,130,255,0.1); border-color: var(--border2); }
.hist-method { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--blue); letter-spacing: 0.12em; margin-bottom: 0.15rem; }
.hist-eq { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--cyan); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hist-ans { font-family: 'Inter', sans-serif; font-size: 0.72rem; color: var(--text3); margin-top: 0.1rem; }
.hist-ts { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--text2); margin-top: 0.1rem; }
.hist-empty { text-align: center; padding: 1.5rem 0.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--text2); line-height: 2.2; letter-spacing: 0.08em; }

/* ── PLACEHOLDER ── */
.nx-placeholder { text-align: center; padding: 4rem 1rem; font-family: 'Inter', sans-serif; font-size: 0.88rem; color: var(--text2); line-height: 2; }
.nx-placeholder .icon { font-size: 2.8rem; margin-bottom: 0.8rem; opacity: 0.5; }
.nx-placeholder .title { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 600; color: var(--text3); margin-bottom: 0.5rem; }

/* ── VALID / INVALID EQUATION ── */
.eq-valid { color: var(--green); font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; }
.eq-invalid { color: var(--red); font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; }

/* ── DIVIDER ── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 0.6rem 0 !important; }

/* ── EXPANDER ── */
[data-testid="stExpander"] { border: 1px solid var(--border) !important; border-radius: 8px !important; background: var(--bg1) !important; }
details>summary { font-family: 'Space Grotesk', sans-serif !important; color: var(--text3) !important; font-size: 0.8rem !important; }

/* ── ALERTS ── */
[data-testid="stAlert"], [data-testid="stInfo"], [data-testid="stSuccess"],
[data-testid="stWarning"], [data-testid="stError"] { font-family: 'Inter', sans-serif !important; border-radius: 7px !important; }

/* ── STEP CARD ── */
.step-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 7px; padding: 0.7rem 0.9rem; margin-bottom: 0.4rem;
  display: flex; gap: 0.8rem; align-items: flex-start;
}
.step-num {
  background: var(--blue3); color: #fff; border-radius: 4px;
  width: 22px; height: 22px; min-width: 22px;
  display: flex; align-items: center; justify-content: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 700;
}
.step-text { font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: var(--text3); line-height: 1.6; }

/* ── COMPARE TABLE COLORS ── */
.best-cell { color: var(--green) !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  NUMERICAL ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def parse_eq(eq_str: str):
    """Returns (expr, f_numpy, df_numpy, error_string)."""
    try:
        safe = (eq_str.strip()
                .replace('^', '**')
                .replace('ln(', 'log('))
        x = sp.Symbol('x')
        expr = sp.sympify(safe, locals={
            'x': x, 'e': sp.E, 'pi': sp.pi,
            'ln': sp.log, 'log': sp.log,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'sqrt': sp.sqrt, 'abs': sp.Abs
        })
        deriv = sp.diff(expr, x)
        mods = [{'log': np.log, 'exp': np.exp, 'sin': np.sin,
                 'cos': np.cos, 'tan': np.tan, 'sqrt': np.sqrt,
                 'Abs': np.abs, 'pi': np.pi, 'E': np.e}, 'numpy']
        f  = sp.lambdify(x, expr,  modules=mods)
        df = sp.lambdify(x, deriv, modules=mods)
        return expr, f, df, None
    except Exception as e:
        return None, None, None, str(e)


def sf(f, v):
    try:
        r = float(f(v))
        return r if np.isfinite(r) else np.nan
    except Exception:
        return np.nan


def find_brackets(f, a, b, n=3000):
    xs = np.linspace(a, b, int(n))
    bks, prev = [], sf(f, xs[0])
    for i in range(1, len(xs)):
        curr = sf(f, xs[i])
        if not np.isnan(prev) and not np.isnan(curr) and prev * curr < 0:
            if not bks or abs(xs[i-1] - bks[-1][1]) > 1e-9:
                bks.append((float(xs[i-1]), float(xs[i])))
        prev = curr
    return bks


# ── METHODS ──────────────────────────────────────────────────────────────────

def method_incremental(f, xl_0, xu_0, tol, max_iter):
    """
    Reference columns: Iteration | x_l | Δx | x_u | f(x_l) | f(x_u) | f(x_l)*f(x_u) | Remark
    """
    rows = []
    dx, xl = (xu_0 - xl_0) / 20.0, xl_0
    root = ea = None
    for i in range(int(max_iter)):
        xu = xl + dx
        fxl, fxu = sf(f, xl), sf(f, xu)
        if np.isnan(fxl) or np.isnan(fxu):
            xl = xu; continue
        prod = fxl * fxu
        remark = "Go to next interval" if prod > 0 else "Sign change → shrink Δx"
        rows.append({"Iter": i+1, "x_l": round(xl,7), "Δx": round(dx,7), "x_u": round(xu,7),
                     "f(x_l)": round(fxl,6), "f(x_u)": round(fxu,6),
                     "f(xl)·f(xu)": "> 0" if prod > 0 else "< 0", "Remark": remark})
        if abs(fxu) < tol or dx < tol / 100:
            root = xu; ea = abs(fxu); break
        xl = xu if prod > 0 else xl
        if prod <= 0: dx /= 10.0
    if root is None: root = xl; ea = abs(sf(f, xl)) or 0.0
    return root, ea, rows


def method_bisection(f, xl, xu, tol, max_iter):
    """
    Reference columns: Iteration | x_l | x_r | x_u | f(x_l) | f(x_r) | |Ea|% | f(xl)·f(xr) | Remark
    """
    rows, root, xr_old, ea = [], None, None, None
    for i in range(int(max_iter)):
        xr = (xl + xu) / 2
        fxl, fxr = sf(f, xl), sf(f, xr)
        prod = fxl * fxr
        ea = abs((xr - xr_old) / xr) * 100 if (xr_old is not None and xr != 0) else None
        remark = "1st subinterval" if prod < 0 else ("2nd subinterval" if prod > 0 else "Exact root")
        rows.append({"Iter": i+1, "x_l": round(xl,8), "x_r": round(xr,8), "x_u": round(xu,8),
                     "f(x_l)": round(fxl,6), "f(x_r)": round(fxr,6),
                     "|Ea|%": round(ea,6) if ea is not None else "—",
                     "f(xl)·f(xr)": "< 0" if prod < 0 else ("> 0" if prod > 0 else "= 0"),
                     "Remark": remark})
        if (ea is not None and ea < tol) or fxr == 0:
            root = xr; break
        if prod < 0: xu = xr
        else: xl = xr
        xr_old = xr
    if root is None: root = xr_old or (xl + xu) / 2
    return root, ea or 0.0, rows


def method_regula_falsi(f, xl, xu, tol, max_iter):
    """
    Reference columns: No. of Iteration | x_L | x_U | x_R | Ea | f(x_L) | f(x_U) | f(x_R) | f(xL)·f(xR)
    """
    rows, root, xr_old, ea = [], None, None, None
    for i in range(int(max_iter)):
        fxl, fxu = sf(f, xl), sf(f, xu)
        if fxl == fxu: break
        xr = (xu * fxl - xl * fxu) / (fxl - fxu)
        fxr = sf(f, xr)
        prod = fxl * fxr
        ea = abs((xr - xr_old) / xr) if (xr_old is not None and xr != 0) else None
        rows.append({"Iter": i+1, "x_L": round(xl,8), "x_U": round(xu,8), "x_R": round(xr,8),
                     "Ea": round(ea,8) if ea is not None else "—",
                     "f(x_L)": round(fxl,6), "f(x_U)": round(fxu,6), "f(x_R)": round(fxr,6),
                     "f(xL)·f(xR)": "< 0" if prod < 0 else ("> 0" if prod > 0 else "= 0")})
        if (ea is not None and ea < tol) or fxr == 0:
            root = xr; break
        if prod < 0: xu = xr
        else: xl = xr
        xr_old = xr
    if root is None: root = xr_old or (xl + xu) / 2
    return root, ea or 0.0, rows


def method_newton_raphson(f, df, x0, tol, max_iter):
    """
    Reference columns: No. of Iteration | x_i | Ea | f(x) | f'(x)
    Row 0 = initial (no Ea)
    """
    rows, xi = [], x0
    rows.append({"Iter": 0, "x_i": round(xi,8), "Ea": "—",
                 "f(x)": round(sf(f, xi),7), "f'(x)": round(sf(df, xi),7)})
    root = ea = None
    for i in range(int(max_iter)):
        fxi, dfxi = sf(f, xi), sf(df, xi)
        if np.isnan(fxi) or np.isnan(dfxi) or abs(dfxi) < 1e-14:
            rows.append({"Iter": i+1, "x_i": round(xi,8), "Ea": "FAIL",
                         "f(x)": str(round(fxi,7) if not np.isnan(fxi) else "NaN"), "f'(x)": "~0/NaN"})
            break
        xi_new = xi - fxi / dfxi
        ea = abs((xi_new - xi) / xi_new) if xi_new != 0 else abs(xi_new - xi)
        xi = xi_new
        rows.append({"Iter": i+1, "x_i": round(xi,8), "Ea": round(ea,8),
                     "f(x)": round(sf(f, xi),7), "f'(x)": round(sf(df, xi),7)})
        if ea < tol:
            root = xi; break
    if root is None: root = xi
    return root, ea or 0.0, rows


def method_secant(f, x0, x1, tol, max_iter):
    """
    Reference columns: Iter | x_{i-1} | x_i | x_{i+1} | Ea | f(x_{i-1}) | f(x_i) | f(x_{i+1})
    """
    rows, xp, xc = [], x0, x1
    root = ea = None
    for i in range(int(max_iter)):
        fxp, fxc = sf(f, xp), sf(f, xc)
        if abs(fxc - fxp) < 1e-14: break
        xn = xc - fxc * (xc - xp) / (fxc - fxp)
        fxn = sf(f, xn)
        ea = abs((xn - xc) / xn) if xn != 0 else abs(xn - xc)
        rows.append({"Iter": i+1, "x_{i-1}": round(xp,8), "x_i": round(xc,8),
                     "x_{i+1}": round(xn,8), "Ea": round(ea,8),
                     "f(x_{i-1})": round(fxp,6), "f(x_i)": round(fxc,6), "f(x_{i+1})": round(fxn,6)})
        xp, xc = xc, xn
        if ea < tol:
            root = xn; break
    if root is None: root = xc
    return root, ea or 0.0, rows


def dispatch(method, f, df, xl, xu, tol, max_iter):
    xm, xm2 = (xl + xu) / 2, xl + (xu - xl) * 0.3
    if   method == "Incremental Search":    return method_incremental(f, xl, xu, tol, max_iter)
    elif method == "Bisection Method":      return method_bisection(f, xl, xu, tol, max_iter)
    elif method == "Regula Falsi":          return method_regula_falsi(f, xl, xu, tol, max_iter)
    elif method == "Newton-Raphson Method": return method_newton_raphson(f, df, xm, tol, max_iter)
    elif method == "Secant Method":         return method_secant(f, xm2, xm, tol, max_iter)
    return None, 0, []


# ══════════════════════════════════════════════════════════════════════════════
#  PLOT HELPERS
# ══════════════════════════════════════════════════════════════════════════════
ROOT_COLORS = ['#6382FF','#22D3EE','#34D399','#FBBF24','#F87171','#A78BFA','#F472B6','#2DD4BF']

def build_graph(f, a, b, roots_data, eq_str):
    mg = (b - a) * 0.1
    xs = np.linspace(a - mg, b + mg, 1400)
    ys = np.array([sf(f, xi) for xi in xs])
    if np.any(np.isfinite(ys)):
        q99 = np.nanpercentile(np.abs(ys[np.isfinite(ys)]), 99)
        ys = np.where(np.abs(ys) > min(q99 * 5, 1e7), np.nan, ys)

    fig = go.Figure()
    # Shaded zero band
    fig.add_hrect(y0=-0.001, y1=0.001, line_width=0, fillcolor='rgba(99,130,255,0.04)')
    # Curve
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)',
                             line=dict(color='#6382FF', width=2.2),
                             hovertemplate='x = %{x:.5f}<br>f(x) = %{y:.6f}<extra></extra>'))
    # Axes
    fig.add_hline(y=0, line_dash="solid", line_color='rgba(99,130,255,0.35)', line_width=1)
    fig.add_vline(x=0, line_dash="dot",   line_color='rgba(99,130,255,0.2)',  line_width=0.8)

    for idx, r in enumerate(roots_data):
        col = ROOT_COLORS[idx % len(ROOT_COLORS)]
        fy  = sf(f, r['root'])
        # Vertical drop line
        if np.isfinite(fy) and abs(fy) < 1e5:
            fig.add_shape(type='line', x0=r['root'], x1=r['root'], y0=0, y1=fy,
                          line=dict(color=col, width=1.2, dash='dot'), opacity=0.5)
        # Root marker
        fig.add_trace(go.Scatter(
            x=[r['root']], y=[0], mode='markers+text',
            name=f"Root {idx+1}: x={r['root']:.5f}",
            marker=dict(color=col, size=13, symbol='circle',
                        line=dict(color='#fff', width=1.5)),
            text=[f"  x={r['root']:.4f}"], textposition='top right',
            textfont=dict(family='JetBrains Mono', size=10, color=col),
            hovertemplate=f"Root {idx+1}<br>x = {r['root']:.8f}<br>f(x) ≈ {fy:.3e}<extra></extra>"
        ))

    fig.update_layout(
        plot_bgcolor='#080C18', paper_bgcolor='#0A0E1A',
        font=dict(family='Inter, sans-serif', color='#64748B'),
        xaxis=dict(title='x', gridcolor='rgba(99,130,255,0.06)',
                   linecolor='rgba(99,130,255,0.2)', zerolinecolor='rgba(99,130,255,0.15)',
                   tickfont=dict(family='JetBrains Mono', size=10),
                   title_font=dict(color='#6382FF', size=11), showgrid=True),
        yaxis=dict(title='f(x)', gridcolor='rgba(99,130,255,0.06)',
                   linecolor='rgba(99,130,255,0.2)', zerolinecolor='rgba(99,130,255,0.15)',
                   tickfont=dict(family='JetBrains Mono', size=10),
                   title_font=dict(color='#6382FF', size=11), showgrid=True),
        legend=dict(bgcolor='rgba(10,14,26,0.85)', bordercolor='rgba(99,130,255,0.2)',
                    borderwidth=1, font=dict(family='JetBrains Mono', size=10, color='#94A3B8')),
        hovermode='x unified', margin=dict(l=10, r=10, t=35, b=10), height=380,
        title=dict(text=f"f(x) = {eq_str}", font=dict(family='JetBrains Mono', size=12, color='#64748B'),
                   x=0.01, xanchor='left')
    )
    return fig


def build_convergence(all_results):
    fig = go.Figure()
    for idx, r in enumerate(all_results[:8]):
        col = ROOT_COLORS[idx % len(ROOT_COLORS)]
        iters, eas = [], []
        for row in r['rows']:
            ev = row.get('Ea', row.get('|Ea|%', '—'))
            try:
                v = float(ev)
                iters.append(row.get('Iter', len(iters) + 1))
                eas.append(max(v, 1e-16))
            except Exception: pass
        if len(iters) > 1:
            fig.add_trace(go.Scatter(x=iters, y=eas, mode='lines+markers',
                                     name=f"Root {idx+1} ≈ {r['root']:.4f}",
                                     line=dict(color=col, width=2), marker=dict(size=5, color=col),
                                     hovertemplate='Iter %{x}<br>Ea = %{y:.4e}<extra></extra>'))
    fig.update_layout(
        plot_bgcolor='#080C18', paper_bgcolor='#0A0E1A',
        font=dict(family='Inter', color='#64748B'),
        xaxis=dict(title='Iteration', gridcolor='rgba(99,130,255,0.06)',
                   tickfont=dict(family='JetBrains Mono', size=10),
                   title_font=dict(color='#6382FF', size=11)),
        yaxis=dict(title='Approx. Error (Ea)', type='log', gridcolor='rgba(99,130,255,0.06)',
                   tickfont=dict(family='JetBrains Mono', size=10),
                   title_font=dict(color='#6382FF', size=11)),
        legend=dict(bgcolor='rgba(10,14,26,0.85)', bordercolor='rgba(99,130,255,0.2)',
                    borderwidth=1, font=dict(family='JetBrains Mono', size=10, color='#94A3B8')),
        hovermode='x unified', margin=dict(l=10, r=10, t=20, b=10), height=280,
    )
    return fig


def build_compare_bar(cmp_df):
    methods = cmp_df["Method"].unique().tolist()
    brackets = cmp_df["Bracket"].unique().tolist()
    fig = go.Figure()
    for mi, m in enumerate(methods):
        sub = cmp_df[cmp_df["Method"] == m]
        fig.add_trace(go.Bar(
            name=m[:12], x=sub["Bracket"], y=sub["Iterations"].astype(float),
            marker_color=ROOT_COLORS[mi % len(ROOT_COLORS)], opacity=0.8,
            hovertemplate=f"{m}<br>Bracket: %{{x}}<br>Iters: %{{y}}<extra></extra>"
        ))
    fig.update_layout(
        barmode='group', plot_bgcolor='#080C18', paper_bgcolor='#0A0E1A',
        font=dict(family='Inter', color='#64748B'),
        xaxis=dict(title='Bracket', gridcolor='rgba(99,130,255,0.06)',
                   tickfont=dict(family='JetBrains Mono', size=9), tickangle=-25),
        yaxis=dict(title='Iterations to Converge', gridcolor='rgba(99,130,255,0.06)',
                   tickfont=dict(family='JetBrains Mono', size=10)),
        legend=dict(bgcolor='rgba(10,14,26,0.85)', bordercolor='rgba(99,130,255,0.2)',
                    borderwidth=1, font=dict(family='JetBrains Mono', size=10, color='#94A3B8')),
        margin=dict(l=10, r=10, t=15, b=10), height=260,
    )
    return fig


def results_to_csv(all_results):
    rows = []
    for r in all_results:
        rows.append({
            "Method": r['method'], "Root": r['root'], "f(root)": r['f_val'],
            "Final_Ea": r['error'], "Iterations": r['iterations'],
            "Bracket_L": r['bracket'][0], "Bracket_U": r['bracket'][1],
            "Converged": "YES" if r.get('converged', True) else "NO",
            "Timestamp": r.get('timestamp', '')
        })
    return pd.DataFrame(rows).to_csv(index=False).encode('utf-8')


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
METHOD_FORMULAS = {
    "Incremental Search":
        "x_u = x_l + Δx\nif f(xl)·f(xu) > 0:\n  advance (xl = xu)\nelse:\n  shrink Δx /= 10\nstop: |f(xu)| < εs",
    "Bisection Method":
        "x_r = (x_l + x_u) / 2\n|Ea| = |Δxr/xr| × 100%\nf(xl)·f(xr)<0 → xu = xr\nf(xl)·f(xr)>0 → xl = xr\nstop: |Ea| < εs",
    "Regula Falsi":
        "xR = [xU·f(xL) - xL·f(xU)]\n      / [f(xL) - f(xU)]\nEa = |(xR_new-xR_old)/xR|\nstop: Ea < εs",
    "Newton-Raphson Method":
        "x_{i+1} = x_i - f(x_i)/f'(x_i)\nEa = |(x_new-x_old)/x_new|\nstop: Ea < εs\n\nNeeds: f'(x) ≠ 0",
    "Secant Method":
        "x_{i+1} = x_i - f(x_i)·(x_i-x_{i-1})\n         / (f(x_i) - f(x_{i-1}))\nEa = |(x_new-x_old)/x_new|\nstop: Ea < εs",
}

with st.sidebar:
    st.markdown('<div class="sb-logo">∿ NumerixPro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tagline">ROOT FINDING ENGINE v3</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">⊙ Method</div>', unsafe_allow_html=True)
    method = st.selectbox("Algorithm", list(METHOD_FORMULAS.keys()), label_visibility="collapsed")
    st.markdown(f'<div class="sb-method-info">{METHOD_FORMULAS[method]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">⊞ Search Range</div>', unsafe_allow_html=True)
    rc1, rc2 = st.columns(2)
    a_range = rc1.number_input("a", value=-5.0, format="%.2f")
    b_range = rc2.number_input("b", value=5.0,  format="%.2f")

    st.markdown('<div class="sb-section">⚙ Parameters</div>', unsafe_allow_html=True)
    tol      = st.number_input("Tolerance (εs)", value=0.001, format="%.5f", min_value=1e-14)
    max_iter = st.number_input("Max Iterations",  value=100, step=10, min_value=5)
    n_scan   = st.number_input("Scan Points",     value=3000, step=500, min_value=200,
                               help="Higher → finds roots in denser regions")

    st.markdown('<div class="sb-section">◈ Options</div>', unsafe_allow_html=True)
    auto_range = st.checkbox("Auto-expand range for ln/exp", value=True)
    show_steps = st.checkbox("Show step-by-step explanation", value=True)

    st.markdown("---")
    st.markdown('<div class="sb-section">🕐 History</div>', unsafe_allow_html=True)
    if st.session_state.history:
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
        for h in reversed(st.session_state.history[-10:]):
            st.markdown(f"""<div class="hist-card">
                <div class="hist-method">{h['method']}</div>
                <div class="hist-eq">f(x) = {h['eq']}</div>
                <div class="hist-ans">{h['answer']}</div>
                <div class="hist-ts">{h['ts']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="hist-empty">NO HISTORY<br>─────────<br>Solve to populate</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nx-header">
  <div style="display:flex;align-items:center;justify-content:space-between;">
    <div>
      <div class="nx-logo">∿ NumerixPro</div>
      <div class="nx-tagline">Numerical Methods Root-Finding Calculator</div>
      <div class="nx-badges">
        <span class="nx-badge">Multi-Root Detection</span>
        <span class="nx-badge cyan">5 Methods</span>
        <span class="nx-badge teal">SymPy · NumPy · Plotly</span>
        <span class="nx-badge green">CSV Export</span>
      </div>
    </div>
    <div style="display:flex;gap:1.5rem;">
      <div class="nx-stat"><div class="nx-stat-val">5</div><div class="nx-stat-lbl">Methods</div></div>
      <div class="nx-stat"><div class="nx-stat-val">∞</div><div class="nx-stat-lbl">Equations</div></div>
      <div class="nx-stat"><div class="nx-stat-val">∿</div><div class="nx-stat-lbl">Roots</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  EQUATION INPUT AREA  (top bar)
# ══════════════════════════════════════════════════════════════════════════════
PRESETS = [
    ("x³−6x²+11x−6",  "x**3 - 6*x**2 + 11*x - 6"),
    ("3x+sin(x)−eˣ",   "3*x + sin(x) - exp(x)"),
    ("e⁻ˣ − x",        "exp(-x) - x"),
    ("ln(x) + x²−4",   "log(x) + x**2 - 4"),
    ("x⁵−x⁴−7x+3",    "x**5 - x**4 - 7*x + 3"),
    ("ln(x) − 2",      "log(x) - 2"),
    ("eˣ − 3x",        "exp(x) - 3*x"),
    ("x⁴−5x²+4",       "x**4 - 5*x**2 + 4"),
    ("ln(x) − 1",      "log(x) - 1"),
    ("x²− 4",          "x**2 - 4"),
]

st.markdown('<div class="nx-card">', unsafe_allow_html=True)
st.markdown('<div class="nx-card-title">∿ Equation Input</div>', unsafe_allow_html=True)

# Preset buttons
st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;color:#334155;letter-spacing:0.1em;margin-bottom:0.4rem;">PRESET EQUATIONS</div>', unsafe_allow_html=True)
preset_cols = st.columns(5)
preset_clicked = None
for pi, (lbl, val) in enumerate(PRESETS):
    with preset_cols[pi % 5]:
        if st.button(lbl, key=f"preset_{pi}"):
            preset_clicked = val
            st.session_state["eq_cache"] = val

# Equation input
eq_default = preset_clicked or st.session_state.get("eq_cache", "x**3 - 6*x**2 + 11*x - 6")
if preset_clicked:
    st.session_state["eq_cache"] = preset_clicked

ci1, ci2 = st.columns([3, 1])
with ci1:
    eq_str = st.text_input("f(x) =", value=eq_default, key="eq_main",
                           help="Python/SymPy: x**2, log(x)=ln(x), exp(x), sin(x), sqrt(x), pi")
with ci2:
    st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
    # Real-time validation
    if eq_str:
        _, _, _, perr = parse_eq(eq_str)
        if perr:
            st.markdown(f'<div class="eq-invalid">✗ {perr[:50]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="eq-valid">✓ Valid equation</div>', unsafe_allow_html=True)

st.markdown('<div class="info-chip" style="margin-top:0.3rem;margin-bottom:0;">'
            'Syntax: <b>log(x)</b>=ln(x) &nbsp;·&nbsp; <b>exp(x)</b>=eˣ &nbsp;·&nbsp; '
            '<b>x**n</b>=xⁿ &nbsp;·&nbsp; <b>sin/cos/tan(x)</b> &nbsp;·&nbsp; <b>sqrt(x)</b>'
            '</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # /nx-card


# ══════════════════════════════════════════════════════════════════════════════
#  SOLVE BUTTON ROW
# ══════════════════════════════════════════════════════════════════════════════
sb1, sb2, sb3 = st.columns([2, 2, 1.2])
with sb1:
    solve_btn = st.button(f"∿  Solve with {method}", use_container_width=True)
with sb2:
    compare_btn = st.button("⊞  Compare All 5 Methods", use_container_width=True)
with sb3:
    if st.session_state.results:
        csv_data = results_to_csv(st.session_state.results)
        st.download_button("⬇ Export CSV", data=csv_data,
                           file_name=f"roots_{datetime.now().strftime('%H%M%S')}.csv",
                           mime="text/csv", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SOLVE LOGIC
# ══════════════════════════════════════════════════════════════════════════════
def run_solve(methods_list, eq, a, b, tol, max_iter, n_scan):
    expr_sym, f_lam, df_lam, perr = parse_eq(eq)
    if perr:
        return None, f"Parse Error: {perr}", None, None
    if b <= a:
        return None, "Range b must be > a.", None, None

    # Auto-expand for log domain (x must be > 0)
    eff_a = max(a, 0.001) if auto_range and 'log(' in eq.lower() else a
    if eff_a >= b:
        eff_a = 0.001

    brackets = find_brackets(f_lam, eff_a, b, n=int(n_scan))
    if not brackets:
        return None, f"No sign changes in [{eff_a:.3f}, {b:.3f}]. Try expanding range or scan points.", None, None

    all_results, seen = [], []
    for m in methods_list:
        for bk in brackets:
            xl_b, xu_b = bk
            root, ea, rows = dispatch(m, f_lam, df_lam, xl_b, xu_b, float(tol), int(max_iter))
            if root is None: continue
            dup = any(abs(root - s['root']) < max(tol*500, 1e-5) and s['method'] == m for s in seen)
            if not dup:
                entry = {
                    "root": root, "error": ea, "iterations": len(rows),
                    "method": m, "bracket": bk, "rows": rows,
                    "f_val": sf(f_lam, root), "converged": (ea < tol),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_results.append(entry)
                seen.append({"root": root, "method": m})

    if not all_results:
        return None, "Brackets found but no method converged. Try adjusting tolerance or max iterations.", None, None

    seen_vals, unique = [], []
    for r in all_results:
        if not any(abs(r['root'] - v) < 1e-5 for v in seen_vals):
            unique.append(r); seen_vals.append(r['root'])

    fig = build_graph(f_lam, eff_a, b, unique, eq)
    return all_results, None, fig, unique


if solve_btn or compare_btn:
    methods_to_run = ([method] if solve_btn else
                      ["Bisection Method", "Regula Falsi",
                       "Newton-Raphson Method", "Secant Method", "Incremental Search"])
    with st.spinner("Computing roots..."):
        results, err_msg, fig, unique_roots = run_solve(
            methods_to_run, eq_str, a_range, b_range, tol, max_iter, n_scan)

    if err_msg:
        st.markdown(f'<div class="error-chip">⚠ {err_msg}</div>', unsafe_allow_html=True)
    else:
        st.session_state.results = results
        st.session_state.last_fig = fig
        st.session_state.last_eq = eq_str

        roots_str = " · ".join([f"x≈{r['root']:.5f}" for r in unique_roots])
        st.session_state.history.append({
            "method":  method if solve_btn else "ALL",
            "eq":      eq_str[:40],
            "answer":  f"{len(unique_roots)} root(s): {roots_str[:60]}",
            "ts":      datetime.now().strftime("%b %d %H:%M"),
        })
        st.toast(f"✓ Found {len(unique_roots)} root(s)!", icon="✅")


# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS DISPLAY
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.results:
    all_results = st.session_state.results

    # Unique roots
    seen_vals, unique_roots = [], []
    for r in all_results:
        if not any(abs(r['root'] - v) < 1e-5 for v in seen_vals):
            unique_roots.append(r); seen_vals.append(r['root'])

    # ── METRICS ROW ──
    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    mc = st.columns(5)
    mc[0].metric("Roots Found",   len(unique_roots))
    mc[1].metric("Method",        all_results[0]['method'].split()[0])
    mc[2].metric("Brackets",      len(set(str(r['bracket']) for r in all_results)))
    best_ea = min((r['error'] for r in all_results if r['error']), default=0)
    mc[3].metric("Best Ea",       f"{best_ea:.2e}" if best_ea else "—")
    mc[4].metric("Total Iters",   sum(r['iterations'] for r in all_results))

    # ── MAIN TABS ──
    tabs = st.tabs(["∿ Graph", "⊛ Results", "▦ Iteration Tables",
                    "◈ Convergence", "⊞ Compare Methods", "⊟ Step-by-Step"])

    # ── TAB 1: GRAPH ──
    with tabs[0]:
        st.markdown('<div class="nx-card">', unsafe_allow_html=True)
        st.markdown('<div class="nx-card-title">∿ Function Graph</div>', unsafe_allow_html=True)
        st.plotly_chart(st.session_state.last_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Function analysis
        expr2, f2, _, _ = parse_eq(st.session_state.last_eq)
        if expr2:
            ga, gb = st.columns(2)
            with ga:
                st.markdown('<div class="nx-card">', unsafe_allow_html=True)
                st.markdown('<div class="nx-card-title">⊙ Symbolic Analysis</div>', unsafe_allow_html=True)
                x = sp.Symbol('x')
                try:
                    d1 = sp.diff(expr2, x)
                    d2 = sp.diff(d1, x)
                    st.markdown(f'<div class="formula-chip">f(x)   = {str(expr2)[:60]}\nf\'(x)  = {str(d1)[:60]}\nf\'\'(x) = {str(d2)[:60]}</div>', unsafe_allow_html=True)
                except: pass
                st.markdown('</div>', unsafe_allow_html=True)
            with gb:
                st.markdown('<div class="nx-card">', unsafe_allow_html=True)
                st.markdown('<div class="nx-card-title">⊛ Roots Summary</div>', unsafe_allow_html=True)
                for i, r in enumerate(unique_roots):
                    col = ROOT_COLORS[i % len(ROOT_COLORS)]
                    bar_w = max(4, min(96, int(100 - min(r['error'] * 1000, 92)))) if r['error'] else 90
                    conv = "CONVERGED" if r['error'] < tol else "CHECK"
                    status_class = "rr-status-ok" if r['error'] < tol else "rr-status-warn"
                    st.markdown(f"""<div class="root-result">
                        <div class="rr-header">
                            <div class="rr-num">ROOT {i+1} / {len(unique_roots)}</div>
                            <div class="{status_class}">{conv}</div>
                        </div>
                        <div class="rr-val" style="color:{col};">x = {r['root']:.10f}</div>
                        <div class="rr-meta">
                            <div class="rr-meta-item">f(x) ≈ <span>{r['f_val']:.3e}</span></div>
                            <div class="rr-meta-item">Ea = <span>{r['error']:.4e}</span></div>
                            <div class="rr-meta-item">Iters = <span>{r['iterations']}</span></div>
                            <div class="rr-meta-item">Method = <span>{r['method']}</span></div>
                        </div>
                        <div class="rr-bar" style="background:linear-gradient(90deg,{col},{col}44);width:{bar_w}%;"></div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: RESULTS TABLE ──
    with tabs[1]:
        st.markdown('<div class="sec-title">⊛ All Roots Found</div>', unsafe_allow_html=True)
        summary_rows = []
        for i, r in enumerate(unique_roots):
            summary_rows.append({
                "Root #":      f"Root {i+1}",
                "x value":     round(r['root'], 10),
                "f(x)":        f"{r['f_val']:.6e}",
                "Error (Ea)":  f"{r['error']:.6e}",
                "Iterations":  r['iterations'],
                "Method":      r['method'],
                "Bracket":     f"[{r['bracket'][0]:.5f}, {r['bracket'][1]:.5f}]",
                "Converged":   "✓ YES" if r['error'] < tol else "✗ NO",
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True,
                     height=min(280, 65 + 42 * len(summary_rows)))

        # Root detail cards
        st.markdown('<div class="sec-title" style="margin-top:1rem;">◈ Root Cards</div>', unsafe_allow_html=True)
        n_card_cols = min(3, len(unique_roots))
        card_cols = st.columns(n_card_cols)
        for i, r in enumerate(unique_roots):
            col = ROOT_COLORS[i % len(ROOT_COLORS)]
            bar_w = max(4, min(96, int(100 - min(r['error'] * 1000, 92)))) if r['error'] else 90
            conv = "CONVERGED" if r['error'] < tol else "CHECK"
            sc = "rr-status-ok" if r['error'] < tol else "rr-status-warn"
            with card_cols[i % n_card_cols]:
                st.markdown(f"""<div class="root-result">
                    <div class="rr-header">
                        <div class="rr-num">ROOT {i+1}</div>
                        <div class="{sc}">{conv}</div>
                    </div>
                    <div class="rr-val" style="color:{col};">x = {r['root']:.8f}</div>
                    <div class="rr-meta">
                        <div class="rr-meta-item">f(x) ≈ <span>{r['f_val']:.3e}</span></div>
                        <div class="rr-meta-item">Ea = <span>{r['error']:.4e}</span></div>
                        <div class="rr-meta-item">Iters = <span>{r['iterations']}</span></div>
                    </div>
                    <div class="rr-meta" style="margin-top:0.3rem;">
                        <span class="nx-badge">{r['method'][:15]}</span>
                    </div>
                    <div class="rr-bar" style="background:linear-gradient(90deg,{col},{col}44);width:{bar_w}%;"></div>
                </div>""", unsafe_allow_html=True)

        # Download button
        st.markdown("<div style='margin-top:0.8rem;'>", unsafe_allow_html=True)
        csv_data = results_to_csv(all_results)
        st.download_button("⬇  Download Full Results as CSV", data=csv_data,
                           file_name=f"NumerixPro_roots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                           mime="text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 3: ITERATION TABLES ──
    with tabs[2]:
        st.markdown('<div class="sec-title">▦ Iteration Tables (Reference Format)</div>', unsafe_allow_html=True)
        groups = {}
        for r in all_results:
            key = f"{r['method']} · [{r['bracket'][0]:.4f}, {r['bracket'][1]:.4f}]"
            if key not in groups: groups[key] = r

        if groups:
            g_tab_labels = [f"Root {i+1}" for i in range(len(groups))]
            g_tabs = st.tabs(g_tab_labels)
            for (key, r), gtab in zip(groups.items(), g_tabs):
                with gtab:
                    st.markdown(f'<div class="info-chip"><b>Method:</b> {r["method"]} &nbsp;|&nbsp; '
                                f'<b>Root:</b> x ≈ {r["root"]:.8f} &nbsp;|&nbsp; '
                                f'<b>Bracket:</b> [{r["bracket"][0]:.5f}, {r["bracket"][1]:.5f}] &nbsp;|&nbsp; '
                                f'<b>Final Ea:</b> {r["error"]:.4e} &nbsp;|&nbsp; '
                                f'<b>Iters:</b> {r["iterations"]}</div>', unsafe_allow_html=True)

                    df_iters = pd.DataFrame(r['rows'])
                    st.dataframe(df_iters, use_container_width=True, height=320)

                    # Export iteration table
                    iter_csv = df_iters.to_csv(index=False).encode('utf-8')
                    st.download_button(f"⬇ Export Iteration Table (Root {list(groups.keys()).index(key)+1})",
                                       data=iter_csv,
                                       file_name=f"iterations_root{list(groups.keys()).index(key)+1}.csv",
                                       mime="text/csv", key=f"dl_iter_{key[:20]}")

    # ── TAB 4: CONVERGENCE ──
    with tabs[3]:
        st.markdown('<div class="sec-title">◈ Error Convergence Analysis</div>', unsafe_allow_html=True)
        st.plotly_chart(build_convergence(all_results), use_container_width=True)

        # Error summary table
        err_rows = []
        for r in all_results:
            err_rows.append({
                "Method":      r['method'],
                "Root x":      round(r['root'], 8),
                "Final Ea":    f"{r['error']:.6e}",
                "Iterations":  r['iterations'],
                "f(root)":     f"{r['f_val']:.6e}",
                "Within Tol":  "✓" if r['error'] < tol else "✗",
            })
        st.dataframe(pd.DataFrame(err_rows), use_container_width=True)

    # ── TAB 5: COMPARE METHODS ──
    with tabs[4]:
        st.markdown('<div class="sec-title">⊞ All-Methods Comparison</div>', unsafe_allow_html=True)
        expr3, f3, df3, _ = parse_eq(st.session_state.last_eq)
        if f3:
            eff_a2 = max(a_range, 0.001) if auto_range and 'log(' in st.session_state.last_eq.lower() else a_range
            bk3 = find_brackets(f3, eff_a2, b_range, n=int(n_scan))
            ALL_M = ["Bisection Method", "Regula Falsi",
                     "Newton-Raphson Method", "Secant Method", "Incremental Search"]
            cmp_rows = []
            for m3 in ALL_M:
                for bk in bk3[:6]:
                    xl3, xu3 = bk
                    r3, ea3, rows3 = dispatch(m3, f3, df3, xl3, xu3, float(tol), int(max_iter))
                    if r3 is not None:
                        cmp_rows.append({
                            "Method":     m3, "Root": round(r3, 8),
                            "Iterations": len(rows3),
                            "Final Ea":   f"{ea3:.4e}" if ea3 else "—",
                            "f(root)":    f"{sf(f3, r3):.4e}",
                            "Bracket":    f"[{xl3:.3f},{xu3:.3f}]",
                            "Converged":  "✓" if ea3 < tol else "✗",
                        })

            if cmp_rows:
                df_cmp = pd.DataFrame(cmp_rows)
                st.dataframe(df_cmp, use_container_width=True)

                # Bar chart
                st.markdown('<div class="sec-title" style="margin-top:1rem;">⊙ Iterations per Method per Bracket</div>', unsafe_allow_html=True)
                df_cmp["Iterations"] = pd.to_numeric(df_cmp["Iterations"], errors='coerce')
                st.plotly_chart(build_compare_bar(df_cmp), use_container_width=True)

                # Winner cards
                st.markdown('<div class="sec-title">⊙ Fastest Method per Bracket</div>', unsafe_allow_html=True)
                for bk_s in df_cmp["Bracket"].unique():
                    sub = df_cmp[df_cmp["Bracket"] == bk_s].sort_values("Iterations").reset_index(drop=True)
                    st.markdown(f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.62rem;color:#334155;margin:0.4rem 0 0.25rem 0;letter-spacing:0.12em;">BRACKET {bk_s}</div>', unsafe_allow_html=True)
                    wc = st.columns(len(sub))
                    for ci, (_, row) in enumerate(sub.iterrows()):
                        col_w = ROOT_COLORS[ci % len(ROOT_COLORS)]
                        with wc[ci]:
                            badge = "🥇" if ci == 0 else ("🥈" if ci == 1 else f"#{ci+1}")
                            st.markdown(f"""<div class="root-result" style="border-color:{col_w}44;padding:0.6rem 0.8rem;">
                                <div class="rr-num" style="color:{col_w};">{badge} RANK {ci+1}</div>
                                <div style="font-family:'Space Grotesk',sans-serif;font-size:0.78rem;font-weight:600;color:{col_w};margin:0.2rem 0;">{row['Method']}</div>
                                <div class="rr-meta"><span class="rr-meta-item">Iters: <span>{row['Iterations']}</span></span>
                                <span class="rr-meta-item">Ea: <span>{row['Final Ea']}</span></span></div>
                            </div>""", unsafe_allow_html=True)

    # ── TAB 6: STEP-BY-STEP ──
    with tabs[5]:
        st.markdown('<div class="sec-title">⊟ Step-by-Step Explanation</div>', unsafe_allow_html=True)
        if all_results:
            r0 = all_results[0]
            steps_by_method = {
                "Incremental Search": [
                    f"Set initial x_l = {r0['bracket'][0]:.4f} with step Δx",
                    "Compute x_u = x_l + Δx and evaluate f(x_l), f(x_u)",
                    "Check sign: if f(x_l)·f(x_u) > 0 → advance (x_l = x_u)",
                    "If f(x_l)·f(x_u) < 0 → root passed, shrink Δx by ÷10",
                    "Repeat until |f(x_u)| < εs — root located",
                    f"Converged to x ≈ {r0['root']:.8f} in {r0['iterations']} iterations",
                ],
                "Bisection Method": [
                    f"Initial bracket: x_l = {r0['bracket'][0]:.4f}, x_u = {r0['bracket'][1]:.4f}",
                    "Verify f(x_l)·f(x_u) < 0 (sign change confirms root exists)",
                    "Compute midpoint: x_r = (x_l + x_u) / 2",
                    "Evaluate |Ea| = |(x_r_new - x_r_old)| / |x_r_new| × 100%",
                    "If f(x_l)·f(x_r) < 0 → root in 1st half → set x_u = x_r",
                    "If f(x_l)·f(x_r) > 0 → root in 2nd half → set x_l = x_r",
                    f"Stop when |Ea| < εs = {tol} → root ≈ {r0['root']:.8f}",
                ],
                "Regula Falsi": [
                    f"Initial bracket: x_L = {r0['bracket'][0]:.4f}, x_U = {r0['bracket'][1]:.4f}",
                    "Draw straight line between [x_L, f(x_L)] and [x_U, f(x_U)]",
                    "x_R = [x_U·f(x_L) - x_L·f(x_U)] / [f(x_L) - f(x_U)]",
                    "Compute Ea = |(x_R_new - x_R_old) / x_R_new|",
                    "Update bracket: f(x_L)·f(x_R) < 0 → x_U = x_R, else x_L = x_R",
                    f"Converged after {r0['iterations']} iterations → x ≈ {r0['root']:.8f}",
                ],
                "Newton-Raphson Method": [
                    f"Initial guess x_0 = midpoint of bracket [{r0['bracket'][0]:.4f}, {r0['bracket'][1]:.4f}]",
                    "Compute f(x_i) and f'(x_i) — the function and its derivative",
                    "Apply formula: x_{i+1} = x_i - f(x_i) / f'(x_i)",
                    "Error: |Ea| = |(x_{i+1} - x_i) / x_{i+1}|",
                    "If f'(x_i) ≈ 0 → method fails (division by zero risk)",
                    f"Converged in {r0['iterations']} iterations → x ≈ {r0['root']:.8f}",
                ],
                "Secant Method": [
                    f"Two initial points from bracket [{r0['bracket'][0]:.4f}, {r0['bracket'][1]:.4f}]",
                    "Approximates derivative: uses finite difference instead of f'(x)",
                    "x_{i+1} = x_i - f(x_i)·(x_i - x_{i-1}) / (f(x_i) - f(x_{i-1}))",
                    "Error: |Ea| = |(x_{i+1} - x_i) / x_{i+1}|",
                    "Does not require symbolic differentiation — more robust for complex f(x)",
                    f"Converged in {r0['iterations']} iterations → x ≈ {r0['root']:.8f}",
                ],
            }

            method_used = r0['method']
            steps = steps_by_method.get(method_used, ["No steps available."])

            st.markdown(f'<div class="info-chip">Method: <b>{method_used}</b> &nbsp;·&nbsp; '
                        f'Equation: <b>f(x) = {st.session_state.last_eq[:50]}</b></div>', unsafe_allow_html=True)

            for si, step in enumerate(steps):
                st.markdown(f"""<div class="step-card">
                    <div class="step-num">{si+1}</div>
                    <div class="step-text">{step}</div>
                </div>""", unsafe_allow_html=True)

            # First 3 iteration detail (expandable)
            if r0['rows']:
                with st.expander("⊞ Expand Iteration Detail (first 5 rows)"):
                    st.dataframe(pd.DataFrame(r0['rows'][:5]), use_container_width=True)
                    if len(r0['rows']) > 5:
                        st.markdown(f'<div class="info-chip">… and {len(r0["rows"])-5} more iterations. See Iteration Tables tab.</div>', unsafe_allow_html=True)

else:
    # ── PLACEHOLDER ──
    st.markdown("""
    <div class="nx-card" style="min-height:520px;">
      <div class="nx-placeholder">
        <div class="icon">∿</div>
        <div class="title">NumerixPro — Ready to Solve</div>
        Select a method from the sidebar, enter your equation above,<br>
        then press <b>Solve</b> to find all roots automatically.<br><br>
        ∿ &nbsp; Multi-root detection across any interval<br>
        ▦ &nbsp; Reference-format iteration tables<br>
        ◈ &nbsp; Error convergence visualization<br>
        ⊞ &nbsp; Compare all 5 methods side-by-side<br>
        ⬇ &nbsp; Export results to CSV<br><br>
        Supports: <b>ln(x)</b> · <b>exp(x)</b> · <b>polynomials</b> · <b>mixed nonlinear</b>
      </div>
    </div>
    """, unsafe_allow_html=True)
