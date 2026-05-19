import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MathStudio Pro", page_icon="📐", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS: LIGHT/DARK BROWN PROFESSIONAL THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

    /* ── ROOT VARIABLES ─────────────────────────────── */
    :root {
        --brown-900: #2C1A0E;
        --brown-800: #3E2410;
        --brown-700: #5C3317;
        --brown-600: #7A4520;
        --brown-500: #9B6B45;
        --brown-400: #B98A64;
        --brown-300: #D4AA88;
        --brown-200: #E8CFB0;
        --brown-100: #F5E9D8;
        --brown-50:  #FBF5EC;
        --cream:     #FAF3E8;
        --gold:      #C8923A;
        --gold-light:#E8B86D;
        --text-dark: #1E0F05;
        --text-mid:  #4A2C12;
        --text-light:#7A5535;
    }

    /* ── GLOBAL APP BACKGROUND ───────────────────────── */
    .stApp {
        background: linear-gradient(160deg, var(--cream) 0%, #F0E6D3 60%, #E8D5B8 100%);
        font-family: 'Source Sans 3', sans-serif;
        color: var(--text-dark);
    }

    /* ── SIDEBAR ─────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--brown-900) 0%, var(--brown-800) 50%, var(--brown-700) 100%) !important;
        border-right: 3px solid var(--gold) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--brown-100) !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(200,146,58,0.25) !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s ease !important;
        display: block !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(200,146,58,0.18) !important;
        border-color: var(--gold) !important;
    }
    [data-testid="stSidebar"] .stMarkdown hr {
        border-color: rgba(200,146,58,0.35) !important;
    }

    /* ── PAGE TITLE BANNER ───────────────────────────── */
    .page-banner {
        background: linear-gradient(135deg, var(--brown-900) 0%, var(--brown-700) 55%, var(--brown-600) 100%);
        border-radius: 14px;
        padding: 28px 36px 22px;
        margin-bottom: 28px;
        border-left: 5px solid var(--gold);
        box-shadow: 0 6px 30px rgba(44,26,14,0.18);
    }
    .page-banner h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important;
        color: var(--brown-50) !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: 0.03em;
    }
    .page-banner p {
        color: var(--brown-300) !important;
        font-size: 0.95rem !important;
        margin: 0 !important;
        font-weight: 300;
    }
    .banner-accent {
        width: 48px; height: 3px;
        background: linear-gradient(90deg, var(--gold), transparent);
        margin-top: 14px;
        border-radius: 2px;
    }

    /* ── SECTION CARDS ───────────────────────────────── */
    .card {
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(185,138,100,0.30);
        border-radius: 12px;
        padding: 22px 22px 18px;
        box-shadow: 0 2px 16px rgba(92,51,23,0.08);
        margin-bottom: 10px;
    }
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.08rem;
        font-weight: 600;
        color: var(--brown-800);
        letter-spacing: 0.02em;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, var(--brown-300), transparent);
        margin-left: 8px;
    }

    /* ── METRIC CARDS ────────────────────────────────── */
    .metric-row {
        display: flex;
        gap: 14px;
        margin: 18px 0 12px;
    }
    .metric-box {
        flex: 1;
        background: linear-gradient(135deg, var(--brown-900) 0%, var(--brown-700) 100%);
        border-radius: 10px;
        padding: 16px 14px 14px;
        text-align: center;
        border: 1px solid var(--brown-600);
        box-shadow: 0 3px 14px rgba(44,26,14,0.14);
    }
    .metric-label {
        font-size: 0.72rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: var(--brown-300);
        margin-bottom: 6px;
        font-weight: 500;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.45rem;
        font-weight: 700;
        color: var(--gold-light);
    }

    /* ── INPUTS ──────────────────────────────────────── */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        background: rgba(255,255,255,0.9) !important;
        border: 1.5px solid var(--brown-300) !important;
        border-radius: 8px !important;
        color: var(--text-dark) !important;
        font-family: 'Source Sans 3', sans-serif !important;
        transition: border-color 0.2s ease !important;
    }
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(200,146,58,0.15) !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: var(--brown-700) !important;
    }

    /* ── PRIMARY BUTTON ──────────────────────────────── */
    .stButton>button {
        background: linear-gradient(135deg, var(--brown-800) 0%, var(--brown-600) 100%) !important;
        color: var(--brown-50) !important;
        border: 1.5px solid var(--brown-500) !important;
        border-radius: 9px !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        padding: 12px 0 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 3px 12px rgba(44,26,14,0.20) !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, var(--brown-700) 0%, var(--gold) 100%) !important;
        border-color: var(--gold) !important;
        box-shadow: 0 5px 20px rgba(200,146,58,0.30) !important;
        transform: translateY(-1px) !important;
    }
    .stButton>button:active {
        transform: translateY(0) !important;
    }

    /* ── DIVIDER ─────────────────────────────────────── */
    hr {
        border: none !important;
        border-top: 1.5px solid var(--brown-200) !important;
        margin: 20px 0 !important;
    }

    /* ── DATA TABLE ──────────────────────────────────── */
    .stDataFrame {
        border: 1px solid var(--brown-200) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* ── EXPANDER ────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--brown-100) !important;
        border-radius: 8px !important;
        border: 1px solid var(--brown-200) !important;
        font-weight: 600 !important;
        color: var(--brown-800) !important;
    }
    .streamlit-expanderContent {
        border: 1px solid var(--brown-200) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ── ALERTS ──────────────────────────────────────── */
    .stSuccess {
        background: rgba(122, 69, 32, 0.08) !important;
        border-left: 4px solid var(--gold) !important;
        border-radius: 8px !important;
        color: var(--brown-800) !important;
    }
    .stError {
        border-left: 4px solid #C0392B !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background: rgba(200,146,58,0.08) !important;
        border-left: 4px solid var(--brown-400) !important;
        border-radius: 8px !important;
        color: var(--brown-700) !important;
    }

    /* ── SPINNER ─────────────────────────────────────── */
    .stSpinner > div {
        border-top-color: var(--gold) !important;
    }

    /* ── HIDE DEFAULT STREAMLIT CHROME ───────────────── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
    </style>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px;">
            <div style="font-size:2.4rem; margin-bottom:4px;">📐</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.35rem; font-weight:700;
                        color:#F5E9D8; letter-spacing:0.04em;">MathStudio</div>
            <div style="font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase;
                        color:#B98A64; font-weight:500;">Pro Edition</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;color:#9B6B45;font-weight:600;margin-bottom:10px;'>Navigation</div>", unsafe_allow_html=True)
    app_mode = st.radio("", ["Root Finding Analysis", "Advanced Matrix Operations"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.78rem;color:#9B6B45;line-height:1.6;'>Powered by SymPy, NumPy & Plotly<br>Built with Streamlit</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — ROOT FINDING
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":

    st.markdown("""
        <div class="page-banner">
            <h1>Root Finding Analysis</h1>
            <p>Locate roots of equations using classical numerical methods with full iteration history and interactive visualisation.</p>
            <div class="banner-accent"></div>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 2.5], gap="large")

    # ── LEFT PANEL: PARAMETERS ──────────────────────────────────────────────
    with col_input:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⚙️ Configuration</div>', unsafe_allow_html=True)

        eq_str = st.text_input("Equation  f(x)", value="x**3 - x - 2",
                               help="Use Python math syntax, e.g. x**3 - x - 2")
        method = st.selectbox("Algorithm", [
            "Incremental Search", "Bisection Method",
            "Regula-Falsi", "Newton-Raphson", "Secant Method"
        ])

        st.markdown("---")

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            c1, c2 = st.columns(2)
            xl = c1.number_input("Lower Bound  xl", value=1.0)
            xu = c2.number_input("Upper Bound  xu", value=2.0)
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess  x₀", value=1.0)
        elif method == "Secant Method":
            c1, c2 = st.columns(2)
            x0 = c1.number_input("First Guess  x₀", value=1.0)
            x1 = c2.number_input("Second Guess  x₁", value=2.0)

        st.markdown("---")

        c1, c2 = st.columns(2)
        tol      = c1.number_input("Tolerance", value=0.0001, format="%.5f")
        max_iter = c2.number_input("Max Iterations", value=50, step=1)

        st.markdown("<br>", unsafe_allow_html=True)
        solve_btn = st.button("▶  Calculate Root")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT PANEL: RESULTS ────────────────────────────────────────────────
    with col_results:
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
                        else:                  xl = xr

                elif method == "Regula-Falsi":
                    for i in range(max_iter):
                        xr  = xu - (f(xu)*(xl - xu)) / (f(xl) - f(xu))
                        err = abs(f(xr))
                        results.append({"Iter": i+1, "xl": xl, "xu": xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(xl) * f(xr) < 0: xu = xr
                        else:                  xl = xr

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

                if root is not None:
                    st.toast('Calculation Complete!', icon='✅')

                    # Metric cards
                    st.markdown(f"""
                        <div class="metric-row">
                            <div class="metric-box">
                                <div class="metric-label">Calculated Root</div>
                                <div class="metric-value">{root:.6f}</div>
                            </div>
                            <div class="metric-box">
                                <div class="metric-label">Total Iterations</div>
                                <div class="metric-value">{iterations}</div>
                            </div>
                            <div class="metric-box">
                                <div class="metric-label">Final Error</div>
                                <div class="metric-value">{f"{final_err:.6f}" if final_err else "N/A"}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("---")

                    # Plotly chart — brown/gold palette
                    x_vals = np.linspace(root - 3, root + 3, 300)
                    y_vals = f(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#9B6B45', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dot", line_color="#5C3317", line_width=1)
                    fig.add_vline(x=0, line_dash="dot", line_color="#5C3317", line_width=1)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name='Root',
                        marker=dict(color='#C8923A', size=14, symbol='x',
                                    line=dict(width=3, color='#C8923A'))
                    ))
                    fig.update_layout(
                        title=dict(text="Function Graph", font=dict(family="Playfair Display", size=18, color="#3E2410")),
                        xaxis_title="x", yaxis_title="f(x)",
                        plot_bgcolor="#FAF3E8",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Source Sans 3", color="#4A2C12"),
                        hovermode="x unified",
                        legend=dict(bgcolor="rgba(250,243,232,0.8)", bordercolor="#D4AA88", borderwidth=1),
                        xaxis=dict(gridcolor="#E8CFB0", zerolinecolor="#B98A64"),
                        yaxis=dict(gridcolor="#E8CFB0", zerolinecolor="#B98A64"),
                        margin=dict(l=0, r=0, t=50, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    with st.expander("📊  Detailed Iteration History"):
                        st.dataframe(pd.DataFrame(results), use_container_width=True)

            except Exception as e:
                st.error(f"Error evaluating equation. Use Python syntax (e.g. ** for exponents).\n\nDetails: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — MATRIX OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":

    st.markdown("""
        <div class="page-banner">
            <h1>Advanced Matrix Operations</h1>
            <p>Enter matrix values directly into the interactive grids below, select an operation, and execute.</p>
            <div class="banner-accent"></div>
        </div>
    """, unsafe_allow_html=True)

    # Operation selector at the top
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️  Select Operation</div>', unsafe_allow_html=True)
    op = st.selectbox("", [
        "Addition", "Multiplication", "System of Equations (Ax = B)",
        "Adjoint", "Inverse", "Determinant", "Power of Matrix", "Transpose"
    ], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    needs_B = op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋  Matrix A</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        rows_A = c1.number_input("Rows", 1, 10, 3, key="rA")
        cols_A = c2.number_input("Cols", 1, 10, 3, key="cA")
        df_A     = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"C{i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A        = edited_A.to_numpy()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if needs_B:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📋  Matrix B</div>', unsafe_allow_html=True)

            if op == "System of Equations (Ax = B)":
                st.info("B must be a single-column results vector.")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:  # Multiplication
                c1, c2 = st.columns(2)
                rows_B = c1.number_input("Rows B", 1, 10, cols_A, disabled=True, key="rB")
                cols_B = c2.number_input("Cols B", 1, 10, 3, key="cB")

            df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B        = edited_B.to_numpy()
            st.markdown('</div>', unsafe_allow_html=True)

        elif op == "Power of Matrix":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">⚙️  Power Settings</div>', unsafe_allow_html=True)
            power = st.number_input("Exponent  n", value=2, step=1)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Execute button — centered using columns
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        execute_btn = st.button("▶  Execute Matrix Operation", use_container_width=True)

    if execute_btn:
        try:
            with st.spinner("Computing…"):
                time.sleep(0.4)

            st.markdown("---")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">✅  Result</div>', unsafe_allow_html=True)

            if op == "Addition":
                result = A + B
            elif op == "Multiplication":
                result = np.matmul(A, B)
            elif op == "Transpose":
                result = A.T
            elif op == "Determinant":
                det_val = np.linalg.det(A)
                st.markdown(f"""
                    <div class="metric-row" style="justify-content:center;">
                        <div class="metric-box" style="max-width:260px;">
                            <div class="metric-label">Determinant Value</div>
                            <div class="metric-value">{det_val:.4f}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
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
                st.dataframe(pd.DataFrame(result).rename(
                    columns={i: f"C{i+1}" for i in range(result.shape[1] if result.ndim > 1 else 1)}
                ), use_container_width=True)
                st.toast('Operation Successful!', icon='✅')

            st.markdown('</div>', unsafe_allow_html=True)

        except np.linalg.LinAlgError as e:
            st.error(f"Mathematical Error: {e}  (Matrix may be singular or non-invertible)")
        except ValueError as e:
            st.error(f"Dimension Mismatch: {e}")
