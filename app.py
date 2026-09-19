"""
Mental Health in Tech Survey - Enhanced Streamlit Web App
Professional Dashboard with Filters and Advanced Features
"""

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
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'success': '#06A77D',      # Green
    'danger': '#D62828',       # Red
    'warning': '#F77F00',      # Orange
    'light': '#F0F2F6',        # Light gray
    'dark': '#1F1F1F'          # Dark gray
}

# Custom CSS for professional look
st.markdown(f"""
    <style>
    /* Main background */
    .main {{
        background-color: {COLORS['light']};
    }}
    
    /* Metrics styling */
    .metric-container {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }}
    
    /* Header styling */
    h1 {{
        color: {COLORS['primary']};
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 3px solid {COLORS['secondary']};
    }}
    
    h2 {{
        color: {COLORS['primary']};
        margin-top: 30px;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: white;
        border-right: 3px solid {COLORS['primary']};
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['secondary']};
    }}
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('mental_health_survey.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['age_group'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 100], 
                             labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    return df

df = load_data()

# Sidebar - Navigation and Filters
st.sidebar.markdown("# 🧠 Mental Health in Tech")
st.sidebar.markdown("---")

# Main page selection
page = st.sidebar.radio(
    "📍 SELECT PAGE",
    [
        "📊 Dashboard",
        "👥 Demographics",
        "❤️ Mental Health",
        "🏢 Support",
        "💼 Culture",
        "🏭 Company",
        "📈 Analysis",
        "🎯 Insights"
    ],
    help="Choose a section to explore"
)

st.sidebar.markdown("---")

# Global Filters
st.sidebar.markdown("### 🔍 FILTERS")

# Filter by country
selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df['Country'].unique().tolist()),
    help="Filter data by country"
)

# Filter by gender
selected_gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df['Gender'].unique().tolist()),
    help="Filter data by gender"
)

# Filter by company size
selected_size = st.sidebar.selectbox(
    "Select Company Size",
    ["All", "1-5", "6-25", "26-100", "100-500", "500-1000", "1000+"],
    help="Filter data by company size"
)

# Apply filters
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_size != "All":
    filtered_df = filtered_df[filtered_df['no_employees'] == selected_size]

st.sidebar.markdown("---")
st.sidebar.info(
    f"📊 **Current Dataset:** {len(filtered_df)}/{len(df)} respondents\n\n"
    f"🌍 **Country:** {selected_country}\n\n"
    f"👤 **Gender:** {selected_gender}\n\n"
    f"🏢 **Company Size:** {selected_size}"
)

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================
if page == "📊 Dashboard":
    st.title("🧠 Mental Health in Tech Survey")
    st.markdown("**Professional Analysis Dashboard | 2014 Survey Data**")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Respondents",
            f"{len(filtered_df):,}",
            f"{len(filtered_df)-len(df)} filtered",
            delta_color="off"
        )
    
    with col2:
        treatment_pct = (len(filtered_df[filtered_df['treatment'] == 'Yes']) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.metric(
            "Sought Treatment",
            f"{treatment_pct:.1f}%",
            f"{int(len(filtered_df[filtered_df['treatment'] == 'Yes']))} people"
        )
    
    with col3:
        family_pct = (len(filtered_df[filtered_df['family_history'] == 'Yes']) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.metric(
            "Family History",
            f"{family_pct:.1f}%",
            f"{int(len(filtered_df[filtered_df['family_history'] == 'Yes']))} people"
        )
    
    with col4:
        benefits_pct = (len(filtered_df[filtered_df['benefits'] == 'Yes']) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.metric(
            "Have Benefits",
            f"{benefits_pct:.1f}%",
            f"{int(len(filtered_df[filtered_df['benefits'] == 'Yes']))} people"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Quick Overview")
        overview_data = {
            "Total Respondents": len(filtered_df),
            "Countries": filtered_df['Country'].nunique(),
            "Average Age": f"{filtered_df['Age'].mean():.1f}",
            "Age Range": f"{filtered_df['Age'].min()}-{filtered_df['Age'].max()}",
            "Tech Companies": f"{(filtered_df['tech_company'] == 'Yes').sum()}",
            "Remote Workers": f"{(filtered_df['remote_work'] == 'Yes').sum()}"
        }
        for key, value in overview_data.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.subheader("💡 Mental Health Summary")
        mh_data = {
            "Sought Treatment": f"{(filtered_df['treatment'] == 'Yes').sum()} ({(len(filtered_df[filtered_df['treatment'] == 'Yes']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0:.1f}%)",
            "Family History": f"{(filtered_df['family_history'] == 'Yes').sum()} ({(len(filtered_df[filtered_df['family_history'] == 'Yes']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0:.1f}%)",
            "Work Interference": f"{(filtered_df['work_interfere'].isin(['Sometimes', 'Often'])).sum()}",
            "Has Benefits": f"{(filtered_df['benefits'] == 'Yes').sum()} ({(len(filtered_df[filtered_df['benefits'] == 'Yes']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0:.1f}%)",
            "Fear Consequences": f"{(filtered_df['mental_health_consequence'] == 'Yes').sum()} ({(len(filtered_df[filtered_df['mental_health_consequence'] == 'Yes']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0:.1f}%)",
            "Remote Workers": f"{(filtered_df['remote_work'] == 'Yes').sum()} ({(len(filtered_df[filtered_df['remote_work'] == 'Yes']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0:.1f}%)"
        }
        for key, value in mh_data.items():
            st.write(f"**{key}:** {value}")


# ============================================================================
# PAGE 2: DEMOGRAPHICS
# ============================================================================
elif page == "👥 Demographics":
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
        colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning']]
        ax.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
               colors=colors_list, startangle=90)
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


# ============================================================================
# PAGE 3: MENTAL HEALTH
# ============================================================================
elif page == "❤️ Mental Health":
    st.title("❤️ Mental Health Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏥 Treatment Status")
        treatment_counts = filtered_df['treatment'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_treatment = [COLORS['success'], COLORS['danger']]
        bars = ax.bar(treatment_counts.index, treatment_counts.values, color=colors_treatment, edgecolor='white', alpha=0.8)
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Have You Sought Treatment?', fontweight='bold')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}\n({height/len(filtered_df)*100:.1f}%)',
                   ha='center', va='bottom', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("👨‍👩‍👧 Family History")
        family_counts = filtered_df['family_history'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_family = [COLORS['danger'], COLORS['success']]
        bars = ax.bar(family_counts.index, family_counts.values, color=colors_family, edgecolor='white', alpha=0.8)
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Family History of Mental Illness', fontweight='bold')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}\n({height/len(filtered_df)*100:.1f}%)',
                   ha='center', va='bottom', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Work Interference")
        work_int_counts = filtered_df['work_interfere'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_work = [COLORS['danger'], COLORS['warning'], COLORS['primary'], COLORS['success']]
        ax.bar(range(len(work_int_counts)), work_int_counts.values, color=colors_work, edgecolor='white', alpha=0.8)
        ax.set_xticks(range(len(work_int_counts)))
        ax.set_xticklabels(work_int_counts.index, rotation=45)
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Mental Health Impact on Work', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("😟 Fear of Consequences")
        consequence_counts = filtered_df['mental_health_consequence'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_consequence = [COLORS['danger'], COLORS['success'], '#95a5a6']
        ax.bar(consequence_counts.index, consequence_counts.values, color=colors_consequence, edgecolor='white', alpha=0.8)
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Fear of Negative Consequences', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()


# ============================================================================
# PAGE 4: EMPLOYER SUPPORT
# ============================================================================
elif page == "🏢 Support":
    st.title("🏢 Employer Support Analysis")
    
    support_cols = ['benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity']
    titles = ['Mental Health Benefits', 'Care Options Awareness', 'Wellness Program', 
              'Resources to Learn', 'Anonymity Protected']
    
    for idx, (col, title) in enumerate(zip(support_cols, titles)):
        if idx % 3 == 0:
            cols = st.columns(3)
        
        with cols[idx % 3]:
            st.subheader(title)
            counts = filtered_df[col].value_counts()
            fig, ax = plt.subplots(figsize=(6, 4))
            colors_list = [COLORS['success'], COLORS['danger'], COLORS['primary']][:len(counts)]
            ax.bar(range(len(counts)), counts.values, color=colors_list, edgecolor='white', alpha=0.8)
            ax.set_xticks(range(len(counts)))
            ax.set_xticklabels(counts.index, rotation=45, ha='right')
            ax.set_ylabel('Count', fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
            plt.close()


# ============================================================================
# PAGE 5: WORKPLACE CULTURE
# ============================================================================
elif page == "💼 Culture":
    st.title("💼 Workplace Culture & Communication")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Discuss with Coworkers")
        coworkers_counts = filtered_df['coworkers'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['success']][:len(coworkers_counts)]
        wedges, texts, autotexts = ax.pie(coworkers_counts.values, labels=coworkers_counts.index, 
                                           autopct='%1.1f%%', colors=colors_list, startangle=90)
        ax.set_title('Willing to Discuss with Coworkers?', fontweight='bold')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("👔 Discuss with Supervisor")
        supervisor_counts = filtered_df['supervisor'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['success']][:len(supervisor_counts)]
        wedges, texts, autotexts = ax.pie(supervisor_counts.values, labels=supervisor_counts.index,
                                           autopct='%1.1f%%', colors=colors_list, startangle=90)
        ax.set_title('Willing to Discuss with Supervisor?', fontweight='bold')
        st.pyplot(fig)
        plt.close()


# ============================================================================
# PAGE 6: COMPANY ANALYSIS
# ============================================================================
elif page == "🏭 Company":
    st.title("🏭 Company & Employment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Company Size Distribution")
        size_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', '1000+']
        company_size_counts = filtered_df['no_employees'].value_counts().reindex(size_order)
        fig, ax = plt.subplots(figsize=(10, 5))
        colors_gradient = plt.cm.Blues(np.linspace(0.4, 0.8, len(company_size_counts)))
        ax.bar(range(len(company_size_counts)), company_size_counts.values, color=colors_gradient, edgecolor='white', alpha=0.8)
        ax.set_xticks(range(len(company_size_counts)))
        ax.set_xticklabels(company_size_counts.index, rotation=45)
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Company Size Distribution', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("💻 Tech vs Non-Tech")
        tech_counts = filtered_df['tech_company'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_tech = [COLORS['primary'], COLORS['secondary']]
        bars = ax.bar(['Tech', 'Non-Tech'], tech_counts.values, color=colors_tech, edgecolor='white', alpha=0.8)
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Company Type', fontweight='bold')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}\n({height/len(filtered_df)*100:.1f}%)',
                   ha='center', va='bottom', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()


# ============================================================================
# PAGE 7: CROSS-ANALYSIS
# ============================================================================
elif page == "📈 Analysis":
    st.title("📈 Cross-Analysis of Variables")
    
    analysis_type = st.selectbox(
        "Select Analysis",
        [
            "Treatment vs Family History",
            "Benefits vs Work Interference",
            "Treatment by Gender",
            "Treatment by Age Group",
            "Benefits by Company Size",
            "Tech vs Non-Tech Support"
        ]
    )
    
    if analysis_type == "Treatment vs Family History":
        st.subheader("Treatment Status by Family History")
        crosstab_data = pd.crosstab(filtered_df['family_history'], filtered_df['treatment'])
        fig, ax = plt.subplots(figsize=(10, 5))
        crosstab_data.plot(kind='bar', ax=ax, color=[COLORS['danger'], COLORS['success']], edgecolor='white', alpha=0.8)
        ax.set_title('Treatment Seeking by Family History', fontweight='bold')
        ax.set_xlabel('Family History', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.legend(['No', 'Yes'], title='Treatment')
        ax.tick_params(axis='x', rotation=0)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    elif analysis_type == "Treatment by Gender":
        st.subheader("Treatment Seeking by Gender")
        treatment_gender = pd.crosstab(filtered_df['Gender'], filtered_df['treatment'])
        fig, ax = plt.subplots(figsize=(10, 5))
        treatment_gender.plot(kind='bar', ax=ax, color=[COLORS['danger'], COLORS['success']], edgecolor='white', alpha=0.8)
        ax.set_title('Treatment Seeking by Gender', fontweight='bold')
        ax.set_xlabel('Gender', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.legend(['No', 'Yes'], title='Treatment')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        plt.close()


# ============================================================================
# PAGE 8: INSIGHTS
# ============================================================================
elif page == "🎯 Insights":
    st.title("🎯 Key Insights & Recommendations")
    
    if len(filtered_df) > 0:
        treatment_pct = (len(filtered_df[filtered_df['treatment'] == 'Yes']) / len(filtered_df)) * 100
        family_pct = (len(filtered_df[filtered_df['family_history'] == 'Yes']) / len(filtered_df)) * 100
        work_interference_pct = (len(filtered_df[filtered_df['work_interfere'].isin(['Sometimes', 'Often'])]) / len(filtered_df)) * 100
        benefits_pct = (len(filtered_df[filtered_df['benefits'] == 'Yes']) / len(filtered_df)) * 100
        fear_consequences_pct = (len(filtered_df[filtered_df['mental_health_consequence'] == 'Yes']) / len(filtered_df)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Mental Health Prevalence")
            st.markdown(f"""
            - **{treatment_pct:.1f}%** of respondents have sought treatment
            - **{family_pct:.1f}%** have a family history of mental illness
            - **{work_interference_pct:.1f}%** report significant work interference
            
            **Insight:** Mental health is a significant concern in tech industry.
            """)
        
        with col2:
            st.subheader("🏢 Employer Support Gap")
            st.markdown(f"""
            - **{benefits_pct:.1f}%** have access to mental health benefits
            - **{(len(filtered_df[filtered_df['care_options'] == 'Yes']) / len(filtered_df)) * 100:.1f}%** are aware of available options
            - **{(len(filtered_df[filtered_df['wellness_program'] == 'Yes']) / len(filtered_df)) * 100:.1f}%** have wellness programs
            
            **Insight:** Significant gap between need and support.
            """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💼 Workplace Communication")
            st.markdown(f"""
            - **{(len(filtered_df[filtered_df['coworkers'] == 'Yes']) / len(filtered_df)) * 100:.1f}%** willing to discuss with coworkers
            - **{(len(filtered_df[filtered_df['supervisor'] == 'Yes']) / len(filtered_df)) * 100:.1f}%** willing to discuss with supervisors
            - **{fear_consequences_pct:.1f}%** fear negative consequences
            
            **Insight:** Stigma remains a barrier despite willingness to discuss.
            """)
        
        with col2:
            st.subheader("🎯 Recommendations")
            st.markdown("""
            1. **Implement Comprehensive Programs**
               - Expand mental health benefits
               - Ensure awareness of resources
            
            2. **Build Supportive Culture**
               - Leadership commitment
               - Remove stigma through education
               - Create safe spaces
            
            3. **Policy Improvements**
               - Flexible leave policies
               - Anonymous support channels
               - Regular wellness check-ins
            
            4. **Support by Company Size**
               - Small companies need partnerships
               - Large companies need leadership
            """)
        
        st.markdown("---")
        st.subheader("📈 Detailed Statistics")
        
        stats_data = {
            'Metric': [
                'Sought Treatment',
                'Family History',
                'Work Interference',
                'Has Benefits',
                'Knows Care Options',
                'Wellness Program',
                'Fear Consequences',
                'Discuss with Coworkers',
                'Discuss with Supervisor',
                'Remote Workers'
            ],
            'Count': [
                len(filtered_df[filtered_df['treatment'] == 'Yes']),
                len(filtered_df[filtered_df['family_history'] == 'Yes']),
                len(filtered_df[filtered_df['work_interfere'].isin(['Sometimes', 'Often'])]),
                len(filtered_df[filtered_df['benefits'] == 'Yes']),
                len(filtered_df[filtered_df['care_options'] == 'Yes']),
                len(filtered_df[filtered_df['wellness_program'] == 'Yes']),
                len(filtered_df[filtered_df['mental_health_consequence'] == 'Yes']),
                len(filtered_df[filtered_df['coworkers'] == 'Yes']),
                len(filtered_df[filtered_df['supervisor'] == 'Yes']),
                len(filtered_df[filtered_df['remote_work'] == 'Yes'])
            ],
            'Percentage': [
                f"{treatment_pct:.1f}%",
                f"{family_pct:.1f}%",
                f"{work_interference_pct:.1f}%",
                f"{benefits_pct:.1f}%",
                f"{(len(filtered_df[filtered_df['care_options'] == 'Yes']) / len(filtered_df)) * 100:.1f}%",
                f"{(len(filtered_df[filtered_df['wellness_program'] == 'Yes']) / len(filtered_df)) * 100:.1f}%",
                f"{fear_consequences_pct:.1f}%",
                f"{(len(filtered_df[filtered_df['coworkers'] == 'Yes']) / len(filtered_df)) * 100:.1f}%",
                f"{(len(filtered_df[filtered_df['supervisor'] == 'Yes']) / len(filtered_df)) * 100:.1f}%",
                f"{(len(filtered_df[filtered_df['remote_work'] == 'Yes']) / len(filtered_df)) * 100:.1f}%"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 11px; padding: 20px;'>
        <b>Mental Health in Tech Survey Dashboard</b><br>
        Enhanced Professional Version | 2014 Survey Data | Interactive Analysis<br>
        © 2024 Data Analysis Project
    </div>
""", unsafe_allow_html=True)
