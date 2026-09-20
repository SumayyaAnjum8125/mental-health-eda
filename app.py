import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mental Health in Tech | 2014 Survey",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL COLOR PALETTE
# ============================================================

COLORS = {
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "success": "#059669",
    "danger": "#DC2626",
    "warning": "#D97706",
    "info": "#0891B2",
    "pink": "#DB2777",

    "dark": "#1E293B",
    "text": "#334155",
    "gray": "#64748B",
    "light": "#F8FAFC",
    "border": "#E2E8F0",
    "white": "#FFFFFF"
}


# ============================================================
# MATPLOTLIB PROFESSIONAL STYLE
# ============================================================

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.labelcolor": COLORS["text"],
    "xtick.color": COLORS["text"],
    "ytick.color": COLORS["text"],
    "text.color": COLORS["text"],
    "axes.edgecolor": "#CBD5E1",
    "axes.facecolor": "#FFFFFF",
    "figure.facecolor": "#FFFFFF",
    "grid.color": "#E2E8F0",
    "grid.alpha": 0.7
})

sns.set_style("whitegrid")


# ============================================================
# CUSTOM STREAMLIT CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application background */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    /* Main content text */
    .main {
        color: #1E293B;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] * {
        color: #1E293B !important;
    }

    /* Sidebar headings */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1E293B !important;
    }

    /* Normal headings */
    h1, h2, h3, h4 {
        color: #1E293B !important;
    }

    /* Paragraph text */
    p, label, span {
        color: #334155;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
    }

    /* Multiselect */
    div[data-baseweb="select"] span {
        color: #1E293B !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 14px;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1E293B !important;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2563EB;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #059669;
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Info boxes */
    div[data-testid="stAlert"] {
        color: #1E293B;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }

    /* Horizontal line */
    hr {
        border-color: #E2E8F0;
    }

    /* Custom title */
    .dashboard-title {
        font-size: 36px;
        font-weight: 800;
        color: #1E293B !important;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #64748B !important;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #1E293B !important;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .info-card {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 15px;
        border-radius: 8px;
        color: #1E293B !important;
        margin: 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    # Support both filenames
    if os.path.exists("mental_health_survey.csv"):
        file_name = "mental_health_survey.csv"

    elif os.path.exists("survey.csv"):
        file_name = "survey.csv"

    else:
        st.error(
            "CSV file not found. Please keep survey.csv or "
            "mental_health_survey.csv in the same folder as app.py."
        )
        st.stop()

    df = pd.read_csv(file_name)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Timestamp
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

    # Age cleaning
    if "Age" in df.columns:

        df["Age"] = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

        df.loc[
            (df["Age"] < 18) |
            (df["Age"] > 100),
            "Age"
        ] = np.nan

        df["age_group"] = pd.cut(
            df["Age"],
            bins=[17, 25, 35, 45, 55, 100],
            labels=[
                "18–25",
                "26–35",
                "36–45",
                "46–55",
                "56+"
            ]
        )

    # Clean text columns
    for col in df.select_dtypes(
        include="object"
    ).columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
        )

        df[col] = df[col].replace(
            ["nan", "NaN", "None"],
            np.nan
        )

    return df


df = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def percentage(series, value="Yes"):

    valid = series.dropna()

    if len(valid) == 0:
        return 0

    return (
        (valid == value).mean()
        * 100
    )


def make_chart():

    fig, ax = plt.subplots(
        figsize=(10, 5.2),
        dpi=110
    )

    fig.patch.set_facecolor(
        COLORS["white"]
    )

    ax.set_facecolor(
        COLORS["white"]
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color(
        "#CBD5E1"
    )

    ax.spines["bottom"].set_color(
        "#CBD5E1"
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.35
    )

    return fig, ax


def format_chart(
    ax,
    title,
    xlabel="",
    ylabel=""
):

    ax.set_title(
        title,
        fontsize=15,
        fontweight="bold",
        color=COLORS["dark"],
        pad=15
    )

    ax.set_xlabel(
        xlabel,
        fontsize=10,
        color=COLORS["text"],
        labelpad=8
    )

    ax.set_ylabel(
        ylabel,
        fontsize=10,
        color=COLORS["text"],
        labelpad=8
    )

    ax.tick_params(
        axis="both",
        labelsize=9,
        colors=COLORS["text"]
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()


# ============================================================
# SIDEBAR HEADER
# ============================================================

st.sidebar.markdown(
    """
    <div style="text-align:center;">
        <div style="font-size:42px;">🧠</div>
        <h2 style="margin-bottom:0px;">
            Mental Health
        </h2>
        <p style="color:#64748B;">
            Tech Workplace Survey
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "📍 NAVIGATION",
    [
        "📊 Dashboard",
        "👥 Demographics",
        "❤️ Mental Health",
        "🏢 Workplace Support",
        "💼 Workplace Culture",
        "🏭 Company Analysis",
        "🌍 Geography",
        "📈 Advanced Analysis",
        "🎯 Insights"
    ]
)


# ============================================================
# FILTERS
# ============================================================

st.sidebar.markdown(
    "### 🎛️ FILTERS"
)

selected_country = st.sidebar.multiselect(
    "🌍 Country",
    sorted(
        df["Country"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    sorted(
        df["Gender"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_remote = st.sidebar.multiselect(
    "🏠 Remote Work",
    sorted(
        df["remote_work"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_size = st.sidebar.multiselect(
    "🏢 Company Size",
    sorted(
        df["no_employees"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_treatment = st.sidebar.multiselect(
    "❤️ Treatment",
    sorted(
        df["treatment"]
        .dropna()
        .unique()
        .tolist()
    )
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_country:

    filtered_df = filtered_df[
        filtered_df["Country"].isin(
            selected_country
        )
    ]

if selected_gender:

    filtered_df = filtered_df[
        filtered_df["Gender"].isin(
            selected_gender
        )
    ]

if selected_remote:

    filtered_df = filtered_df[
        filtered_df["remote_work"].isin(
            selected_remote
        )
    ]

if selected_size:

    filtered_df = filtered_df[
        filtered_df["no_employees"].isin(
            selected_size
        )
    ]

if selected_treatment:

    filtered_df = filtered_df[
        filtered_df["treatment"].isin(
            selected_treatment
        )
    ]


# Reset button
if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):

    st.rerun()


st.sidebar.markdown("---")

st.sidebar.info(
    f"Showing **{len(filtered_df):,}** "
    f"of **{len(df):,}** respondents."
)


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="dashboard-title">'
        '🧠 Mental Health in Tech'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        '2014 Mental Health in Technology Workplace Survey'
        '</div>',
        unsafe_allow_html=True
    )

    # KPI values
    respondents = len(filtered_df)

    treatment_rate = percentage(
        filtered_df["treatment"]
    )

    family_rate = percentage(
        filtered_df["family_history"]
    )

    benefits_rate = percentage(
        filtered_df["benefits"]
    )

    remote_rate = percentage(
        filtered_df["remote_work"]
    )

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Respondents",
            f"{respondents:,}"
        )

    with col2:

        st.metric(
            "❤️ Treatment",
            f"{treatment_rate:.1f}%"
        )

    with col3:

        st.metric(
            "🧬 Family History",
            f"{family_rate:.1f}%"
        )

    with col4:

        st.metric(
            "🏠 Remote Work",
            f"{remote_rate:.1f}%"
        )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        '📊 Key Visualizations'
        '</div>',
        unsafe_allow_html=True
    )

    # Toggle controls
    col1, col2 = st.columns(2)

    with col1:

        show_family = st.toggle(
            "❤️ Treatment vs Family History",
            value=True
        )

    with col2:

        show_gender = st.toggle(
            "👤 Treatment by Gender",
            value=True
        )

    # Family history chart
    if show_family:

        data = pd.crosstab(
            filtered_df["family_history"],
            filtered_df["treatment"]
        )

        fig, ax = make_chart()

        data.plot(
            kind="bar",
            ax=ax,
            color=[
                COLORS["danger"],
                COLORS["success"]
            ],
            width=0.65
        )

        format_chart(
            ax,
            "Treatment Status by Family History",
            "Family History",
            "Number of Respondents"
        )

        ax.legend(
            title="Treatment",
            frameon=False
        )

        plt.xticks(
            rotation=0
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    # Gender chart
    if show_gender:

        gender_data = (
            filtered_df
            .groupby("Gender")["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
            .sort_values(
                ascending=False
            )
        )

        fig, ax = make_chart()

        gender_data.plot(
            kind="bar",
            ax=ax,
            color=COLORS["primary"],
            width=0.65
        )

        format_chart(
            ax,
            "Treatment Rate by Gender",
            "Gender",
            "Treatment Rate (%)"
        )

        plt.xticks(
            rotation=30,
            ha="right"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# PAGE 2 — DEMOGRAPHICS
# ============================================================

elif page == "👥 Demographics":

    st.title("👥 Demographics")

    col1, col2 = st.columns(2)

    with col1:

        show_age = st.toggle(
            "📊 Age Distribution",
            value=True
        )

    with col2:

        show_gender = st.toggle(
            "👤 Gender Distribution",
            value=True
        )

    if show_age:

        fig, ax = make_chart()

        ax.hist(
            filtered_df["Age"].dropna(),
            bins=15,
            color=COLORS["primary"],
            edgecolor="white",
            alpha=0.85
        )

        format_chart(
            ax,
            "Age Distribution",
            "Age",
            "Number of Respondents"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    if show_gender:

        gender_counts = (
            filtered_df["Gender"]
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5.5),
            dpi=110
        )

        gender_counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["secondary"],
            width=0.65
        )

        format_chart(
            ax,
            "Gender Distribution",
            "Gender",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=30,
            ha="right"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# PAGE 3 — MENTAL HEALTH
# ============================================================

elif page == "❤️ Mental Health":

    st.title("❤️ Mental Health Analysis")

    col1, col2 = st.columns(2)

    with col1:

        show_treatment = st.toggle(
            "❤️ Treatment Status",
            value=True
        )

    with col2:

        show_interference = st.toggle(
            "💼 Work Interference",
            value=True
        )

    if show_treatment:

        counts = (
            filtered_df["treatment"]
            .value_counts()
        )

        fig, ax = make_chart()

        counts.plot(
            kind="bar",
            ax=ax,
            color=[
                COLORS["success"],
                COLORS["danger"]
            ],
            width=0.65
        )

        format_chart(
            ax,
            "Mental Health Treatment Status",
            "Treatment",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=0
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    if show_interference:

        counts = (
            filtered_df["work_interfere"]
            .value_counts()
        )

        fig, ax = make_chart()

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["secondary"],
            width=0.65
        )

        format_chart(
            ax,
            "Mental Health Work Interference",
            "Work Interference",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=25,
            ha="right"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# PAGE 4 — WORKPLACE SUPPORT
# ============================================================

elif page == "🏢 Workplace Support":

    st.title("🏢 Employer Mental Health Support")

    support_columns = [
        "benefits",
        "care_options",
        "wellness_program",
        "seek_help",
        "anonymity"
    ]

    selected_support = st.multiselect(
        "Select support factors",
        support_columns,
        default=support_columns
    )

    if selected_support:

        support_rates = {}

        for col in selected_support:

            support_rates[
                col.replace(
                    "_", " "
                ).title()
            ] = percentage(
                filtered_df[col]
            )

        support_data = (
            pd.Series(
                support_rates
            )
            .sort_values(
                ascending=True
            )
        )

        fig, ax = make_chart()

        support_data.plot(
            kind="barh",
            ax=ax,
            color=COLORS["info"],
            width=0.65
        )

        format_chart(
            ax,
            "Workplace Mental Health Support",
            "Percentage",
            ""
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# PAGE 5 — WORKPLACE CULTURE
# ============================================================

elif page == "💼 Workplace Culture":

    st.title("💼 Workplace Culture")

    col1, col2 = st.columns(2)

    with col1:

        show_coworkers = st.toggle(
            "👥 Coworker Support",
            value=True
        )

    with col2:

        show_supervisor = st.toggle(
            "👨‍💼 Supervisor Support",
            value=True
        )

    if show_coworkers:

        counts = (
            filtered_df["coworkers"]
            .value_counts()
        )

        fig, ax = make_chart()

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["primary"],
            width=0.65
        )

        format_chart(
            ax,
            "Coworker Support",
            "Response",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=0
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    if show_supervisor:

        counts = (
            filtered_df["supervisor"]
            .value_counts()
        )

        fig, ax = make_chart()

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["secondary"],
            width=0.65
        )

        format_chart(
            ax,
            "Supervisor Support",
            "Response",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=0
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# PAGE 6 — COMPANY ANALYSIS
# ============================================================

elif page == "🏭 Company Analysis":

    st.title("🏭 Company Analysis")

    col1, col2 = st.columns(2)

    with col1:

        show_size = st.toggle(
            "🏢 Company Size",
            value=True
        )

    with col2:

        show_tech = st.toggle(
            "💻 Tech vs Non-Tech",
            value=True
        )

    if show_size:

        counts = (
            filtered_df["no_employees"]
            .value_counts()
        )

        fig, ax = make_chart()

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["primary"],
            width=0.65
        )

        format_chart(
            ax,
            "Company Size Distribution",
            "Number of Employees",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=25,
            ha="right"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    if show_tech:

        counts = (
            filtered_df["tech_company"]
            .value_counts()
        )

        fig, ax = make_chart()

        counts.plot(
            kind="bar",
            ax=ax,
            color=[
                COLORS["primary"],
                COLORS["pink"]
            ],
            width=0.65
        )

        format_chart(
            ax,
            "Technology Company Status",
            "Company Type",
            "Number of Respondents"
        )

        plt.xticks(
            rotation=0
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# PAGE 7 — GEOGRAPHY
# ============================================================

elif page == "🌍 Geography":

    st.title("🌍 Geographic Analysis")

    country_data = (
        filtered_df
        .groupby("Country")
        .agg(
            Respondents=(
                "treatment",
                "size"
            ),
            Treatment_Rate=(
                "treatment",
                lambda x:
                percentage(x)
            )
        )
        .query(
            "Respondents >= 10"
        )
        .sort_values(
            "Treatment_Rate",
            ascending=False
        )
    )

    if len(country_data) > 0:

        max_countries = min(
            20,
            len(country_data)
        )

        top_n = st.slider(
            "Number of countries",
            min_value=5,
            max_value=max_countries,
            value=min(
                10,
                max_countries
            )
        )

        selected_countries = (
            country_data
            .head(top_n)
            .sort_values(
                "Treatment_Rate"
            )
        )

        fig, ax = make_chart()

        selected_countries[
            "Treatment_Rate"
        ].plot(
            kind="barh",
            ax=ax,
            color=COLORS["secondary"],
            width=0.65
        )

        format_chart(
            ax,
            "Treatment Rate by Country",
            "Treatment Rate (%)",
            "Country"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

        st.subheader(
            "Country Summary"
        )

        st.dataframe(
            country_data.round(2),
            use_container_width=True
        )

    else:

        st.warning(
            "Not enough data for geographic analysis."
        )


# ============================================================
# PAGE 8 — ADVANCED ANALYSIS
# ============================================================

elif page == "📈 Advanced Analysis":

    st.title("📈 Advanced Analysis")

    option = st.selectbox(
        "Choose Analysis",
        [
            "Treatment by Gender",
            "Treatment by Age Group",
            "Treatment by Remote Work",
            "Treatment by Company Size",
            "Treatment by Tech Company",
            "Treatment by Family History"
        ]
    )

    if option == "Treatment by Gender":

        data = (
            filtered_df
            .groupby("Gender")["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
            .sort_values(
                ascending=False
            )
        )

        xlabel = "Gender"

    elif option == "Treatment by Age Group":

        data = (
            filtered_df
            .groupby(
                "age_group",
                observed=False
            )["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
        )

        xlabel = "Age Group"

    elif option == "Treatment by Remote Work":

        data = (
            filtered_df
            .groupby(
                "remote_work"
            )["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
        )

        xlabel = "Remote Work"

    elif option == "Treatment by Company Size":

        data = (
            filtered_df
            .groupby(
                "no_employees"
            )["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
        )

        xlabel = "Company Size"

    elif option == "Treatment by Tech Company":

        data = (
            filtered_df
            .groupby(
                "tech_company"
            )["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
        )

        xlabel = "Company Type"

    else:

        data = (
            filtered_df
            .groupby(
                "family_history"
            )["treatment"]
            .apply(
                lambda x:
                percentage(x)
            )
        )

        xlabel = "Family History"

    fig, ax = make_chart()

    data.plot(
        kind="bar",
        ax=ax,
        color=COLORS["primary"],
        width=0.65
    )

    format_chart(
        ax,
        f"Treatment Rate by {xlabel}",
        xlabel,
        "Treatment Rate (%)"
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

    st.subheader(
        "📋 Analysis Values"
    )

    st.dataframe(
        data.round(2)
        .rename(
            "Treatment Rate (%)"
        )
        .to_frame(),
        use_container_width=True
    )


# ============================================================
# PAGE 9 — INSIGHTS
# ============================================================

elif page == "🎯 Insights":

    st.title("🎯 Key Insights")

    treatment_pct = percentage(
        filtered_df["treatment"]
    )

    family_pct = percentage(
        filtered_df["family_history"]
    )

    remote_pct = percentage(
        filtered_df["remote_work"]
    )

    benefits_pct = percentage(
        filtered_df["benefits"]
    )

    st.markdown(
        f"""
        <div class="info-card">
        <b>Current filtered dataset:</b>
        {len(filtered_df):,} respondents
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "❤️ Treatment",
            f"{treatment_pct:.1f}%"
        )

    with col2:

        st.metric(
            "🧬 Family History",
            f"{family_pct:.1f}%"
        )

    with col3:

        st.metric(
            "🏠 Remote Work",
            f"{remote_pct:.1f}%"
        )

    with col4:

        st.metric(
            "🏢 Benefits",
            f"{benefits_pct:.1f}%"
        )

    st.markdown("---")

    st.subheader(
        "📌 Data-Based Observations"
    )

    st.write(
        f"""
        • The current filtered dataset contains
        **{len(filtered_df):,} respondents**.

        • **{treatment_pct:.1f}%** of respondents reported
        receiving treatment.

        • **{family_pct:.1f}%** reported a family history
        of mental health conditions.

        • **{remote_pct:.1f}%** reported working remotely.

        • **{benefits_pct:.1f}%** reported that mental health
        benefits were available.
        """
    )

    st.info(
        "These are descriptive observations from the survey "
        "data and do not establish causation."
    )


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 📥 EXPORT"
)

csv_data = (
    filtered_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.sidebar.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_mental_health_data.csv",
    mime="text/csv",
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748B;
        font-size:13px;
        padding:10px;
    ">
        🧠 Mental Health in Tech Survey • 2014
        <br>
        Exploratory Data Analysis Dashboard
    </div>
    """,
    unsafe_allow_html=True
)