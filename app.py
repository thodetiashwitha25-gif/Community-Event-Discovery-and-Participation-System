import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Community Dashboard", layout="wide")

# Title
st.title("🎉 Community Event Dashboard")

# Load data
df = pd.read_excel("community_events.xlsx")

# FIXED DATE FORMAT
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Sidebar filters
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

location = st.sidebar.multiselect(
    "Location",
    options=df['Location'].unique(),
    default=df['Location'].unique()
)

# Filter data
filtered_df = df[
    (df['Category'].isin(category)) &
    (df['Location'].isin(location))
]

# If data exists
if not filtered_df.empty:

    # KPIs
    st.subheader("📊 Overview")
    col1, col2 = st.columns(2)

    col1.metric("Total Events", filtered_df['Event ID'].nunique())
    col2.metric("Total Participants", int(filtered_df['Participants'].sum()))

    # Bar Chart
    st.subheader("📈 Category Analysis")
    fig1 = px.bar(filtered_df, x='Category', y='Participants', color='Category')
    st.plotly_chart(fig1, use_container_width=True)

    # Pie Chart
    st.subheader("🥧 Age Group Distribution")
    fig2 = px.pie(filtered_df, names='Age Group', values='Participants')
    st.plotly_chart(fig2, use_container_width=True)

    # Line Chart
    st.subheader("📅 Monthly Trend")
    filtered_df = filtered_df.copy()
    filtered_df['Month'] = filtered_df['Date'].dt.strftime('%Y-%m')

    fig3 = px.line(filtered_df, x='Month', y='Participants', markers=True)
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("⚠️ No data available. Check filters.")

# Show data
st.subheader("📄 Data Preview")
st.write(df)