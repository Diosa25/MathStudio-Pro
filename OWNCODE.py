import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Numerical Project",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VINTAGE BROWN AESTHETIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&display=swap');

    /* ──────────────────────────── GLOBAL ──────────────────────────── */
    html, body, [class*="css"], .stApp {
        font-family: 'Crimson Text', Georgia, serif;
        background-color: #F2E8D5;
        color: #2C1A0E;
    }

    .main .block-container {
        padding: 0.8rem 2.5rem 2rem 2.5rem;
        max-width: 100%;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none; }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-track { background: #EDE0C4; }
    ::-webkit-scrollbar-thumb { background: #8B5E3C; border-radius: 4px; }

    /* ──────────────────────────── HEADER ──────────────────────────── */
    .vintage-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.1rem 2rem 1rem 2rem;
        background: linear-gradient(135deg, #2C1A0E 0%, #5C3317 45%, #3B2210 100%);
        border-radius: 14px;
        margin-bottom: 0.3rem;
        box-shadow: 0 6px 24px rgba(44,26,14,0.45), inset 0 1px 0 rgba(212,169,106,0.2);
        border: 1px solid #7A4F2E;
        position: relative;
        overflow: hidden;
    }

    .vintage-header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 20px,
            rgba(212,169,106,0.03) 20px,
            rgba(212,169,106,0.03) 40px
        );
        pointer-events: none;
    }

    .header-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.9rem;
        color: #D4A96A;
        letter-spacing: 0.07em;
        line-height: 1.5;
        font-style: italic;
        text-shadow: 0 1px 3px rgba(0,0,0,0.4);
        min-width: 180px;
    }

    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #F5E6C8;
        letter-spacing: 0.25em;
        text-align: center;
        text-shadow: 1px 2px 6px rgba(0,0,0,0.5);
        font-weight: 700;
        flex: 1;
    }

    .header-right {
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.82rem;
        color: #B8946A;
        text-align: right;
        letter-spacing: 0.05em;
        line-height: 1.6;
        min-width: 180px;
    }

    .ornamental-divider {
        text-align: center;
        color: #9B7245;
        font-size: 1rem;
        letter-spacing: 0.5em;
        margin: 0.4rem 0 0.6rem 0;
        user-select: none;
    }

    /* ──────────────────────────── NAV AREA ──────────────────────────── */
    .nav-strip {
        background: linear-gradient(to right, #EDE0C4, #E5D4AE, #EDE0C4);
        border: 1.5px solid #C4A882;
        border-radius: 10px;
        padding: 0.7rem 1.2rem 0.5rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(59,31,12,0.1), inset 0 1px 0 rgba(255,255,255,0.4);
    }

    /* ──────────────────────────── SECTION TITLE ──────────────────────────── */
    .sec-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        color: #3B1F0C;
        border-bottom: 2px solid #9B7245;
        padding-bottom: 0.3rem;
        margin-bottom: 0.8rem;
        letter-spacing: 0.05em;
    }

    .sec-subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.05rem;
        color: #6B4226;
        font-style: italic;
        margin-bottom: 0.9rem;
    }

    /* ──────────────────────────── INPUT CARD ──────────────────────────── */
    .input-card {
        background: linear-gradient(160deg, #FBF4E6 0%, #F5EAD4 100%);
        border: 1.5px solid #C8A97A;
        border-radius: 12px;
        padding: 1.2rem 1.3rem;
        box-shadow: 3px 4px 16px rgba(59,31,12,0.12), inset 0 1px 0 rgba(255,255,255,0.6);
    }

    .result-card {
        background: linear-gradient(160deg, #FBF4E6 0%, #F7EDD8 100%);
        border: 1.5px solid #C8A97A;
        border-radius: 12px;
        padding: 1.2rem 1.3rem;
        box-shadow: 3px 4px 16px rgba(59,31,12,0.1);
        min-height: 300px;
    }

    .table-section {
        background: linear-gradient(to bottom, #FBF4E6, #F5EAD4);
        border: 1.5px solid #C8A97A;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-top: 0.9rem;
        box-shadow: 3px 4px 16px rgba(59,31,12,0.1);
    }

    /* ──────────────────────────── WIDGET OVERRIDES ──────────────────────────── */
    div[data-testid="stRadio"] > div {
        gap: 0 !important;
    }

    div[data-testid="stRadio"] label > div[data-testid="stMarkdownContainer"] p {
        font-family: 'Playfair Display', serif !important;
        font-size: 1rem !important;
        color: #3B1F0C !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
    }

    .stSelectbox > label,
    .stNumberInput > label,
    .stTextInput > label {
        font-family: 'Crimson Text', serif !important;
        color: #4A2A12 !important;
        font-size: 0.97rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }

    .stSelectbox [data-baseweb="select"] > div,
    .stTextInput input,
    .stNumberInput input {
        border: 1.5px solid #C4A882 !important;
        border-radius: 7px !important;
        background-color: #FBF4E6 !important;
        color: #2C1A0E !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1rem !important;
        box-shadow: inset 0 1px 4px rgba(59,31,12,0.08) !important;
    }

    .stSelectbox [data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #8B5E3C !important;
        box-shadow: 0 0 0 2px rgba(139,94,60,0.18) !important;
    }

    /* ──────────────────────────── BUTTON ──────────────────────────── */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #5C3317 0%, #8B5E3C 60%, #7A4F2E 100%);
        color: #F5E6C8;
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        font-weight: 700;
        border: 1px solid #9B7245;
        letter-spacing: 0.1em;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 3px 12px rgba(59,31,12,0.32), inset 0 1px 0 rgba(255,255,255,0.12);
        transition: all 0.28s ease;
        text-shadow: 0 1px 3px rgba(0,0,0,0.35);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #3B1F0C 0%, #5C3317 100%);
        transform: translateY(-1px);
        box-shadow: 0 5px 18px rgba(59,31,12,0.45);
        color: #FFE8B0;
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* ──────────────────────────── METRICS ──────────────────────────── */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #EDE0C4, #E5D4AE) !important;
        border: 1.5px solid #C4A882 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 2px 3px 10px rgba(59,31,12,0.12) !important;
    }

    [data-testid="stMetricLabel"] p {
        font-family: 'Cormorant Garamond', serif !important;
        color: #6B4226 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        color: #2C1A0E !important;
        font-size: 1.5rem !important;
    }

    /* ──────────────────────────── DATAFRAME ──────────────────────────── */
    [data-testid="stDataFrame"] {
        border: 1.5px solid #C4A882 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* ──────────────────────────── INFO / SUCCESS ──────────────────────────── */
    [data-testid="stInfo"] {
        background-color: #EDE0C4 !important;
        border-left: 4px solid #8B5E3C !important;
        border-radius: 7px !important;
        color: #3B1F0C !important;
    }

    [data-testid="stSuccess"] {
        background-color: #E6DCC8 !important;
        border-left: 4px solid #5C3317 !important;
        border-radius: 7px !important;
    }

    /* ──────────────────────────── HR ──────────────────────────── */
    hr {
        border: none !important;
        border-top: 1.5px solid #C4A882 !important;
        margin: 0.7rem 0 !important;
    }

    /* ──────────────────────────── SPINNER ──────────────────────────── */
    [data-testid="stSpinner"] {
        color: #5C3317 !important;
    }

    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  TOP HEADER
# ═══════════════════════════════════════════════════════
st.markdown("""
    <div class="vintage-header">
        <div class="header-name">DIOSAMABEL B. PENASO<br>BSCOMPE-2</div>
        <div class="header-title">✦ &nbsp; NUMERICAL PROJECT &nbsp; ✦</div>
        <div class="header-right">Numerical Methods<br>Analysis Suite</div>
    </div>
    <div class="ornamental-divider">— ✦ ◆ ✦ —</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  UPPER NAVIGATION STRIP
# ═══════════════════════════════════════════════════════
st.markdown('<div class="nav-strip">', unsafe_allow_html=True)
app_mode = st.radio(
    "**Select Module**",
    ["Root Finding Analysis", "Advanced Matrix Operations"],
    horizontal=True,
    label_visibility="visible"
)
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  SESSION STATE INIT
# ═══════════════════════════════════════════════════════
if "rf_results"    not in st.session_state: st.session_state.rf_results    = []
if "rf_root"       not in st.session_state: st.session_state.rf_root       = None
if "rf_iterations" not in st.session_state: st.session_state.rf_iterations = 0
if "rf_error"      not in st.session_state: st.session_state.rf_error      = 0
if "rf_fig"        not in st.session_state: st.session_state.rf_fig        = None

# ═══════════════════════════════════════════════════════
#  MODULE 1 — ROOT FINDING ANALYSIS
# ═══════════════════════════════════════════════════════
if app_mode == "Root Finding Analysis":
    st.markdown('<div class="sec-title">⚙ Root Finding Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-subtitle">Analyze equations and find roots using classical numerical methods with interactive graph visualization.</div>', unsafe_allow_html=True)

    col_input, col_graph = st.columns([1, 2.3])

    # ── LEFT: INPUT CARD ──
    with col_input:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("**Parameters**")
        eq_str   = st.text_input("Equation f(x)", value="x**3 - x - 2")
        method   = st.selectbox("Algorithm", [
            "Incremental Search",
            "Bisection Method",
            "Regula-Falsi",
            "Newton-Raphson",
            "Secant Method"
        ])

        if method in ["Bisection Method", "Regula-Falsi", "Incremental Search"]:
            xl = st.number_input("Lower Bound (xl)", value=1.0)
            xu = st.number_input("Upper Bound (xu)", value=2.0)
        elif method == "Newton-Raphson":
            x0 = st.number_input("Initial Guess (x0)", value=1.0)
        elif method == "Secant Method":
            x0 = st.number_input("First Guess (x0)",  value=1.0)
            x1 = st.number_input("Second Guess (x1)", value=2.0)

        tol      = st.number_input("Tolerance",       value=0.0001, format="%.5f")
        max_iter = st.number_input("Max Iterations",  value=50, step=1)
        solve_btn = st.button("⟳  Calculate Root")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: GRAPH / METRICS CARD ──
    with col_graph:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        if solve_btn:
            try:
                xs   = sp.Symbol('x')
                expr = sp.sympify(eq_str)
                f    = sp.lambdify(xs, expr, 'numpy')
                df   = sp.lambdify(xs, sp.diff(expr, xs), 'numpy')

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
                        xr  = xu - (f(xu) * (xl - xu)) / (f(xl) - f(xu))
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
                        xr_new = xr - fxr / dfxr
                        err    = abs(xr_new - xr)
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
                            root, iterations, final_err = (curr_x + next_x) / 2, i+2, 0; break
                        curr_x = next_x

                if root is not None:
                    # Build figure
                    x_vals = np.linspace(root - 3, root + 3, 400)
                    y_vals = f(x_vals)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name='f(x)',
                        line=dict(color='#5C3317', width=2.5)
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="#9B7245", line_width=1.2)
                    fig.add_vline(x=0, line_dash="dash", line_color="#9B7245", line_width=1.2)
                    fig.add_trace(go.Scatter(
                        x=[root], y=[0], mode='markers', name='Root',
                        marker=dict(color='#8B1A1A', size=13, symbol='x', line=dict(width=3))
                    ))
                    fig.update_layout(
                        title=dict(
                            text=f"f(x) = {eq_str}",
                            font=dict(family="Playfair Display, serif", size=15, color="#2C1A0E")
                        ),
                        xaxis_title="x", yaxis_title="f(x)",
                        hovermode="x unified",
                        plot_bgcolor='#FBF4E6',
                        paper_bgcolor='#FBF4E6',
                        font=dict(family="Crimson Text, serif", color="#2C1A0E"),
                        xaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882'),
                        yaxis=dict(gridcolor='#E2CFA8', linecolor='#C4A882', zerolinecolor='#C4A882'),
                        legend=dict(bgcolor='#EDE0C4', bordercolor='#C4A882', borderwidth=1,
                                    font=dict(family="Crimson Text, serif")),
                        margin=dict(l=5, r=5, t=40, b=10),
                        height=340
                    )

                    # Persist to session state
                    st.session_state.rf_results    = results
                    st.session_state.rf_root       = root
                    st.session_state.rf_iterations = iterations
                    st.session_state.rf_error      = final_err
                    st.session_state.rf_fig        = fig
                    st.toast('Calculation Complete!', icon='✅')

                else:
                    st.warning("No root found within the specified bounds / iterations.")

            except Exception as e:
                st.error(f"Error: Make sure the equation uses valid Python math (e.g., ** for exponents). → {e}")

        # ── DISPLAY STORED RESULTS ──
        if st.session_state.rf_root is not None:
            m1, m2, m3 = st.columns(3)
            m1.metric("Calculated Root",  f"{st.session_state.rf_root:.6f}")
            m2.metric("Total Iterations", st.session_state.rf_iterations)
            m3.metric("Final Error",
                      f"{st.session_state.rf_error:.2e}" if st.session_state.rf_error else "—")

            st.markdown("<div style='margin-top:0.7rem;'>", unsafe_allow_html=True)
            st.plotly_chart(st.session_state.rf_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='text-align:center; padding:3rem 1rem; color:#9B7245; font-family:"Playfair Display",serif; font-size:1.05rem; font-style:italic;'>
                    ✦ Configure the parameters and press<br>"Calculate Root" to see the result ✦
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── ITERATION TABLE — always visible below ──
    if st.session_state.rf_results:
        st.markdown('<div class="table-section">', unsafe_allow_html=True)
        st.markdown('<div class="sec-title" style="font-size:1.1rem; margin-bottom:0.6rem;">📊 Iteration History</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(st.session_state.rf_results).style.format("{:.7g}"),
            use_container_width=True,
            height=260
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  MODULE 2 — ADVANCED MATRIX OPERATIONS
# ═══════════════════════════════════════════════════════
elif app_mode == "Advanced Matrix Operations":
    st.markdown('<div class="sec-title">⊞ Advanced Matrix Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-subtitle">Use the interactive spreadsheets below to input your matrix data and execute linear algebra operations.</div>', unsafe_allow_html=True)

    op = st.selectbox("Select Operation", [
        "Addition", "Multiplication",
        "System of Equations (Ax = B)",
        "Adjoint", "Inverse", "Determinant",
        "Power of Matrix", "Transpose"
    ])

    st.markdown("<hr>", unsafe_allow_html=True)

    needs_B = op in ["Addition", "Multiplication", "System of Equations (Ax = B)"]
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title" style="font-size:1.05rem;">Matrix A</div>', unsafe_allow_html=True)
        ca1, ca2 = st.columns(2)
        rows_A = ca1.number_input("Rows A", 1, 10, 3)
        cols_A = ca2.number_input("Cols A", 1, 10, 3)
        df_A     = pd.DataFrame(np.zeros((rows_A, cols_A)), columns=[f"C{i+1}" for i in range(cols_A)])
        edited_A = st.data_editor(df_A, use_container_width=True, key="matrix_a")
        A        = edited_A.to_numpy()

    if needs_B:
        with col2:
            st.markdown('<div class="sec-title" style="font-size:1.05rem;">Matrix B</div>', unsafe_allow_html=True)
            if op == "System of Equations (Ax = B)":
                st.info("Matrix B is the results column vector (same rows as A).")
                rows_B, cols_B = rows_A, 1
            elif op == "Addition":
                rows_B, cols_B = rows_A, cols_A
            else:
                cb1, cb2 = st.columns(2)
                rows_B = cb1.number_input("Rows B", 1, 10, int(cols_A), disabled=True)
                cols_B = cb2.number_input("Cols B", 1, 10, 3)
            df_B     = pd.DataFrame(np.zeros((rows_B, cols_B)), columns=[f"C{i+1}" for i in range(cols_B)])
            edited_B = st.data_editor(df_B, use_container_width=True, key="matrix_b")
            B        = edited_B.to_numpy()
    else:
        with col2:
            if op == "Power of Matrix":
                st.markdown('<div class="sec-title" style="font-size:1.05rem;">Settings</div>', unsafe_allow_html=True)
                power = st.number_input("Exponent (n)", value=2, step=1)
            else:
                st.markdown("""
                    <div style='padding:1.5rem; text-align:center; color:#9B7245;
                                font-family:"Playfair Display",serif; font-style:italic;
                                font-size:1rem; margin-top:1.5rem;'>
                        This operation acts on Matrix A only.
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    exec_btn = st.button("⊞  Execute Matrix Operation", use_container_width=True)

    if exec_btn:
        try:
            with st.spinner("Processing..."):
                time.sleep(0.4)

            st.markdown('<div class="table-section">', unsafe_allow_html=True)
            st.markdown('<div class="sec-title" style="font-size:1.1rem;">Result</div>', unsafe_allow_html=True)

            result = None
            if   op == "Addition":
                result = A + B
            elif op == "Multiplication":
                result = np.matmul(A, B)
            elif op == "Transpose":
                result = A.T
            elif op == "Determinant":
                val = np.linalg.det(A)
                st.metric("Determinant Value", f"{val:.6f}")
            elif op == "Inverse":
                result = np.linalg.inv(A)
            elif op == "Adjoint":
                result = np.round(np.linalg.inv(A) * np.linalg.det(A), 6)
            elif op == "Power of Matrix":
                result = np.linalg.matrix_power(A, int(power))
            elif op == "System of Equations (Ax = B)":
                result = np.linalg.solve(A, B)
                st.success("✦  Solutions found for Vector X:")

            if result is not None:
                st.dataframe(pd.DataFrame(result), use_container_width=True, height=280)
                st.toast('Operation Successful!', icon='✅')

            st.markdown('</div>', unsafe_allow_html=True)

        except np.linalg.LinAlgError as e:
            st.error(f"Mathematical Error: {e}  (The matrix may be singular / non-invertible.)")
        except ValueError as e:
            st.error(f"Dimension Mismatch: {e}")
