import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Mental Health in Tech - Professional Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'danger': '#D62828',
    'warning': '#F77F00',
    'light': '#F0F2F6',
    'dark': '#1F1F1F'
}

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('mental_health_survey.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['age_group'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 100],
                             labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    return df

df = load_data()

# Sidebar
st.sidebar.markdown("# 🧠 Mental Health in Tech")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📍 SELECT PAGE",
    ["📊 Dashboard","👥 Demographics","❤️ Mental Health","🏢 Support",
     "💼 Culture","🏭 Company","📈 Analysis","🎯 Insights"]
)

# Filters
selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(df['Country'].unique().tolist()))
selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(df['Gender'].unique().tolist()))
selected_size = st.sidebar.selectbox("Select Company Size", ["All","1-5","6-25","26-100","100-500","500-1000","1000+"])

filtered_df = df.copy()
if selected_country != "All": filtered_df = filtered_df[filtered_df['Country'] == selected_country]
if selected_gender != "All": filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
if selected_size != "All": filtered_df = filtered_df[filtered_df['no_employees'] == selected_size]

# ============================================================================ #
# DASHBOARD PAGE
# ============================================================================ #
if page == "📊 Dashboard":
    st.title("🧠 Mental Health in Tech Survey")
    st.markdown("**Professional Analysis Dashboard | 2014 Survey Data**")

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Respondents", f"{len(filtered_df):,}")
    with col2: st.metric("Countries", f"{filtered_df['Country'].nunique()}")
    with col3: st.metric("Average Age", f"{filtered_df['Age'].mean():.1f}")
    with col4: st.metric("Remote Workers", f"{(filtered_df['remote_work'] == 'Yes').sum()}")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Sought Treatment", f"{(filtered_df['treatment'] == 'Yes').sum()} people")
    with col2: st.metric("Family History", f"{(filtered_df['family_history'] == 'Yes').sum()} people")
    with col3: st.metric("Has Benefits", f"{(filtered_df['benefits'] == 'Yes').sum()} people")

# ============================================================================ #
# DEMOGRAPHICS PAGE
# ============================================================================ #
elif page == "👥 Demographics":
    st.title("👥 Demographic Analysis")
    st.write("Age, Gender, and Country distributions with charts and stats.")

# ============================================================================ #
# MENTAL HEALTH PAGE
# ============================================================================ #
elif page == "❤️ Mental Health":
    st.title("❤️ Mental Health Metrics")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Treatment Yes", f"{(filtered_df['treatment'] == 'Yes').sum()}")
    with col2: st.metric("Family History Yes", f"{(filtered_df['family_history'] == 'Yes').sum()}")
    with col3: st.metric("Work Interference (Sometimes/Often)", f"{(filtered_df['work_interfere'].isin(['Sometimes','Often'])).sum()}")
    col1, col2 = st.columns(2)
    with col1: st.metric("Fear Consequences Yes", f"{(filtered_df['mental_health_consequence'] == 'Yes').sum()}")
    with col2: st.metric("Remote Workers", f"{(filtered_df['remote_work'] == 'Yes').sum()}")

# ============================================================================ #
# SUPPORT PAGE
# ============================================================================ #
elif page == "🏢 Support":
    st.title("🏢 Employer Support Metrics")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Benefits Yes", f"{(filtered_df['benefits'] == 'Yes').sum()}")
    with col2: st.metric("Care Options Yes", f"{(filtered_df['care_options'] == 'Yes').sum()}")
    with col3: st.metric("Wellness Program Yes", f"{(filtered_df['wellness_program'] == 'Yes').sum()}")
    col1, col2 = st.columns(2)
    with col1: st.metric("Seek Help Resources Yes", f"{(filtered_df['seek_help'] == 'Yes').sum()}")
    with col2: st.metric("Anonymity Protected Yes", f"{(filtered_df['anonymity'] == 'Yes').sum()}")

# ============================================================================ #
# CULTURE PAGE
# ============================================================================ #
elif page == "💼 Culture":
    st.title("💼 Workplace Culture Metrics")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Discuss with Coworkers Yes", f"{(filtered_df['coworkers'] == 'Yes').sum()}")
    with col2: st.metric("Discuss with Supervisor Yes", f"{(filtered_df['supervisor'] == 'Yes').sum()}")
    with col3: st.metric("Fear Consequences Yes", f"{(filtered_df['mental_health_consequence'] == 'Yes').sum()}")

# ============================================================================ #
# COMPANY PAGE
# ============================================================================ #
elif page == "🏭 Company":
    st.title("🏭 Company Metrics")
    col1, col2 = st.columns(2)
    with col1: st.metric("Tech Companies", f"{(filtered_df['tech_company'] == 'Yes').sum()}")
    with col2: st.metric("Non-Tech Companies", f"{(filtered_df['tech_company'] == 'No').sum()}")
    st.metric("Company Size Categories", f"{filtered_df['no_employees'].nunique()} sizes")

# ============================================================================ #
# ANALYSIS PAGE
# ============================================================================ #
elif page == "📈 Analysis":
    st.title("📈 Cross-Analysis Metrics")
    st.write("Here you can add crosstab charts or metrics comparing treatment vs family history, gender, company size, etc.")
    st.metric("Treatment vs Family History (Yes/Yes)", f"{len(filtered_df[(filtered_df['family_history']=='Yes') & (filtered_df['treatment']=='Yes')])}")

# ============================================================================ #
# INSIGHTS PAGE
# ============================================================================ #
elif page == "🎯 Insights":
    st.title("🎯 Key Insights & Recommendations")
    st.write("Summary of metrics and recommendations based on gaps between mental health needs and employer support.")
    st.metric("Gap: Treatment vs Benefits", f"{(filtered_df['treatment']=='Yes').sum() - (filtered_df['benefits']=='Yes').sum()} people")

# ============================================================================ #
# Footer
# ============================================================================ #
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 11px; padding: 20px;'>
        <b>Mental Health in Tech Survey Dashboard</b><br>
        Enhanced Professional Version | 2014 Survey Data | Interactive Analysis<br>
        © 2024 Data Analysis Project
    </div>
""", unsafe_allow_html=True)
