import io
import re
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DataDetox",
    page_icon="🧼",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def init_state():
    defaults = {
        "page": "landing",
        "analysis_ready": False,
        "uploaded_name": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_css():
    st.markdown("""
    <style>
    :root{
        --bg:#f2ede3;
        --surface:#f6f1e7;
        --surface-2:#efe7da;
        --surface-3:#e8dfd1;
        --text:#1f1f1f;
        --muted:#5f5952;
        --line:#d8cfc3;
        --teal:#0c7a7d;
        --teal-dark:#075f62;
        --teal-soft:#d9ecea;
        --danger:#a55555;
        --shadow1: 8px 8px 18px rgba(166,149,124,0.18);
        --shadow2: -8px -8px 18px rgba(255,250,242,0.78);
        --inset: inset 6px 6px 10px rgba(185,169,145,0.18), inset -6px -6px 10px rgba(255,250,242,0.82);
        --radius: 22px;
    }

    html, body, [class*="css"] {
        color: var(--text) !important;
    }

    .stApp {
        background: var(--bg);
        color: var(--text) !important;
    }

    .stApp p, .stApp span, .stApp div, .stApp label, .stApp li,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: var(--text);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1380px;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--line);
    }

    .hero-shell {
        background: linear-gradient(180deg, #f6f1e7 0%, #f1eadf 100%);
        border: 1px solid rgba(140,120,98,0.10);
        border-radius: 30px;
        padding: 2rem;
        box-shadow: var(--shadow1), var(--shadow2);
    }

    .top-badge {
        display:inline-block;
        background: var(--teal-soft);
        color: var(--teal-dark) !important;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.05;
        font-weight: 800;
        color: var(--text) !important;
        margin-bottom: 0.6rem;
    }

    .hero-subtitle {
        font-size: 1.06rem;
        color: var(--muted) !important;
        max-width: 56rem;
        margin-bottom: 1.4rem;
    }

    .soft-card {
        background: var(--surface);
        border: 1px solid rgba(140,120,98,0.10);
        border-radius: var(--radius);
        padding: 1rem 1.1rem;
        box-shadow: var(--shadow1), var(--shadow2);
    }

    .inset-card {
        background: var(--surface-2);
        border-radius: 18px;
        padding: 1rem;
        box-shadow: var(--inset);
        border: 1px solid rgba(140,120,98,0.06);
    }

    .section-title {
        font-size: 1.12rem;
        font-weight: 800;
        color: var(--text) !important;
        margin-bottom: 0.8rem;
    }

    .muted {
        color: var(--muted) !important;
        font-size: 0.95rem;
    }

    .stat-label {
        color: var(--muted) !important;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }

    .stat-value {
        color: var(--text) !important;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .pill {
        display:inline-block;
        border:1px solid var(--line);
        padding:0.45rem 0.75rem;
        border-radius:999px;
        color:var(--muted) !important;
        margin-right:0.4rem;
        margin-bottom:0.4rem;
        background:#f8f4ec;
    }

    .status-pass {
        background: #e2f2ee;
        border: 1px solid #b7ddd6;
        color: #175a55 !important;
        border-radius: 16px;
        padding: 0.95rem 1rem;
        font-weight: 700;
    }

    .status-fail {
        background: #f8e6e3;
        border: 1px solid #e5c1bb;
        color: #8b4343 !important;
        border-radius: 16px;
        padding: 0.95rem 1rem;
        font-weight: 700;
    }

    .formula-box {
        background: #f8f4ec;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        color: var(--text) !important;
    }

    .feature-grid {
        display:grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
    }

    .feature-card {
        background: var(--surface);
        border-radius: 22px;
        padding: 1.1rem;
        box-shadow: var(--shadow1), var(--shadow2);
        border: 1px solid rgba(140,120,98,0.08);
        min-height: 160px;
    }

    .feature-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display:flex;
        align-items:center;
        justify-content:center;
        background: var(--teal-soft);
        color: var(--teal-dark) !important;
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
        font-weight: 800;
    }

    .feature-title {
        font-size: 1.02rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        color: var(--text) !important;
    }

    .feature-text {
        font-size: 0.95rem;
        color: var(--muted) !important;
    }

    .nav-bar {
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding: 0.8rem 0 1.2rem 0;
        gap: 1rem;
    }

    .brand {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--text) !important;
    }

    .brand span {
        color: var(--teal-dark) !important;
    }

    .center-note {
        text-align:center;
        color: var(--muted) !important;
        font-size: 0.94rem;
        margin-top: 0.3rem;
    }

    .stButton > button {
        background: linear-gradient(180deg, var(--teal) 0%, var(--teal-dark) 100%);
        color: white !important;
        border: none;
        border-radius: 999px;
        font-weight: 700;
        padding: 0.75rem 1.15rem;
        box-shadow: 0 10px 18px rgba(12,122,125,0.22);
    }

    .stDownloadButton > button {
        border-radius: 999px;
        font-weight: 700;
        border: 1px solid var(--line);
        color: var(--text) !important;
        background: var(--surface);
    }

    div[data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid rgba(140,120,98,0.08);
        padding: 0.8rem;
        border-radius: 20px;
        box-shadow: var(--shadow1), var(--shadow2);
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *,
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        color: var(--text) !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: var(--text) !important;
        font-weight: 700;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] * {
        color: var(--text) !important;
    }

    span[data-baseweb="tag"] {
        color: white !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--muted) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
        border-bottom-color: var(--teal) !important;
        font-weight: 700;
    }

    .stCaption, small {
        color: var(--muted) !important;
    }

    @media (max-width: 900px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 2.1rem;
        }
        .nav-bar {
            flex-direction: column;
            align-items: flex-start;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def clean_column_name(name):
    name = str(name).strip()
    name = re.sub(r"\s+", " ", name)
    return name if name else "Unnamed"


def make_unique_columns(columns):
    seen = {}
    new_cols = []

    for col in columns:
        base = clean_column_name(col)
        if base in seen:
            seen[base] += 1
            new_cols.append(f"{base}_{seen[base]}")
        else:
            seen[base] = 0
            new_cols.append(base)

    return new_cols


def safe_read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = make_unique_columns(df.columns)
    return df


def generate_sample_data(n=250, seed=42):
    rng = np.random.default_rng(seed)

    genders = rng.choice(["Male", "Female"], size=n, p=[0.56, 0.44])
    education = rng.choice(["Bachelors", "Masters", "PhD"], size=n, p=[0.56, 0.33, 0.11])

    age = rng.normal(29, 6, size=n).round().astype(int)
    age = np.clip(age, 21, 50)

    exp_years = np.clip((age - 21) * rng.uniform(0.2, 0.75, size=n) + rng.normal(2, 1.5, size=n), 0, 25)
    exp_years = np.round(exp_years, 1)

    test_score = np.clip(rng.normal(68, 12, size=n), 35, 98).round(1)
    interview_score = np.clip(
        0.5 * test_score + rng.normal(32, 8, size=n) + np.where(genders == "Male", 2.8, -2.2),
        30, 99
    ).round(1)

    edu_bonus = np.select(
        [education == "Bachelors", education == "Masters", education == "PhD"],
        [0, 4, 7],
        default=0
    )

    composite = 0.4 * test_score + 0.4 * interview_score + 0.8 * exp_years + edu_bonus + np.where(genders == "Male", 3, -3)
    hired = np.where(composite > np.percentile(composite, 55), "Hired", "Rejected")

    df = pd.DataFrame({
        "ApplicantID": [f"A{i:04d}" for i in range(1, n + 1)],
        "Gender": genders,
        "Age": age,
        "Education": education,
        "ExperienceYears": exp_years,
        "TestScore": test_score,
        "InterviewScore": interview_score,
        "Hired": hired
    })

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[20, 25, 30, 35, 40, 60],
        labels=["21-25", "26-30", "31-35", "36-40", "41+"],
        include_lowest=True
    ).astype(str)

    for col, frac in {
        "Age": 0.04,
        "Education": 0.06,
        "ExperienceYears": 0.05,
        "InterviewScore": 0.04
    }.items():
        idx = rng.choice(df.index, size=max(1, int(n * frac)), replace=False)
        df.loc[idx, col] = np.nan

    df.columns = make_unique_columns(df.columns)
    return df


def compute_data_health(df):
    rows, cols = df.shape
    total_points = rows * cols
    missing_values = int(df.isna().sum().sum())
    score = 0 if total_points == 0 else (1 - missing_values / total_points) * 100
    return {
        "rows": rows,
        "cols": cols,
        "missing_values": missing_values,
        "total_points": total_points,
        "score": round(score, 2)
    }


def health_label(score):
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Moderate"
    return "Poor"


def to_binary_selection(series, selected_positive_values):
    selected_set = {str(v).strip().lower() for v in selected_positive_values}
    return series.astype(str).str.strip().str.lower().isin(selected_set).astype(int)


def is_identifier_like(series, col_name, n_rows):
    col_lower = str(col_name).lower()
    blocked_name_tokens = ["id", "applicantid", "candidateid", "employeeid", "uuid", "rollno", "regno"]

    if any(token in col_lower for token in blocked_name_tokens):
        return True

    nunique = series.nunique(dropna=True)
    unique_ratio = nunique / max(n_rows, 1)

    return unique_ratio > 0.5


def get_protected_candidates(df):
    candidates = []
    n_rows = len(df)

    for col in df.columns:
        series = df[col]

        if isinstance(series, pd.DataFrame):
            continue

        nunique = series.nunique(dropna=True)
        dtype_str = str(series.dtype)

        group_like = (nunique >= 2) and (
            nunique <= 20 or dtype_str == "object" or "category" in dtype_str
        )

        if group_like and not is_identifier_like(series, col, n_rows):
            candidates.append(col)

    return candidates


def compute_disparate_impact(df, protected_attr, target_col, positive_values):
    if protected_attr not in df.columns or target_col not in df.columns:
        return None, "Selected columns were not found in the dataset."

    protected_series = df[protected_attr]
    target_series = df[target_col]

    if isinstance(protected_series, pd.DataFrame) or isinstance(target_series, pd.DataFrame):
        return None, "Duplicate column names detected. Please rename repeated columns in the CSV."

    work = pd.DataFrame({
        protected_attr: protected_series,
        target_col: target_series
    }).dropna()

    if work.empty:
        return None, "No valid rows remain after removing missing values in the selected columns."

    if work[protected_attr].nunique(dropna=True) < 2:
        return None, "Choose a protected attribute with at least two groups."

    if len(positive_values) == 0:
        return None, "Select at least one positive outcome value."

    work["selected"] = to_binary_selection(work[target_col], positive_values)

    grouped = (
        work.groupby(protected_attr, dropna=True)
        .agg(
            Total_Count=(target_col, "count"),
            Selected_Count=("selected", "sum")
        )
        .reset_index()
        .rename(columns={protected_attr: "Group"})
    )

    grouped["Selection_Rate"] = grouped["Selected_Count"] / grouped["Total_Count"]

    if grouped.empty:
        return None, "No groups were available for disparity analysis."

    highest_rate = grouped["Selection_Rate"].max()

    if highest_rate == 0:
        return None, "No selected outcomes were found for the chosen positive class."

    grouped["DI_vs_Highest"] = grouped["Selection_Rate"] / highest_rate
    grouped = grouped.sort_values("Selection_Rate", ascending=False).reset_index(drop=True)

    privileged_group = grouped.iloc[0]["Group"]
    privileged_rate = float(grouped.iloc[0]["Selection_Rate"])

    comparison_df = grouped[grouped["Group"] != privileged_group].copy()

    if comparison_df.empty:
        return None, "At least two groups are needed to compute disparate impact."

    unprivileged_row = comparison_df.sort_values("DI_vs_Highest", ascending=True).iloc[0]
    unprivileged_group = unprivileged_row["Group"]
    unprivileged_rate = float(unprivileged_row["Selection_Rate"])
    di_ratio = float(unprivileged_row["DI_vs_Highest"])
    verdict = "PASS" if di_ratio >= 0.8 else "FAIL"

    return {
        "summary": grouped,
        "privileged_group": privileged_group,
        "unprivileged_group": unprivileged_group,
        "privileged_rate": privileged_rate,
        "unprivileged_rate": unprivileged_rate,
        "di_ratio": di_ratio,
        "verdict": verdict
    }, None


def plot_missing_values(df):
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        color="Missing Values",
        color_continuous_scale=["#d7ebe8", "#0c7a7d"],
        title="Missing Values by Column"
    )
    fig.update_layout(
        paper_bgcolor="#f6f1e7",
        plot_bgcolor="#f6f1e7",
        font_color="#1f1f1f",
        height=380
    )
    return fig


def plot_correlation(df):
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr(method="pearson").round(2)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Correlation Heatmap (Pearson r)"
    )
    fig.update_layout(
        paper_bgcolor="#f6f1e7",
        plot_bgcolor="#f6f1e7",
        font_color="#1f1f1f",
        height=480
    )
    return fig


def plot_age_distribution(df):
    if "Age" not in df.columns:
        return None

    age = pd.to_numeric(df["Age"], errors="coerce").dropna()
    if age.empty:
        return None

    fig = px.histogram(
        age,
        x="Age",
        nbins=20,
        marginal="violin",
        opacity=0.9,
        color_discrete_sequence=["#0c7a7d"],
        title="Age Distribution"
    )
    fig.update_layout(
        paper_bgcolor="#f6f1e7",
        plot_bgcolor="#f6f1e7",
        font_color="#1f1f1f",
        height=380
    )
    return fig


def plot_selection_rates(summary_df):
    work = summary_df.copy()
    work["Selection Rate %"] = (work["Selection_Rate"] * 100).round(2)

    fig = px.bar(
        work,
        x="Group",
        y="Selection Rate %",
        text="Selection Rate %",
        color="Selection Rate %",
        color_continuous_scale=["#d7ebe8", "#0c7a7d"],
        title="Selection Rate by Group"
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        paper_bgcolor="#f6f1e7",
        plot_bgcolor="#f6f1e7",
        font_color="#1f1f1f",
        height=390
    )
    return fig


def render_landing():
    st.markdown(
        '<div class="nav-bar"><div class="brand">Data<span>Detox</span></div><div class="muted">Bias Mitigation in AI Hiring</div></div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.25, 0.75])

    with left:
        st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
        st.markdown('<div class="top-badge">Unified Fairness + Data Quality Audit</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Audit hiring datasets before your model learns the wrong patterns.</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-subtitle">DataDetox helps teams inspect completeness, analyze adverse impact using the four-fifths rule, and detect proxy bias through interactive visual diagnostics — all from a simple CSV upload.</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<span class="pill">CSV Upload</span><span class="pill">Completeness Audit</span><span class="pill">Four-Fifths Rule</span><span class="pill">Correlation Heatmap</span>',
            unsafe_allow_html=True
        )

        st.markdown("")
        c1, c2 = st.columns([0.26, 0.74])
        with c1:
            if st.button("Launch App"):
                st.session_state.page = "workspace"
                st.rerun()
        with c2:
            st.markdown(
                '<div class="center-note">Start with demo data or upload your own hiring dataset in the next screen.</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">What users can do</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="inset-card">
            <div class="stat-label">Step 1</div>
            <div class="stat-value" style="font-size:1.1rem;">Upload hiring CSV</div>
            <div class="muted">Bring your applicant, score, and decision data into one view.</div>
        </div>
        <br>
        <div class="inset-card">
            <div class="stat-label">Step 2</div>
            <div class="stat-value" style="font-size:1.1rem;">Run fairness audit</div>
            <div class="muted">Measure data health and compute disparate impact by protected group.</div>
        </div>
        <br>
        <div class="inset-card">
            <div class="stat-label">Step 3</div>
            <div class="stat-value" style="font-size:1.1rem;">Explore visuals</div>
            <div class="muted">Use charts to inspect missingness, age spread, and proxy correlations.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⬆</div>
        <div class="feature-title">Fast CSV onboarding</div>
        <div class="feature-text">Upload local files directly in the browser and begin analysis immediately.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">◎</div>
        <div class="feature-title">Decision fairness check</div>
        <div class="feature-text">Compare group-level selection rates and highlight possible adverse impact.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">▣</div>
        <div class="feature-title">Research-poster ready visuals</div>
        <div class="feature-text">Show health metrics, heatmaps, and distributions in a polished interface.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Team</div>', unsafe_allow_html=True)
    st.write("Vidhi • Chandrima Banerjee • Dayanitha M")
    st.markdown('</div>', unsafe_allow_html=True)


def render_workspace():
    with st.sidebar:
        st.title("DataDetox")
        st.markdown("**A Unified Framework for Bias Mitigation in AI Hiring**")
        st.markdown("---")

        if st.button("← Back to Landing"):
            st.session_state.page = "landing"
            st.rerun()

        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload CSV",
            type=["csv"],
            key="csv_upload",
            help="Upload a hiring dataset in CSV format."
        )

        st.markdown("### Team")
        st.markdown("- Vidhi")
        st.markdown("- Chandrima Banerjee")
        st.markdown("- Dayanitha M")

    st.markdown(
        '<div class="nav-bar"><div class="brand">Data<span>Detox</span> Workspace</div><div class="muted">Audit • Diagnose • Explain</div></div>',
        unsafe_allow_html=True
    )

    if uploaded_file is not None:
        try:
            df = safe_read_csv(uploaded_file)
            st.session_state.uploaded_name = uploaded_file.name
            source = f"Uploaded: {uploaded_file.name}"
        except Exception as e:
            st.error(f"Could not read uploaded CSV: {e}")
            st.stop()
    else:
        df = generate_sample_data()
        source = "Using built-in demo dataset"

    health = compute_data_health(df)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Source", source)
    k2.metric("Rows", health["rows"])
    k3.metric("Columns", health["cols"])
    k4.metric("Health Score", f"{health['score']}%")

    st.progress(
        int(round(max(0, min(100, health["score"])))),
        text=f"Completeness status: {health_label(health['score'])}"
    )

    st.markdown("")
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Upload and Configure</div>', unsafe_allow_html=True)

    protected_candidates = get_protected_candidates(df)
    target_candidates = list(df.columns)

    c1, c2, c3, c4 = st.columns([1, 1, 1.2, 0.8])

    with c1:
        if protected_candidates:
            default_protected = protected_candidates.index("Gender") if "Gender" in protected_candidates else 0
            protected_attr = st.selectbox(
                "Protected Attribute",
                protected_candidates,
                index=default_protected,
                help="Choose a group-based category such as Gender, AgeGroup, or Education. Identifier-like columns are excluded."
            )
        else:
            protected_attr = None
            st.warning("No suitable protected-attribute columns were detected.")

    with c2:
        default_target = target_candidates.index("Hired") if "Hired" in target_candidates else 0
        target_col = st.selectbox("Target Variable", target_candidates, index=default_target)

    unique_values = sorted(df[target_col].dropna().astype(str).str.strip().unique().tolist())
    suggested_defaults = [v for v in ["Hired", "Yes", "Selected", "True", "1", "Pass", "Accepted"] if v in unique_values]

    with c3:
        positive_values = st.multiselect(
            "Positive Outcome Value(s)",
            options=unique_values,
            default=suggested_defaults[:1] if suggested_defaults else []
        )

    with c4:
        st.write("")
        st.write("")
        if st.button("Run Audit"):
            st.session_state.analysis_ready = True

    st.markdown('</div>', unsafe_allow_html=True)

    tabs = st.tabs([
        "Overview",
        "Completeness",
        "Bias Detection",
        "Visual Diagnostics",
        "Download Demo CSV"
    ])

    with tabs[0]:
        left, right = st.columns([1.45, 0.9])

        with left:
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(20), width='stretch')
            st.caption("Duplicate CSV headers are automatically renamed with suffixes like _1, _2 if needed.")
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Formulas Used</div>', unsafe_allow_html=True)
            st.markdown('<div class="formula-box">Completeness score</div>', unsafe_allow_html=True)
            st.latex(r"C = \left(1 - \frac{\text{Missing Values}}{\text{Total Data Points}}\right)\times 100")
            st.markdown('<div class="formula-box">Disparate impact ratio</div>', unsafe_allow_html=True)
            st.latex(r"DI = \frac{R_{\text{group}}}{R_{\text{highest group}}}")
            st.markdown(
                '<p class="muted">If any comparison ratio falls below 0.8, the app flags potential adverse impact under the four-fifths rule.</p>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Completeness Audit</div>', unsafe_allow_html=True)

        a, b, c, d, e = st.columns(5)
        a.metric("Rows", health["rows"])
        b.metric("Columns", health["cols"])
        c.metric("Missing", health["missing_values"])
        d.metric("Data Points", health["total_points"])
        e.metric("Score", f"{health['score']}%")

        if health["score"] >= 90:
            st.markdown(
                '<div class="status-pass">Excellent completeness. The dataset is mostly filled in.</div>',
                unsafe_allow_html=True
            )
        elif health["score"] >= 75:
            st.warning("Moderate completeness. Some missing values may affect interpretation.")
        else:
            st.markdown(
                '<div class="status-fail">Poor completeness. Missing values are substantial and should be reviewed.</div>',
                unsafe_allow_html=True
            )

        st.plotly_chart(plot_missing_values(df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Bias Detection</div>', unsafe_allow_html=True)

        if not st.session_state.analysis_ready:
            st.info("Choose the columns, select the positive outcome, and click Run Audit.")
        elif protected_attr is None:
            st.warning("No suitable protected-attribute column is available for disparity analysis.")
        else:
            if is_identifier_like(df[protected_attr], protected_attr, len(df)):
                st.error(
                    "The selected protected attribute looks like an identifier or near-unique field. "
                    "Please choose a group-based column such as Gender, AgeGroup, or Education."
                )
            else:
                results, error = compute_disparate_impact(df, protected_attr, target_col, positive_values)

                if error:
                    st.warning(error)
                else:
                    r1, r2, r3, r4 = st.columns(4)
                    r1.metric("Privileged Group", str(results["privileged_group"]))
                    r2.metric("Most Disadvantaged Group", str(results["unprivileged_group"]))
                    r3.metric("DI Ratio", f"{results['di_ratio']:.3f}")
                    r4.metric("Verdict", results["verdict"])

                    if results["verdict"] == "PASS":
                        st.markdown(
                            '<div class="status-pass">No immediate adverse-impact flag: all group ratios are at least 0.8 relative to the highest-rate group.</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="status-fail">Warning: Potential adverse impact detected because at least one group falls below the 0.8 threshold.</div>',
                            unsafe_allow_html=True
                        )

                    st.caption(
                        f"The most disadvantaged group has a selection rate equal to {results['di_ratio']:.2%} of the highest-rate group."
                    )

                    display_df = results["summary"].copy()
                    display_df["Selection_Rate"] = (display_df["Selection_Rate"] * 100).round(2).astype(str) + "%"
                    display_df["DI_vs_Highest"] = display_df["DI_vs_Highest"].round(3)
                    st.dataframe(display_df, use_container_width=True)
                    st.plotly_chart(plot_selection_rates(results["summary"]), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Visual Diagnostics</div>', unsafe_allow_html=True)

        corr_fig = plot_correlation(df)
        if corr_fig is not None:
            st.plotly_chart(corr_fig, use_container_width=True)
            st.info("Strong numeric correlations may indicate proxy variables that indirectly reflect protected characteristics.")
        else:
            st.info("Not enough numeric columns are available for the correlation heatmap.")

        age_fig = plot_age_distribution(df)
        if age_fig is not None:
            st.plotly_chart(age_fig, use_container_width=True)
        else:
            st.info("No usable Age column was found.")

        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Download Demo CSV</div>', unsafe_allow_html=True)

        csv_buffer = io.StringIO()
        generate_sample_data().to_csv(csv_buffer, index=False)

        st.download_button(
            label="Download sample_hiring_data.csv",
            data=csv_buffer.getvalue(),
            file_name="sample_hiring_data.csv",
            mime="text/csv"
        )
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    init_state()
    inject_css()

    if st.session_state.page == "landing":
        render_landing()
    else:
        render_workspace()


if __name__ == "__main__":
    main()