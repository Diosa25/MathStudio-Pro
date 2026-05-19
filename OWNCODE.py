import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MathStudio Pro",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── WARM SANDY THEME ────────────────────────────────────────────────────────
BG       = "#F0C294"   # RGB(0.94, 0.76, 0.58)  – main background
CARD     = "#D9A97A"   # light brown – widget cards / boxes
CARD2    = "#C8895A"   # medium brown – accent panels
DARK     = "#6B3F1E"   # deep brown – text / headings
LIGHT    = "#FBF0E4"   # cream white – inner contrast
ACCENT   = "#A0522D"   # sienna – buttons / highlights
SHADOW   = "rgba(107,63,30,0.18)"

st.markdown(f"""
<style>
/* ── Global background ─────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"] {{
    background-color: {BG};
    font-family: 'Georgia', serif;
}}

/* ── Sidebar ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {CARD2} 0%, {DARK} 100%);
}}
[data-testid="stSidebar"] * {{
    color: {LIGHT} !important;
}}
[data-testid="stSidebar"] .stRadio label {{
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 6px 12px;
    margin: 3px 0;
    display: block;
    transition: background 0.2s;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(255,255,255,0.18);
}}

/* ── All input widgets → cream background ───────────────────── */
.stTextInput input, .stNumberInput input,
.stSelectbox > div > div,
[data-testid="stDataEditor"] {{
    background-color: {LIGHT} !important;
    border: 1.5px solid {CARD2} !important;
    border-radius: 8px !important;
    color: {DARK} !important;
}}

/* ── Buttons ────────────────────────────────────────────────── */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, {DARK});
    color: {LIGHT};
    border: none;
    border-radius: 10px;
    font-weight: bold;
    font-size: 15px;
    padding: 10px 20px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 14px {SHADOW};
    transition: transform 0.2s, box-shadow 0.2s;
    width: 100%;
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 7px 20px {SHADOW};
}}

/* ── Cards / info boxes ─────────────────────────────────────── */
.param-card {{
    background: {CARD};
    border-radius: 14px;
    padding: 22px 20px;
    box-shadow: 0 4px 18px {SHADOW};
    margin-bottom: 18px;
}}
.result-banner {{
    background: linear-gradient(120deg, {CARD2}, {ACCENT});
    border-radius: 14px;
    padding: 18px 24px;
    color: {LIGHT};
    margin-bottom: 16px;
    box-shadow: 0 4px 18px {SHADOW};
}}
.module-header {{
    background: linear-gradient(120deg, {DARK} 0%, {ACCENT} 100%);
    border-radius: 16px;
    padding: 28px 36px;
    color: {LIGHT};
    margin-bottom: 28px;
    box-shadow: 0 6px 24px {SHADOW};
}}
.module-header h1 {{
    margin: 0;
    font-size: 2.1rem;
    letter-spacing: 1px;
}}
.module-header p {{
    margin: 6px 0 0;
    font-size: 0.95rem;
    opacity: 0.85;
}}
.section-title {{
    color: {DARK};
    font-size: 1.1rem;
    font-weight: bold;
    border-left: 4px solid {ACCENT};
    padding-left: 10px;
    margin-bottom: 12px;
}}
.metric-strip {{
    background: {CARD};
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 2px 10px {SHADOW};
}}

/* ── Dataframe table headers ────────────────────────────────── */
[data-testid="stDataFrame"] th {{
    background-color: {CARD2} !important;
    color: {LIGHT} !important;
}}

/* ── Expander ───────────────────────────────────────────────── */
[data-testid="stExpander"] {{
    background: {CARD};
    border-radius: 10px;
    border: none !important;
}}

/* ── Divider ────────────────────────────────────────────────── */
hr {{ border-color: {CARD2}; }}

/* ── Metric ─────────────────────────────────────────────────── */
[data-testid="stMetricValue"] {{
    color: {DARK} !important;
    font-size: 1.5rem !important;
}}
[data-testid="stMetricLabel"] {{
    color: {ACCENT} !important;
}}

/* ── Spinner / success / error ──────────────────────────────── */
.stAlert {{ border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 📐 MathStudio Pro")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio(
    "Choose Module",
    ["Root Finding Analysis", "Advanced Matrix Operations"]
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<small style='color:#FBF0E4;opacity:0.7'>Powered by Streamlit & SymPy</small>",
    unsafe_allow_html=True
)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 – ROOT FINDING
#  NEW LAYOUT: full-width banner header → horizontal param strip (3 cols) →
#              method-specific inputs row → full-width graph + metrics →
#              collapsible iteration table
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":

    st.markdown("""
    <div class="module-header">
        <h1>🔍 Root Finding Analysis</h1>
        <p>Solve equations numerically using classical algorithms — visualized step by step.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top param strip ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">⚙️ Configuration</div>', unsafe_allow_html=True)

    top1, top2, top3, top4 = st.columns([2, 1.5, 1, 1])
    with top1:
        eq_str = st.text_input("Equation  f(x)", value="x**3 - x - 2",
                               help="Use Python syntax, e.g. x**2 - 4*x + 3")
    with top2:
        method = st.selectbox("Algorithm", [
            "Bisection Method", "Regula-Falsi", "Newton-Raphson",
            "Secant Method", "Incremental Search"
        ])
    with top3:
        tol     = st.number_input("Tolerance", value=0.0001, format="%.5f")
    with top4:
        max_iter = st.number_input("Max Iterations", value=50, step=1)

    # ── Method-specific inputs in a card ──────────────────────────────────────
    st.markdown('<div class="section-title">📥 Method Inputs</div>', unsafe_allow_html=True)

    with st.container():
        mi1, mi2, mi3 = st.columns([1, 1, 2])

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            with mi1:
                xl = st.number_input("Lower Bound  (xl)", value=1.0)
            with mi2:
                xu = st.number_input("Upper Bound  (xu)", value=2.0)
        elif method == "Newton-Raphson":
            with mi1:
                x0 = st.number_input("Initial Guess  (x0)", value=1.0)
        elif method == "Secant Method":
            with mi1:
                x0 = st.number_input("First Guess  (x0)", value=1.0)
            with mi2:
                x1 = st.number_input("Second Guess  (x1)", value=2.0)

        with mi3:
            st.markdown("<br>", unsafe_allow_html=True)
            solve_btn = st.button("▶  Calculate Root")

    st.markdown("---")

    # ── Results ────────────────────────────────────────────────────────────────
    if solve_btn:
        try:
            x_sym = sp.Symbol('x')
            expr  = sp.sympify(eq_str)
            f     = sp.lambdify(x_sym, expr, 'numpy')
            df_fn = sp.lambdify(x_sym, sp.diff(expr, x_sym), 'numpy')

            results, root, iterations, final_err = [], None, 0, 0

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
                    fxr, dfxr = f(xr), df_fn(xr)
                    xr_new    = xr - fxr/dfxr
                    err       = abs(xr_new - xr)
                    results.append({"Iter": i+1, "xi": xr, "f(xi)": fxr, "f'(xi)": dfxr, "xi+1": xr_new, "Error": err})
                    xr = xr_new
                    if err < tol:
                        root, iterations, final_err = xr, i+1, err; break

            elif method == "Secant Method":
                for i in range(max_iter):
                    fx1, fx0 = f(x1), f(x0)
                    x2       = x1 - (fx1*(x0 - x1)) / (fx0 - fx1)
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

            if root is not None:
                st.toast("Calculation complete!", icon="✅")

                # ── Metrics row ──────────────────────────────────────────────
                mc1, mc2, mc3, mc4 = st.columns(4)
                mc1.metric("Calculated Root",  f"{root:.6f}")
                mc2.metric("Total Iterations", iterations)
                mc3.metric("Final Error",       f"{final_err:.2e}" if final_err else "N/A")
                mc4.metric("Method Used",       method.split()[0])

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Graph (full width) ───────────────────────────────────────
                x_vals = np.linspace(root - 3, root + 3, 400)
                y_vals = f(x_vals)

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=x_vals, y=y_vals, mode='lines', name='f(x)',
                    line=dict(color='#6B3F1E', width=2.5)
                ))
                fig.add_hline(y=0, line_dash="dot", line_color="#A0522D")
                fig.add_vline(x=0, line_dash="dot", line_color="#A0522D")
                fig.add_trace(go.Scatter(
                    x=[root], y=[0], mode='markers', name='Root',
                    marker=dict(color='#C8895A', size=14, symbol='star',
                                line=dict(color='#6B3F1E', width=2))
                ))
                fig.update_layout(
                    title=dict(text=f"f(x) = {eq_str}  |  Root ≈ {root:.6f}",
                               font=dict(color="#6B3F1E", size=15)),
                    paper_bgcolor="rgba(251,240,228,0.7)",
                    plot_bgcolor="rgba(251,240,228,0.7)",
                    xaxis=dict(gridcolor="#D9A97A", title="x"),
                    yaxis=dict(gridcolor="#D9A97A", title="f(x)"),
                    legend=dict(bgcolor="rgba(240,194,148,0.6)"),
                    hovermode="x unified",
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

                # ── Iteration table (collapsible) ────────────────────────────
                with st.expander("📊 Full Iteration History"):
                    st.dataframe(pd.DataFrame(results), use_container_width=True)

        except Exception as e:
            st.error(f"⚠️ Could not evaluate equation. Use Python syntax (e.g. x**2). Details: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 – MATRIX OPERATIONS
#  NEW LAYOUT: centered operation selector → tabbed single/dual matrix input →
#              wide result panel below, no side-by-side clutter
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":

    st.markdown("""
    <div class="module-header">
        <h1>🔢 Advanced Matrix Operations</h1>
        <p>Enter matrices in the interactive grids below, choose an operation and execute.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Operation selector (full width, prominent) ─────────────────────────────
    op_col, _ = st.columns([2, 1])
    with op_col:
        op = st.selectbox(
            "🧮  Select Operation",
            ["Addition", "Multiplication", "System of Equations (Ax = B)",
             "Adjoint", "Inverse", "Determinant", "Power of Matrix", "Transpose"]
        )

    st.markdown("---")

    # ─── Determine if we need one or two matrices ─────────────────────────────
    needs_two = op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]

    # ── Matrix A block ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📋 Matrix A</div>', unsafe_allow_html=True)

    size_row = st.columns([1, 1, 4])
    with size_row[0]:
        rows_A = st.number_input("Rows (A)", 1, 10, 3, key="rA")
    with size_row[1]:
        cols_A = st.number_input("Cols (A)", 1, 10, 3, key="cA")

    df_A    = pd.DataFrame(np.zeros((rows_A, cols_A)),
                           columns=[f"c{i+1}" for i in range(cols_A)])
    edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
    A        = edited_A.to_numpy()

    # ── Matrix B block (conditional) ──────────────────────────────────────────
    if needs_two:
        st.markdown("---")
        st.markdown('<div class="section-title">📋 Matrix B</div>', unsafe_allow_html=True)

        if op == "System of Equations (Ax = B)":
            st.info("Vector B must be a single column (n × 1).", icon="ℹ️")
            rows_B, cols_B = rows_A, 1
        elif op == "Addition":
            rows_B, cols_B = rows_A, cols_A
            st.caption(f"Size locked to match A: {rows_A} × {cols_A}")
        else:  # Multiplication
            b_size = st.columns([1, 1, 4])
            with b_size[0]:
                rows_B = st.number_input("Rows (B)", 1, 10, cols_A,
                                         disabled=True, key="rB")
            with b_size[1]:
                cols_B = st.number_input("Cols (B)", 1, 10, 3, key="cB")

        df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)),
                                columns=[f"c{i+1}" for i in range(cols_B)])
        edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
        B        = edited_B.to_numpy()

    # ── Power setting ──────────────────────────────────────────────────────────
    if op == "Power of Matrix":
        st.markdown("---")
        pw_col, _ = st.columns([1, 3])
        with pw_col:
            power = st.number_input("Exponent  n  (Aⁿ)", value=2, step=1)

    # ── Execute button ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        run_btn = st.button("⚡  Execute Matrix Operation")

    st.markdown("---")

    # ── Computation & output ────────────────────────────────────────────────────
    if run_btn:
        try:
            with st.spinner("Computing…"):
                time.sleep(0.4)

            result = None

            if op == "Addition":
                result = A + B
            elif op == "Multiplication":
                result = np.matmul(A, B)
            elif op == "Transpose":
                result = A.T
            elif op == "Determinant":
                det_val = np.linalg.det(A)
                st.markdown('<div class="section-title">📤 Result</div>',
                            unsafe_allow_html=True)
                _, d_col, _ = st.columns([1, 1, 1])
                with d_col:
                    st.metric("Determinant of A", f"{det_val:.6f}")
                result = None
            elif op == "Inverse":
                result = np.linalg.inv(A)
            elif op == "Adjoint":
                result = np.round(np.linalg.inv(A) * np.linalg.det(A), 6)
            elif op == "Power of Matrix":
                result = np.linalg.matrix_power(A, int(power))
            elif op == "System of Equations (Ax = B)":
                result = np.linalg.solve(A, B)
                st.success("✅ Solution vector  X  found!", icon="✅")

            if result is not None:
                st.markdown('<div class="section-title">📤 Resulting Matrix</div>',
                            unsafe_allow_html=True)

                # Label columns nicely
                if result.ndim == 1:
                    res_df = pd.DataFrame(result, columns=["Value"])
                else:
                    res_df = pd.DataFrame(result,
                                          columns=[f"Col {i+1}" for i in range(result.shape[1])],
                                          index=[f"Row {i+1}" for i in range(result.shape[0])])
                st.dataframe(res_df, use_container_width=True)
                st.toast("Operation successful!", icon="✅")

        except np.linalg.LinAlgError as e:
            st.error(f"⚠️ Mathematical Error: {e}  (Matrix may be singular or non-invertible.)")
        except ValueError as e:
            st.error(f"⚠️ Dimension Mismatch: {e}")
