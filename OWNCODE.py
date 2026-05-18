import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MathStudio Pro", page_icon="📐", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Source+Sans+3:wght@300;400;600&display=swap');

    /* ── Global background & base text ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #F0C294 !important;
        font-family: 'Source Sans 3', sans-serif;
        color: #3b2712;
    }

    [data-testid="stHeader"] { background: transparent !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #c8895a !important;
        border-right: 3px solid #a0623a;
    }
    [data-testid="stSidebar"] * { color: #fff3e8 !important; }
    [data-testid="stSidebar"] .stRadio label { font-family: 'Source Sans 3', sans-serif; font-weight: 600; }

    /* ── Page titles ── */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700;
        color: #5c2f0e !important;
        letter-spacing: -0.5px;
        border-bottom: 3px solid #c8895a;
        padding-bottom: 8px;
    }
    h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #6b3a1f !important;
    }

    /* ── LIGHT BROWN BOXES (generic containers) ── */
    .brown-box {
        background: #dba97a;
        border: 1.5px solid #b87040;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 4px 4px 14px rgba(90,45,10,0.15);
    }

    /* ── Metric cards (root finding) ── */
    .metric-strip {
        display: flex;
        gap: 16px;
        margin: 12px 0 20px 0;
    }
    .metric-tile {
        flex: 1;
        background: #c8895a;
        border: 2px solid #a0623a;
        border-radius: 10px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 3px 3px 10px rgba(80,35,5,0.18);
    }
    .metric-tile .label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #fff3e8;
        margin-bottom: 4px;
    }
    .metric-tile .value {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 700;
        color: #fff8f0;
    }

    /* ── Horizontal result strip (matrix) ── */
    .result-banner {
        background: linear-gradient(135deg, #c8895a, #dba97a);
        border: 2px solid #a0623a;
        border-radius: 14px;
        padding: 18px 28px;
        margin: 18px 0;
        font-family: 'Playfair Display', serif;
        font-size: 17px;
        color: #fff3e8;
        box-shadow: 4px 4px 16px rgba(80,35,5,0.2);
    }

    /* ── Inputs, selects, number inputs ── */
    .stTextInput input, .stNumberInput input, .stSelectbox select,
    [data-testid="stNumberInput"] input {
        background: #f5dfc4 !important;
        border: 1.5px solid #b87040 !important;
        border-radius: 8px !important;
        color: #3b2712 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: #8b4513 !important;
        color: #fff8f0 !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 0 !important;
        width: 100% !important;
        letter-spacing: 0.5px;
        box-shadow: 3px 3px 10px rgba(80,35,5,0.25);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: #a0522d !important;
        transform: translateY(-2px);
        box-shadow: 4px 6px 14px rgba(80,35,5,0.3);
    }

    /* ── Divider ── */
    hr { border-color: #b87040 !important; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1.5px solid #b87040 !important;
        border-radius: 8px;
        overflow: hidden;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #dba97a !important;
        border-radius: 8px !important;
        font-weight: 600;
        color: #5c2f0e !important;
    }

    /* ── Info / toast boxes ── */
    [data-testid="stAlert"] {
        background: #dba97a !important;
        border-left: 4px solid #8b4513 !important;
        border-radius: 8px !important;
        color: #3b2712 !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #8b4513 !important; }

    /* ── Section header pill ── */
    .section-pill {
        display: inline-block;
        background: #8b4513;
        color: #fff8f0;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 12px;
    }

    /* ── Matrix column card ── */
    .matrix-card {
        background: #dba97a;
        border: 1.5px solid #b87040;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 4px 4px 14px rgba(90,45,10,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("<h2 style='font-family:Playfair Display,serif; margin-bottom:4px;'>📐 MathStudio Pro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("Select Module", ["Root Finding Analysis", "Advanced Matrix Operations"])
st.sidebar.markdown("---")
st.sidebar.info("Developed with Streamlit & Python")


# ══════════════════════════════════════════
# MODULE 1: ROOT FINDING  — vertical-panel layout
# Left: narrow settings panel | Right: wide results area
# ══════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.title("Root Finding Analysis")
    st.markdown("Analyze equations and find roots using classical numerical methods.")

    # Two-column split: settings (narrow) | results (wide)
    col_input, col_results = st.columns([1, 2.5])

    with col_input:
        st.markdown('<div class="brown-box">', unsafe_allow_html=True)
        st.markdown('<span class="section-pill">⚙ Parameters</span>', unsafe_allow_html=True)

        eq_str = st.text_input("Equation f(x)", value="x**3 - x - 2")
        method = st.selectbox("Algorithm", [
            "Incremental Search", "Bisection Method",
            "Regula-Falsi", "Newton-Raphson", "Secant Method"
        ])

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            xl = st.number_input("Lower Bound (xl)", value=1.0)
            xu = st.number_input("Upper Bound (xu)", value=2.0)
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess (x0)", value=1.0)
        elif method == "Secant Method":
            x0 = st.number_input("First Guess (x0)", value=1.0)
            x1 = st.number_input("Second Guess (x1)", value=2.0)

        tol      = st.number_input("Tolerance", value=0.0001, format="%.5f")
        max_iter = st.number_input("Max Iterations", value=50, step=1)

        st.markdown("</div>", unsafe_allow_html=True)
        solve_btn = st.button("Calculate Root")

    with col_results:
        if solve_btn:
            try:
                x    = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f    = sp.lambdify(x, expr, 'numpy')
                df   = sp.lambdify(x, sp.diff(expr, x), 'numpy')

                results, root, iterations, final_err = [], None, 0, 0

                if method == "Bisection Method":
                    for i in range(int(max_iter)):
                        xr  = (xl + xu) / 2
                        err = abs(xu - xl) / 2
                        results.append({"Iter": i+1, "xl": xl, "xu": xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if f(xr) == 0 or err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(xl) * f(xr) < 0: xu = xr
                        else: xl = xr

                elif method == "Regula-Falsi":
                    for i in range(int(max_iter)):
                        xr  = xu - (f(xu)*(xl - xu)) / (f(xl) - f(xu))
                        err = abs(f(xr))
                        results.append({"Iter": i+1, "xl": xl, "xu": xu, "xr": xr, "f(xr)": f(xr), "Error": err})
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break
                        if f(xl) * f(xr) < 0: xu = xr
                        else: xl = xr

                elif method == "Newton-Raphson":
                    xr = x0
                    for i in range(int(max_iter)):
                        fxr, dfxr = f(xr), df(xr)
                        xr_new    = xr - fxr/dfxr
                        err       = abs(xr_new - xr)
                        results.append({"Iter": i+1, "xi": xr, "f(xi)": fxr, "f'(xi)": dfxr, "xi+1": xr_new, "Error": err})
                        xr = xr_new
                        if err < tol:
                            root, iterations, final_err = xr, i+1, err; break

                elif method == "Secant Method":
                    for i in range(int(max_iter)):
                        fx1, fx0 = f(x1), f(x0)
                        x2  = x1 - (fx1 * (x0 - x1)) / (fx0 - fx1)
                        err = abs(x2 - x1)
                        results.append({"Iter": i+1, "x(i-1)": x0, "x(i)": x1, "x(i+1)": x2, "f(x(i+1))": f(x2), "Error": err})
                        x0, x1 = x1, x2
                        if err < tol:
                            root, iterations, final_err = x2, i+1, err; break

                elif method == "Incremental Search":
                    step, curr_x = 0.1, xl
                    for i in range(int(max_iter)):
                        next_x = curr_x + step
                        results.append({"Iter": i+1, "x": curr_x, "f(x)": f(curr_x)})
                        if f(curr_x) * f(next_x) < 0:
                            root, iterations = (curr_x + next_x)/2, i+2; break
                        curr_x = next_x

                if root is not None:
                    st.toast('Calculation Complete!', icon='✅')

                    # ── Three horizontal metric tiles ──
                    st.markdown(f"""
                        <div class="metric-strip">
                            <div class="metric-tile">
                                <div class="label">Calculated Root</div>
                                <div class="value">{root:.6f}</div>
                            </div>
                            <div class="metric-tile">
                                <div class="label">Total Iterations</div>
                                <div class="value">{iterations}</div>
                            </div>
                            <div class="metric-tile">
                                <div class="label">Final Error</div>
                                <div class="value">{f"{final_err:.6f}" if final_err else "N/A"}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # ── Plotly graph inside a brown box ──
                    st.markdown('<div class="brown-box">', unsafe_allow_html=True)
                    st.markdown('<span class="section-pill">📈 Interactive Graph</span>', unsafe_allow_html=True)

                    x_vals = np.linspace(root - 3, root + 3, 300)
                    y_vals = f(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#8b4513', width=3)
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="#5c2f0e", line_width=1)
                    fig.add_vline(x=0, line_dash="dash", line_color="#5c2f0e", line_width=1)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name='Root',
                        marker=dict(color='#c0392b', size=14, symbol='x-thin', line=dict(width=3, color='#c0392b'))
                    ))
                    fig.update_layout(
                        plot_bgcolor='#f5dfc4',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#3b2712'),
                        xaxis=dict(gridcolor='#c8a07a', zerolinecolor='#8b6040'),
                        yaxis=dict(gridcolor='#c8a07a', zerolinecolor='#8b6040'),
                        legend=dict(bgcolor='#dba97a', bordercolor='#b87040', borderwidth=1),
                        margin=dict(l=0, r=0, t=20, b=0),
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # ── Expandable iteration table ──
                    with st.expander("📊 View Detailed Iteration History"):
                        st.dataframe(pd.DataFrame(results), use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")


# ══════════════════════════════════════════
# MODULE 2: MATRIX OPS  — card-stack layout
# Full-width operation selector → stacked matrix cards (centered, side-by-side) → result banner
# ══════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    st.title("Advanced Matrix Operations")
    st.markdown("Select an operation, fill in the matrix cells, then execute.")

    # ── Full-width operation chooser ──
    st.markdown('<div class="brown-box">', unsafe_allow_html=True)
    st.markdown('<span class="section-pill">🔢 Operation</span>', unsafe_allow_html=True)
    op = st.selectbox("", [
        "Addition", "Multiplication", "System of Equations (Ax = B)",
        "Adjoint", "Inverse", "Determinant", "Power of Matrix", "Transpose"
    ], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    needs_B = op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]

    # ── Matrix input cards ──
    if needs_B:
        col1, col2 = st.columns(2, gap="large")
    else:
        col1, _ = st.columns([1, 1])

    with col1:
        st.markdown('<div class="brown-box">', unsafe_allow_html=True)
        st.markdown('<span class="section-pill">Matrix A</span>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        rows_A = c1.number_input("Rows A", 1, 10, 3)
        cols_A = c2.number_input("Cols A", 1, 10, 3)
        df_A     = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"C{i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A        = edited_A.to_numpy()

        if op == "Power of Matrix":
            st.markdown("---")
            st.markdown('<span class="section-pill">⚙ Settings</span>', unsafe_allow_html=True)
            power = st.number_input("Exponent (n)", value=2, step=1)
        st.markdown("</div>", unsafe_allow_html=True)

    if needs_B:
        with col2:
            st.markdown('<div class="brown-box">', unsafe_allow_html=True)
            st.markdown('<span class="section-pill">Matrix B</span>', unsafe_allow_html=True)

            if op == "System of Equations (Ax = B)":
                st.info("B must be a single-column vector (same rows as A).")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:
                c1, c2 = st.columns(2)
                rows_B = c1.number_input("Rows B", 1, 10, int(cols_A), disabled=True)
                cols_B = c2.number_input("Cols B", 1, 10, 3)

            df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B        = edited_B.to_numpy()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Execute button (full width) ──
    if st.button("▶  Execute Matrix Operation", use_container_width=True):
        try:
            with st.spinner("Calculating…"):
                time.sleep(0.4)

            # ── Result banner header ──
            st.markdown(f'<div class="result-banner">✔ Operation: <b>{op}</b> — Result below</div>', unsafe_allow_html=True)

            if op == "Addition":
                result = A + B
            elif op == "Multiplication":
                result = np.matmul(A, B)
            elif op == "Transpose":
                result = A.T
            elif op == "Determinant":
                det = np.linalg.det(A)
                st.markdown(f"""
                    <div class="metric-strip">
                        <div class="metric-tile" style="max-width:280px;">
                            <div class="label">Determinant Value</div>
                            <div class="value">{det:.4f}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                result = None
            elif op == "Inverse":
                result = np.linalg.inv(A)
            elif op == "Adjoint":
                result = np.round(np.linalg.inv(A) * np.linalg.det(A), 4)
            elif op == "Power of Matrix":
                result = np.linalg.matrix_power(A, int(power))
            elif op == "System of Equations (Ax = B)":
                result = np.linalg.solve(A, B)
                st.success("Solutions for Vector X:")

            if result is not None:
                st.markdown('<div class="brown-box">', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(result), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.toast('Operation Successful!', icon='✅')

        except np.linalg.LinAlgError as e:
            st.error(f"Math Error: {e}")
        except ValueError as e:
            st.error(f"Dimension Error: {e}")
