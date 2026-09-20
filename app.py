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
# DEMOGRAPHICS PAGE (fixed Gender Distribution pie chart)
# ============================================================================ #
if page == "👥 Demographics":
    st.title("👥 Demographic Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Age Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(filtered_df['Age'], bins=20, color=COLORS['primary'], edgecolor='white', alpha=0.8)
        ax.set_xlabel('Age', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Age Distribution', fontweight='bold', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        ax.set_facecolor(COLORS['light'])
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("📈 Age Statistics")
        age_stats = pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
            'Value': [
                f"{filtered_df['Age'].mean():.2f}",
                f"{filtered_df['Age'].median():.2f}",
                f"{filtered_df['Age'].std():.2f}",
                f"{filtered_df['Age'].min()}",
                f"{filtered_df['Age'].max()}"
            ]
        })
        st.dataframe(age_stats, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👫 Gender Distribution")
        gender_counts = filtered_df['Gender'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning'], COLORS['danger']]

        wedges, texts, autotexts = ax.pie(
            gender_counts.values,
            labels=None,  # remove labels from slices
            autopct='%1.1f%%',
            colors=colors_list[:len(gender_counts)],
            startangle=90,
            pctdistance=0.8
        )

        # Legend outside the pie with proper names
        ax.legend(
            wedges,
            gender_counts.index,
            title="Gender",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        ax.set_title('Gender Distribution', fontweight='bold')
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("🌍 Top 10 Countries")
        country_counts = filtered_df['Country'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_gradient = plt.cm.Blues(np.linspace(0.4, 0.8, len(country_counts)))
        ax.barh(range(len(country_counts)), country_counts.values, color=colors_gradient, edgecolor='white')
        ax.set_yticks(range(len(country_counts)))
        ax.set_yticklabels(country_counts.index)
        ax.set_xlabel('Count', fontweight='bold')
        ax.invert_yaxis()
        ax.set_title('Top 10 Countries', fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
        plt.close()

# ============================================================================ #
# (Keep other pages: Dashboard, Mental Health, Support, Culture, Company, Analysis, Insights)
# ============================================================================ #

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 11px; padding: 20px;'>
        <b>Mental Health in Tech Survey Dashboard</b><br>
        Enhanced Professional Version | 2014 Survey Data | Interactive Analysis<br>
        © 2024 Data Analysis Project
    </div>
""", unsafe_allow_html=True)
