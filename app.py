import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

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
# CUSTOM COLORS
# ============================================================

COLORS = {
    "primary": "#4F46E5",
    "secondary": "#7C3AED",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#06B6D4",
    "pink": "#EC4899",
    "dark": "#1E293B",
    "text": "#334155",
    "light": "#F8FAFC",
    "white": "#FFFFFF",
    "gray": "#64748B"
}

sns.set_style("whitegrid")


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #EEF2FF 0%,
            #F8FAFC 100%
        );
    }

    h1 {
        color: #1E293B;
        font-weight: 700;
    }

    h2, h3 {
        color: #334155;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #64748B;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #334155;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
    }

    .info-box {
        background-color: #EEF2FF;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #4F46E5;
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

    df = pd.read_csv("mental_health_survey.csv")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Convert timestamp
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

    # Clean Age
    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    # Keep realistic ages
    df.loc[
        (df["Age"] < 18) | (df["Age"] > 100),
        "Age"
    ] = np.nan

    # Age groups
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
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h2 style="text-align:center;">🧠 Mental Health</h2>
    <p style="text-align:center;color:#64748B;">
    Tech Workplace Survey
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# ============================================================
# PAGE NAVIGATION
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

st.sidebar.markdown("### 🎛️ Filters")

country_options = sorted(
    df["Country"].dropna().unique().tolist()
)

gender_options = sorted(
    df["Gender"].dropna().unique().tolist()
)

remote_options = sorted(
    df["remote_work"].dropna().unique().tolist()
)

employee_options = sorted(
    df["no_employees"].dropna().unique().tolist()
)

selected_country = st.sidebar.multiselect(
    "🌍 Country",
    country_options,
    default=[]
)

selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    gender_options,
    default=[]
)

selected_remote = st.sidebar.multiselect(
    "🏠 Remote Work",
    remote_options,
    default=[]
)

selected_size = st.sidebar.multiselect(
    "🏢 Company Size",
    employee_options,
    default=[]
)

selected_treatment = st.sidebar.multiselect(
    "❤️ Treatment",
    sorted(df["treatment"].dropna().unique()),
    default=[]
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_country:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_country)
    ]

if selected_gender:
    filtered_df = filtered_df[
        filtered_df["Gender"].isin(selected_gender)
    ]

if selected_remote:
    filtered_df = filtered_df[
        filtered_df["remote_work"].isin(selected_remote)
    ]

if selected_size:
    filtered_df = filtered_df[
        filtered_df["no_employees"].isin(selected_size)
    ]

if selected_treatment:
    filtered_df = filtered_df[
        filtered_df["treatment"].isin(selected_treatment)
    ]


# Reset button
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()


st.sidebar.markdown("---")

st.sidebar.info(
    f"Showing **{len(filtered_df):,}** respondents "
    f"out of **{len(df):,}** total respondents."
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def percentage(series, value="Yes"):

    valid = series.dropna()

    if len(valid) == 0:
        return 0

    return (valid == value).mean() * 100


def style_chart(ax, title, xlabel="", ylabel=""):

    ax.set_title(
        title,
        fontsize=17,
        fontweight="bold",
        color=COLORS["dark"],
        pad=15
    )

    ax.set_xlabel(
        xlabel,
        fontsize=11,
        color=COLORS["text"]
    )

    ax.set_ylabel(
        ylabel,
        fontsize=11,
        color=COLORS["text"]
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="main-title">🧠 Mental Health in Tech</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">2014 Mental Health in Technology Workplace Survey</div>',
        unsafe_allow_html=True
    )

    # KPI calculations
    respondents = len(filtered_df)

    treatment_rate = percentage(
        filtered_df["treatment"]
    )

    family_rate = percentage(
        filtered_df["family_history"]
    )

    remote_rate = percentage(
        filtered_df["remote_work"]
    )

    benefits_rate = percentage(
        filtered_df["benefits"]
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

    # Dashboard controls
    st.markdown(
        '<div class="section-title">📊 Dashboard Visualizations</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        show_treatment = st.toggle(
            "❤️ Treatment vs Family History",
            value=True
        )

    with col2:

        show_gender = st.toggle(
            "👤 Treatment by Gender",
            value=True
        )

    # Treatment vs family history
    if show_treatment:

        crosstab = pd.crosstab(
            filtered_df["family_history"],
            filtered_df["treatment"]
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        crosstab.plot(
            kind="bar",
            ax=ax,
            color=[
                COLORS["danger"],
                COLORS["success"]
            ],
            edgecolor="white"
        )

        style_chart(
            ax,
            "Treatment Seeking by Family History",
            "Family History",
            "Number of Respondents"
        )

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)

    # Treatment by gender
    if show_gender:

        gender_rate = (
            filtered_df
            .groupby("Gender")["treatment"]
            .apply(lambda x: percentage(x))
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        gender_rate.plot(
            kind="bar",
            ax=ax,
            color=COLORS["primary"]
        )

        style_chart(
            ax,
            "Treatment Rate by Gender",
            "Gender",
            "Treatment Rate (%)"
        )

        plt.xticks(rotation=30, ha="right")

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# DEMOGRAPHICS
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

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.hist(
            filtered_df["Age"].dropna(),
            bins=15,
            color=COLORS["primary"],
            edgecolor="white",
            alpha=0.85
        )

        style_chart(
            ax,
            "Age Distribution",
            "Age",
            "Number of Respondents"
        )

        st.pyplot(fig)

        plt.close(fig)

    if show_gender:

        gender_counts = filtered_df["Gender"].value_counts()

        fig, ax = plt.subplots(figsize=(9, 6))

        ax.pie(
            gender_counts.values,
            labels=gender_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Gender Distribution",
            fontsize=17,
            fontweight="bold"
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# MENTAL HEALTH
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

        counts = filtered_df[
            "treatment"
        ].value_counts()

        fig, ax = plt.subplots(figsize=(9, 5))

        counts.plot(
            kind="bar",
            ax=ax,
            color=[
                COLORS["success"],
                COLORS["danger"]
            ]
        )

        style_chart(
            ax,
            "Mental Health Treatment Status",
            "Treatment",
            "Number of Respondents"
        )

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)

    if show_interference:

        counts = filtered_df[
            "work_interfere"
        ].value_counts()

        fig, ax = plt.subplots(figsize=(9, 5))

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["secondary"]
        )

        style_chart(
            ax,
            "Mental Health Work Interference",
            "Work Interference",
            "Number of Respondents"
        )

        plt.xticks(rotation=30, ha="right")

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# WORKPLACE SUPPORT
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
                col.replace("_", " ").title()
            ] = percentage(
                filtered_df[col]
            )

        support_df = pd.Series(
            support_rates
        ).sort_values(
            ascending=True
        )

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        support_df.plot(
            kind="barh",
            ax=ax,
            color=COLORS["info"]
        )

        style_chart(
            ax,
            "Workplace Mental Health Support",
            "",
            "Yes Response (%)"
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# WORKPLACE CULTURE
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

        counts = filtered_df[
            "coworkers"
        ].value_counts()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["primary"]
        )

        style_chart(
            ax,
            "Coworker Support",
            "Response",
            "Respondents"
        )

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)

    if show_supervisor:

        counts = filtered_df[
            "supervisor"
        ].value_counts()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["secondary"]
        )

        style_chart(
            ax,
            "Supervisor Support",
            "Response",
            "Respondents"
        )

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# COMPANY ANALYSIS
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

        counts = filtered_df[
            "no_employees"
        ].value_counts()

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        counts.plot(
            kind="bar",
            ax=ax,
            color=COLORS["primary"]
        )

        style_chart(
            ax,
            "Company Size Distribution",
            "Number of Employees",
            "Respondents"
        )

        plt.xticks(rotation=30)

        st.pyplot(fig)

        plt.close(fig)

    if show_tech:

        counts = filtered_df[
            "tech_company"
        ].value_counts()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        counts.plot(
            kind="bar",
            ax=ax,
            color=[
                COLORS["primary"],
                COLORS["pink"]
            ]
        )

        style_chart(
            ax,
            "Tech Company vs Non-Tech Company",
            "Company Type",
            "Respondents"
        )

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# GEOGRAPHY
# ============================================================

elif page == "🌍 Geography":

    st.title("🌍 Geographic Analysis")

    country_data = (
        filtered_df
        .groupby("Country")
        .agg(
            Respondents=("treatment", "size"),
            Treatment_Rate=(
                "treatment",
                lambda x: percentage(x)
            )
        )
        .query("Respondents >= 10")
        .sort_values(
            "Treatment_Rate",
            ascending=False
        )
    )

    if len(country_data) > 0:

        top_n = st.slider(
            "Number of countries to display",
            min_value=5,
            max_value=min(20, len(country_data)),
            value=min(10, len(country_data))
        )

        selected_countries = country_data.head(
            top_n
        )

        fig, ax = plt.subplots(
            figsize=(11, 6)
        )

        selected_countries[
            "Treatment_Rate"
        ].sort_values().plot(
            kind="barh",
            ax=ax,
            color=COLORS["secondary"]
        )

        style_chart(
            ax,
            "Treatment Rate by Country",
            "Treatment Rate (%)",
            "Country"
        )

        st.pyplot(fig)

        plt.close(fig)

        st.dataframe(
            country_data.round(2),
            use_container_width=True
        )

    else:

        st.warning(
            "Not enough data for geographic analysis."
        )


# ============================================================
# ADVANCED ANALYSIS
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
            .apply(lambda x: percentage(x))
            .sort_values(ascending=False)
        )

        xlabel = "Gender"

    elif option == "Treatment by Age Group":

        data = (
            filtered_df
            .groupby(
                "age_group",
                observed=False
            )["treatment"]
            .apply(lambda x: percentage(x))
        )

        xlabel = "Age Group"

    elif option == "Treatment by Remote Work":

        data = (
            filtered_df
            .groupby("remote_work")["treatment"]
            .apply(lambda x: percentage(x))
        )

        xlabel = "Remote Work"

    elif option == "Treatment by Company Size":

        data = (
            filtered_df
            .groupby("no_employees")["treatment"]
            .apply(lambda x: percentage(x))
        )

        xlabel = "Company Size"

    elif option == "Treatment by Tech Company":

        data = (
            filtered_df
            .groupby("tech_company")["treatment"]
            .apply(lambda x: percentage(x))
        )

        xlabel = "Company Type"

    else:

        data = (
            filtered_df
            .groupby("family_history")["treatment"]
            .apply(lambda x: percentage(x))
        )

        xlabel = "Family History"

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    data.plot(
        kind="bar",
        ax=ax,
        color=COLORS["primary"]
    )

    style_chart(
        ax,
        f"Treatment Rate by {xlabel}",
        xlabel,
        "Treatment Rate (%)"
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    st.pyplot(fig)

    plt.close(fig)

    # Show values
    st.dataframe(
        data.round(2).rename(
            "Treatment Rate (%)"
        ).to_frame(),
        use_container_width=True
    )


# ============================================================
# INSIGHTS
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
        """
        <div class="info-box">
        <b>How to use this page:</b><br>
        The values below are calculated from the currently
        selected filters. Use them as descriptive findings
        from the survey data.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "❤️ Treatment Rate",
            f"{treatment_pct:.1f}%"
        )

        st.metric(
            "🧬 Family History",
            f"{family_pct:.1f}%"
        )

    with col2:

        st.metric(
            "🏠 Remote Work",
            f"{remote_pct:.1f}%"
        )

        st.metric(
            "🏢 Benefits: Yes",
            f"{benefits_pct:.1f}%"
        )

    st.markdown("---")

    st.subheader("📌 Data-Based Observations")

    st.write(
        f"""
        • The filtered dataset contains **{len(filtered_df):,} respondents**.

        • **{treatment_pct:.1f}%** of respondents reported treatment.

        • **{family_pct:.1f}%** reported having a family history of mental health conditions.

        • **{remote_pct:.1f}%** reported working remotely.

        • **{benefits_pct:.1f}%** reported that mental health benefits were available.
        """
    )

    st.info(
        "These observations describe patterns in the survey data. "
        "They should not be interpreted as proof of causation."
    )


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📥 Export")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.sidebar.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_mental_health_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#64748B;padding:10px;">
    🧠 Mental Health in Tech Survey • 2014 • Exploratory Data Analysis
    </div>
    """,
    unsafe_allow_html=True
)