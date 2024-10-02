import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')



st.set_page_config(page_title="PS Dash",page_icon=":bar_chart:",layout='wide')
st.title(" :bar_chart: ProShippiers Month Over Month Dashboard",anchor='title')
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True) # Remove the space from top to content

logo_link = 'https://proshippiersweb.blob.core.windows.net/logos/ProSW.png'
st.logo(logo_link)

# Block for uploading data
load_block = st.empty()
load_container = load_block.container()

# Load data
fl = load_container.file_uploader(":file_folder: Upload CSV file", type=['csv',"xls","xlsx"])
if fl is not None:
    filename = fl.name
    df = pd.read_csv(filename)
    load_block.empty()
else:
    os.chdir(r"C:\Users\sergi\PycharmProjects\psDashboard")
    df = pd.read_csv("data.csv")

# Create sidebar menu
st.sidebar.header("Filtrar datos:")
month = st.sidebar.multiselect("Seleccionar mes:", options=df["Month"].unique(), default=df["Month"].unique())
broker = st.sidebar.multiselect("Seleccionar broker:", options=df["Broker"].unique(), default=df["Broker"].unique())

# Filter dataframe
filtered_df = df[(df["Month"].isin(month)) & (df["Broker"].isin(broker))]

col1, col2, col3, col4 = st.columns((1,1,1,1))

# Current month
col1.metric(
    label="September",
    value = "10",
    delta = "2"
)


# Previous Month
col2.metric(
    label="August",
    value = "10",
    delta = "2"
)

# MoM %
col3.metric(
    label="MoM %",
    value = "10",
    delta = "2"
)

# Display current month broker fee
total_fee = filtered_df[" Broker Fee "].sum()
col4.metric("Total", f"${total_fee:,.2f}")


# Line chart: Fee trend by month
monthly_fee = filtered_df.groupby("Month")[" Broker Fee "].sum().reset_index()
fig2 = px.line(monthly_fee, x="Month", y=" Broker Fee ", title="Sales by Month", markers=True, color_discrete_sequence=['rgb(204,102,119)'])
st.plotly_chart(fig2)



