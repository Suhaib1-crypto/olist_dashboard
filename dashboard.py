# Dashboard Settings

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# Import Business Data

customers = pd.read_csv("olist_customers_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")

# Build Unified Dataset

df = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

df = df.merge(
    payments,
    on="order_id",
    how="left"
)

df = df.merge(
    reviews,
    on="order_id",
    how="left"
)

df = df.merge(
    items,
    on="order_id",
    how="left"
)

# Date Processing

df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

# Dashboard Theme Engine

st.markdown("""
<style>
...
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Main Background */

.stApp{
    
    background-color:#0F1117;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background-color:#161B22;
}

/* Dashboard Title */

.main-title{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#FF9900;
    margin-bottom:10px;
}

/* Subtitle */

.sub-title{
    text-align:center;
    color:#C9D1D9;
    font-size:18px;
    margin-bottom:30px;
}

/* KPI Cards */

[data-testid="stMetric"]{
    background:#161B22;
    border:1px solid #30363D;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.3);
}

/* Metric Labels */

[data-testid="stMetricLabel"]{
    color:#C9D1D9;
    font-weight:bold;
}

/* Metric Values */

[data-testid="stMetricValue"]{
    color:#FF9900;
    font-weight:bold;
}

/* Section Headings */

h2{
    color:#FF9900;
    border-bottom:2px solid #30363D;
    padding-bottom:5px;
}

/* Tables */

[data-testid="stDataFrame"]{
    border:1px solid #30363D;
    border-radius:10px;
}

/* Download Button */

.stDownloadButton > button{
    background-color:#FF9900;
    color:black;
    font-weight:bold;
    border:none;
    border-radius:10px;
    padding:10px 20px;
}

.stDownloadButton > button:hover{
    background-color:#FFB84D;
}

/* General Text */

p, label, div{
    color:#E6EDF3;
}

</style>
""", unsafe_allow_html=True)

# Dashboard Theme Engine

st.markdown("""
<style>

AMAZON THEME CSS

</style>
""", unsafe_allow_html=True)

# Main Dashboard Banner

st.markdown("""
<div class='main-title'>
🛒 OLIST BUSINESS INTELLIGENCE DASHBOARD
</div>

<div class='sub-title'>
Revenue • Customers • Orders • Payment Analytics
</div>
""", unsafe_allow_html=True)

# Business Performance Indicators

...

total_orders = df["order_id"].nunique()
total_revenue = df["payment_value"].sum()
total_customers = df["customer_unique_id"].nunique()
avg_review = df["review_score"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col2:
    st.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

with col3:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "Average Review",
        f"{avg_review:.2f}"
    )

# Revenue Intelligence

st.markdown("## 📈 Revenue Intelligence")

monthly_sales = (
    df.groupby(
        df["order_purchase_timestamp"].dt.to_period("M")
    )["payment_value"]
    .sum()
    .reset_index()
)

monthly_sales["order_purchase_timestamp"] = (
    monthly_sales["order_purchase_timestamp"]
    .astype(str)
)

fig1 = px.line(
    monthly_sales,
    x="order_purchase_timestamp",
    y="payment_value",
    title="Monthly Revenue Trend",
    markers=True
)
fig1.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font_color="#D1D5DB"
)

fig1.update_traces(
    line_color="#D1D5DB"
)


st.plotly_chart(fig1, use_container_width=True)


# Payment Behaviour Analysis

st.markdown("## 💳 Payment Behaviour Analysis")

payment_chart = (
    df.groupby("payment_type")["payment_value"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    payment_chart,
    names="payment_type",
    values="payment_value",
    title="Revenue Distribution by Payment Method"
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(color="white"),
    legend=dict(
        font=dict(color="white", size=14)
    )
)
fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font_color="#D1D5DB"
)

st.plotly_chart(fig2, use_container_width=True)


# Customer Satisfaction Metrics

st.markdown("## ⭐ Customer Satisfaction Metrics")

review_chart = (
    df.groupby("review_score")
    .size()
    .reset_index(name="count")
)

fig3 = px.bar(
    review_chart,
    x="review_score",
    y="count",
    title="Review Score Distribution"
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font_color="#D1D5DB"
)

fig3.update_traces(
    marker_color="#9CA3AF"
)
st.plotly_chart(fig3, use_container_width=True)


# Customer Geography Insights

st.markdown("## 🌎 Customer Geography Insights")

state_chart = (
    df.groupby("customer_state")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    state_chart,
    x="customer_state",
    y="payment_value",
    title="Top States by Revenue"
)
fig4.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font_color="#D1D5DB"
)

fig4.update_traces(
    marker_color="#9CA3AF"
)
st.plotly_chart(fig4, use_container_width=True)


# Product Performance Overview

st.markdown("## 📦 Product Performance Overview")

product_chart = (
    df.groupby("product_id")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    product_chart,
    x="product_id",
    y="payment_value",
    title="Top 10 Revenue Generating Products"
)
fig5.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(color="white"),

    xaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),

    yaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    )
)

fig5.update_traces(
    marker_color="white"
)
st.plotly_chart(fig5, use_container_width=True)


# Business Correlation Matrix

st.markdown("## 🔥 Business Correlation Matrix")

numeric_df = df.select_dtypes(include="number")

corr_matrix = numeric_df.corr()

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="Greys",
    ax=ax
)

st.pyplot(fig)


# Executive Summary Table

st.markdown("## 📋 Executive Summary Table")

summary_table = df[
    [
        "order_id",
        "customer_state",
        "payment_type",
        "payment_value",
        "review_score"
    ]
].head(100)

st.dataframe(summary_table)


# Data Export Center

st.markdown("## 📥 Data Export Center")

csv = summary_table.to_csv(index=False)

st.download_button(
    label="Download Summary Data",
    data=csv,
    file_name="olist_summary.csv",
    mime="text/csv"
)


# Dashboard Credits

st.markdown("---")

st.markdown(
    """
    ### 🛒 Olist E-Commerce Analytics Dashboard

    Developed using Streamlit, Plotly, Pandas and Seaborn.

    Features:
    - Revenue Analytics
    - Customer Insights
    - Payment Behaviour Analysis
    - Product Performance Tracking
    - Review Intelligence
    """
)