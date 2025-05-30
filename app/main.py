import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Velocity Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {font-size: 24px; font-weight: bold; margin-bottom: 20px;}
    .metric-card {background: #f8f9fa; border-radius: 10px; padding: 20px; margin-bottom: 20px;}
    .metric-value {font-size: 32px; font-weight: bold;}
    .metric-label {font-size: 14px; color: #6c757d;}
    </style>
""", unsafe_allow_html=True)

# Mock data for demo (will be replaced with real API calls)
def get_mock_velocity_metrics():
    return {
        "pr_cycle_time_days": 2.5,
        "daily_commits": 18,
        "active_contributors": 7,
        "prs_merged": 12,
        "prs_open": 4
    }

def get_mock_coverage_metrics():
    return {
        "prompt_coverage": 78,
        "test_success_rate": 92,
        "regression_failures": 3,
        "prompts_tracked": 145
    }

# Sidebar with filters
with st.sidebar:
    st.title("Filters")
    
    # Date range filter
    today = datetime.today()
    last_month = today - timedelta(days=30)
    date_range = st.date_input(
        "Date Range",
        value=(last_month, today),
        min_value=today - timedelta(days=365),
        max_value=today
    )
    
    # Team/Project filter
    teams = ["All Teams", "AI Core", "NLP Team", "Platform", "DevOps"]
    selected_team = st.selectbox("Team", teams)
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.experimental_rerun()

# Main content
st.title("📊 AI Velocity Dashboard")
st.markdown("Monitor your AI development team's productivity, test coverage, and infrastructure health.")

# Metrics Section
st.markdown("### Team Velocity")
col1, col2, col3, col4 = st.columns(4)

velocity_metrics = get_mock_velocity_metrics()

with col1:
    st.markdown("<div class='metric-card'>"
                f"<div class='metric-value'>{velocity_metrics['pr_cycle_time_days']} days</div>"
                "<div class='metric-label'>Avg PR Cycle Time</div>"
                "</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>"
                f"<div class='metric-value'>{velocity_metrics['daily_commits']}</div>"
                "<div class='metric-label'>Daily Commits</div>"
                "</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>"
                f"<div class='metric-value'>{velocity_metrics['active_contributors']}</div>"
                "<div class='metric-label'>Active Contributors</div>"
                "</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-card'>"
                f"<div class='metric-value'>{velocity_metrics['prs_merged']}/{velocity_metrics['prs_open']}</div>"
                "<div class='metric-label'>PRs Merged/Open</div>"
                "</div>", unsafe_allow_html=True)

# Charts Section
st.markdown("### Activity Over Time")

# Sample time series data
if 'date_range' in locals() and len(date_range) == 2:
    start_date, end_date = date_range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate mock data
    df = pd.DataFrame({
        'date': date_range,
        'commits': [max(0, int(10 + 10 * (i % 7) / 7 + (i % 30) / 30)) for i in range(len(date_range))],
        'prs_created': [max(1, int(2 + 3 * (i % 7) / 7 + (i % 14) / 14)) for i in range(len(date_range))],
        'prs_merged': [max(0, int(1 + 2 * (i % 7) / 7 + (i % 21) / 21)) for i in range(len(date_range))]
    })
    
    # Plot
    fig = px.line(df, x='date', y=['commits', 'prs_created', 'prs_merged'],
                 title='Development Activity',
                 labels={'value': 'Count', 'variable': 'Metric', 'date': 'Date'},
                 template='plotly_white')
    
    st.plotly_chart(fig, use_container_width=True)

# Test Coverage Section
st.markdown("### Test & Prompt Coverage")

coverage_metrics = get_mock_coverage_metrics()

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.pie(
        names=['Covered', 'Not Covered'],
        values=[coverage_metrics['prompt_coverage'], 100 - coverage_metrics['prompt_coverage']],
        title='Prompt Coverage',
        hole=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        x=['Success', 'Failures'],
        y=[coverage_metrics['test_success_rate'], 100 - coverage_metrics['test_success_rate']],
        title='Test Success Rate',
        labels={'x': 'Status', 'y': 'Percentage'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("<div class='metric-card' style='height: 300px;'>"
                f"<h4>Prompt Coverage Details</h4>"
                f"<p>Total Prompts: {coverage_metrics['prompts_tracked']}</p>"
                f"<p>Regression Failures: {coverage_metrics['regression_failures']}</p>"
                "</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*AI Velocity Dashboard v0.1.0*")

if __name__ == "__main__":
    # This is needed for Streamlit Cloud
    pass
