import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Mental Health in Tech - Professional Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colors
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'danger': '#D62828',
    'warning': '#F77F00',
    'light': '#F0F2F6',
    'dark': '#1F1F1F'
}

sns.set_style("whitegrid")
sns.set_context("talk")  # larger fonts

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('mental_health_survey.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['age_group'] = pd.cut(df['Age'], bins=[0,25,35,45,55,100],
                             labels=['18-25','26-35','36-45','46-55','55+'])
    return df

df = load_data()

# Sidebar
page = st.sidebar.radio("📍 SELECT PAGE",
    ["📊 Dashboard","👥 Demographics","❤️ Mental Health","🏢 Support",
     "💼 Culture","🏭 Company","📈 Analysis","🎯 Insights"])

# Filters
selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(df['Country'].unique().tolist()))
selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(df['Gender'].unique().tolist()))
selected_size = st.sidebar.selectbox("Select Company Size", ["All","1-5","6-25","26-100","100-500","500-1000","1000+"])

filtered_df = df.copy()
if selected_country != "All": filtered_df = filtered_df[filtered_df['Country']==selected_country]
if selected_gender != "All": filtered_df = filtered_df[filtered_df['Gender']==selected_gender]
if selected_size != "All": filtered_df = filtered_df[filtered_df['no_employees']==selected_size]

# DASHBOARD
if page=="📊 Dashboard":
    st.title("🧠 Dashboard Overview")
    col1,col2,col3,col4 = st.columns(4)
    with col1: st.metric("Respondents", f"{len(filtered_df):,}")
    with col2: st.metric("Treatment Yes", (filtered_df['treatment']=='Yes').sum())
    with col3: st.metric("Family History Yes", (filtered_df['family_history']=='Yes').sum())
    with col4: st.metric("Benefits Yes", (filtered_df['benefits']=='Yes').sum())

    st.markdown("---")
    st.subheader("📈 Treatment vs Family History")
    crosstab = pd.crosstab(filtered_df['family_history'], filtered_df['treatment'])
    fig, ax = plt.subplots(figsize=(12,6))
    crosstab.plot(kind='bar', ax=ax, color=[COLORS['danger'],COLORS['success']], edgecolor='white')
    ax.set_title("Treatment Seeking by Family History", fontsize=16, fontweight='bold')
    st.pyplot(fig)

# DEMOGRAPHICS
elif page=="👥 Demographics":
    st.title("👥 Demographics")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Age Distribution")
        fig, ax = plt.subplots(figsize=(12,6))
        ax.hist(filtered_df['Age'], bins=15, color=COLORS['primary'], edgecolor='white', alpha=0.85)
        ax.set_title("Age Distribution", fontsize=16, fontweight='bold')
        st.pyplot(fig)
    with col2:
        st.subheader("Gender Distribution")
        gender_counts = filtered_df['Gender'].value_counts()
        fig, ax = plt.subplots(figsize=(8,6))
        wedges, texts, autotexts = ax.pie(gender_counts.values, autopct='%1.1f%%',
                                          colors=[COLORS['primary'],COLORS['secondary'],COLORS['success'],COLORS['warning'],COLORS['danger']],
                                          startangle=90, pctdistance=0.75)
        ax.legend(wedges, gender_counts.index, title="Gender", loc="center left", bbox_to_anchor=(1,0,0.5,1))
        ax.set_title("Gender Distribution", fontsize=16, fontweight='bold')
        st.pyplot(fig)

# MENTAL HEALTH
elif page=="❤️ Mental Health":
    st.title("❤️ Mental Health")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Treatment Status")
        treatment_counts = filtered_df['treatment'].value_counts()
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(x=treatment_counts.index, y=treatment_counts.values, palette=[COLORS['success'],COLORS['danger']], ax=ax)
        ax.set_title("Treatment Status", fontsize=16, fontweight='bold')
        st.pyplot(fig)
    with col2:
        st.subheader("Work Interference")
        work_counts = filtered_df['work_interfere'].value_counts()
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(x=work_counts.index, y=work_counts.values, palette="muted", ax=ax)
        ax.set_title("Work Interference", fontsize=16, fontweight='bold')
        st.pyplot(fig)

# SUPPORT
elif page=="🏢 Support":
    st.title("🏢 Employer Support")
    support_cols = ['benefits','care_options','wellness_program','seek_help','anonymity']
    for col in support_cols:
        st.subheader(col.replace("_"," ").title())
        counts = filtered_df[col].value_counts()
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(x=counts.index, y=counts.values, palette="Blues", ax=ax)
        ax.set_title(f"{col.replace('_',' ').title()} Responses", fontsize=16, fontweight='bold')
        st.pyplot(fig)

# CULTURE
elif page=="💼 Culture":
    st.title("💼 Workplace Culture")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Coworkers")
        counts = filtered_df['coworkers'].value_counts()
        fig, ax = plt.subplots(figsize=(8,6))
        ax.pie(counts.values, autopct='%1.1f%%', colors=[COLORS['primary'],COLORS['secondary'],COLORS['success']], startangle=90)
        ax.legend(counts.index, title="Coworkers", loc="center left", bbox_to_anchor=(1,0,0.5,1))
        st.pyplot(fig)
    with col2:
        st.subheader("Supervisor")
        counts = filtered_df['supervisor'].value_counts()
        fig, ax = plt.subplots(figsize=(8,6))
        ax.pie(counts.values, autopct='%1.1f%%', colors=[COLORS['primary'],COLORS['secondary'],COLORS['success']], startangle=90)
        ax.legend(counts.index, title="Supervisor", loc="center left", bbox_to_anchor=(1,0,0.5,1))
        st.pyplot(fig)

# COMPANY
elif page=="🏭 Company":
    st.title("🏭 Company Analysis")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Company Size")
        counts = filtered_df['no_employees'].value_counts()
        fig, ax = plt.subplots(figsize=(12,6))
        sns.barplot(x=counts.index, y=counts.values, palette="Blues_d", ax=ax)
        ax.set_title("Company Size Distribution", fontsize=16, fontweight='bold')
        st.pyplot(fig)
    with col2:
        st.subheader("Tech vs Non-Tech")
        counts = filtered_df['tech_company'].value_counts()
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(x=counts.index, y=counts.values, palette=[COLORS['primary'],COLORS['secondary']], ax=ax)
        ax.set_title("Company Type", fontsize=16, fontweight='bold')
        st.pyplot(fig)

# ANALYSIS
elif page=="📈 Analysis":
    st.title("📈 Cross Analysis")
    st.subheader("Treatment by Gender")
    crosstab = pd.crosstab(filtered_df['Gender'], filtered_df['treatment'])
    fig, ax = plt.subplots(figsize=(12,6))
    crosstab.plot(kind='bar', ax=ax, color=[COLORS['danger'],COLORS['success']], edgecolor='white')
    ax.set_title("Treatment Seeking by Gender", fontsize=16, fontweight='bold')
    st.pyplot(fig)

# INSIGHTS
elif page=="🎯 Insights":
    st.title("🎯 Insights & Recommendations")
    treatment_pct = (filtered_df['treatment']=='Yes').mean()*100
    benefits_pct = (filtered_df['benefits']=='Yes').mean()*100