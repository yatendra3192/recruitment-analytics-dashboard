import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import os

# Page configuration
st.set_page_config(page_title="Recruitment Analytics Dashboard", layout="wide", page_icon="📊")

# Load data
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    elif os.path.exists('datafile.xlsx'):
        df = pd.read_excel('datafile.xlsx')
    else:
        return None

    # Clean date columns
    date_columns = ['Req Date\n (DD-MMM-YY)', 'Req Approved on (DD-MMM-YY)',
                    'Requisition Assigned', 'DOJ\n(DD-MMM-YY)']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

# Dashboard Title
st.title("📊 Recruitment Analytics Dashboard")

# File upload section
uploaded_file = st.file_uploader("Upload your recruitment data (Excel file)", type=['xlsx', 'xls'])

# Load the data
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    df = load_data()

# Check if data is loaded
if df is None:
    st.warning("⚠️ Please upload an Excel file to view the dashboard.")
    st.info("📋 Expected columns include: Requisition details, Status, Business Unit, Department, Location, TAT metrics, etc.")
    st.stop()

st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")
if 'Business Unit' in df.columns:
    business_units = ['All'] + sorted(df['Business Unit'].dropna().unique().tolist())
    selected_bu = st.sidebar.selectbox("Business Unit", business_units)

if 'Department' in df.columns:
    departments = ['All'] + sorted(df['Department'].dropna().unique().tolist())
    selected_dept = st.sidebar.selectbox("Department", departments)

if 'Location' in df.columns:
    locations = ['All'] + sorted(df['Location'].dropna().unique().tolist())
    selected_location = st.sidebar.selectbox("Location", locations)

# Apply filters
filtered_df = df.copy()
if 'Business Unit' in df.columns and selected_bu != 'All':
    filtered_df = filtered_df[filtered_df['Business Unit'] == selected_bu]
if 'Department' in df.columns and selected_dept != 'All':
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
if 'Location' in df.columns and selected_location != 'All':
    filtered_df = filtered_df[filtered_df['Location'] == selected_location]

# KPI Metrics Row
st.header("📈 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Requisitions", len(filtered_df))
with col2:
    if 'Broad Status' in filtered_df.columns:
        closed = len(filtered_df[filtered_df['Broad Status'].str.contains('Closed|Joined', case=False, na=False)])
        st.metric("Closed Positions", closed)
with col3:
    if 'Current TAT\n(Days since Req approved)' in filtered_df.columns:
        tat_numeric = pd.to_numeric(filtered_df['Current TAT\n(Days since Req approved)'], errors='coerce')
        avg_tat = tat_numeric.mean()
        st.metric("Avg TAT (Days)", f"{avg_tat:.1f}" if not pd.isna(avg_tat) else "N/A")
with col4:
    if 'Total nos of profiles shared' in filtered_df.columns:
        total_profiles = filtered_df['Total nos of profiles shared'].sum()
        st.metric("Total Profiles Shared", int(total_profiles) if not pd.isna(total_profiles) else 0)
with col5:
    if 'Interviewed' in filtered_df.columns:
        interviewed = filtered_df['Interviewed'].sum()
        st.metric("Candidates Interviewed", int(interviewed) if not pd.isna(interviewed) else 0)

st.markdown("---")

# Row 1: Two column charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Requisitions by Status")
    if 'Broad Status' in filtered_df.columns:
        status_counts = filtered_df['Broad Status'].value_counts()
        fig1 = px.pie(values=status_counts.values, names=status_counts.index,
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, width='stretch')

with col2:
    st.subheader("🏢 Requisitions by Business Unit")
    if 'Business Unit' in filtered_df.columns:
        bu_counts = filtered_df['Business Unit'].value_counts().head(10)
        fig2 = px.bar(x=bu_counts.index, y=bu_counts.values,
                     labels={'x': 'Business Unit', 'y': 'Count'},
                     color=bu_counts.values,
                     color_continuous_scale='Blues')
        fig2.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig2, width='stretch')

# Row 2: Two column charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("📍 Requisitions by Location")
    if 'Location' in filtered_df.columns:
        location_counts = filtered_df['Location'].value_counts().head(10)
        fig3 = px.bar(x=location_counts.index, y=location_counts.values,
                     labels={'x': 'Location', 'y': 'Count'},
                     color=location_counts.values,
                     color_continuous_scale='Greens')
        fig3.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig3, width='stretch')

with col4:
    st.subheader("👥 Gender Distribution")
    if 'Gender' in filtered_df.columns:
        gender_counts = filtered_df['Gender'].value_counts()
        fig4 = px.pie(values=gender_counts.values, names=gender_counts.index,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig4, width='stretch')

# Row 3: Time series chart
st.subheader("📅 Requisition Trends Over Time")
if 'Req Date\n (DD-MMM-YY)' in filtered_df.columns:
    req_data_clean = filtered_df[filtered_df['Req Date\n (DD-MMM-YY)'].notna()].copy()
    if len(req_data_clean) > 0:
        req_over_time = req_data_clean.set_index('Req Date\n (DD-MMM-YY)').resample('ME').size()
        fig5 = px.line(x=req_over_time.index, y=req_over_time.values,
                       labels={'x': 'Month', 'y': 'Number of Requisitions'},
                       markers=True)
        fig5.update_traces(line_color='#636EFA', line_width=3)
        st.plotly_chart(fig5, width='stretch')
    else:
        st.info("No valid date data available for trend analysis")

# Row 4: Two column charts
col5, col6 = st.columns(2)

with col5:
    st.subheader("💼 Candidate Sources")
    if 'Candidate Source' in filtered_df.columns:
        source_counts = filtered_df['Candidate Source'].value_counts().head(8)
        fig6 = px.bar(x=source_counts.values, y=source_counts.index,
                     orientation='h',
                     labels={'x': 'Count', 'y': 'Source'},
                     color=source_counts.values,
                     color_continuous_scale='Oranges')
        fig6.update_layout(showlegend=False)
        st.plotly_chart(fig6, width='stretch')

with col6:
    st.subheader("🎯 New vs Replacement")
    if 'New/ Replacement' in filtered_df.columns:
        new_replace_counts = filtered_df['New/ Replacement'].value_counts()
        fig7 = px.bar(x=new_replace_counts.index, y=new_replace_counts.values,
                     labels={'x': 'Type', 'y': 'Count'},
                     color=new_replace_counts.index,
                     color_discrete_sequence=['#FF6692', '#19D3F3'])
        fig7.update_layout(showlegend=False)
        st.plotly_chart(fig7, width='stretch')

# Row 5: TAT Analysis
st.subheader("⏱️ Turn Around Time (TAT) Analysis")
col7, col8 = st.columns(2)

with col7:
    if 'Current TAT\n(Days since Req approved)' in filtered_df.columns:
        tat_data = filtered_df['Current TAT\n(Days since Req approved)'].dropna()
        fig8 = px.histogram(tat_data, nbins=30,
                           labels={'value': 'TAT (Days)', 'count': 'Frequency'},
                           color_discrete_sequence=['#AB63FA'])
        fig8.update_layout(showlegend=False, title='TAT Distribution')
        st.plotly_chart(fig8, width='stretch')

with col8:
    if 'Joining TAT\n(Req Assigned to Joining)' in filtered_df.columns:
        joining_tat = filtered_df['Joining TAT\n(Req Assigned to Joining)'].dropna()
        fig9 = px.box(y=joining_tat,
                     labels={'y': 'Joining TAT (Days)'},
                     color_discrete_sequence=['#00CC96'])
        fig9.update_layout(title='Joining TAT Distribution')
        st.plotly_chart(fig9, width='stretch')

# Row 6: Department-wise analysis
st.subheader("🏛️ Top 10 Departments by Requisition Count")
if 'Department' in filtered_df.columns:
    dept_counts = filtered_df['Department'].value_counts().head(10)
    fig10 = px.bar(x=dept_counts.index, y=dept_counts.values,
                  labels={'x': 'Department', 'y': 'Count'},
                  color=dept_counts.values,
                  color_continuous_scale='Viridis')
    fig10.update_layout(showlegend=False, xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig10, width='stretch')

# Data table at the bottom
st.markdown("---")
st.subheader("📋 Detailed Data View")
st.dataframe(filtered_df, width='stretch', height=400)

# Export functionality
st.markdown("---")
col_export1, col_export2 = st.columns([1, 4])
with col_export1:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv,
        file_name=f'recruitment_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
    )
