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

# Load data
fl = st.file_uploader(":file_folder: Upload CSV file", type=['csv',"xls","xlsx"])
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
    os.chdir(r"C:\Users\sergi\PycharmProjects\psDashboard")
    df = pd.read_csv("data.csv")

st.sidebar.header("Filtrar datos:")
month = st.sidebar.multiselect("Seleccionar mes:", options=df["Month"].unique(), default=df["Month"].unique())
broker = st.sidebar.multiselect("Seleccionar broker:", options=df["Broker"].unique(), default=df["Broker"].unique())

# Filter dataframe
filtered_df = df[(df["Month"].isin(month)) & (df["Broker"].isin(broker))]

# Line chart: Fee trend by month
monthly_fee = filtered_df.groupby("Month")[" Broker Fee "].sum().reset_index()
fig2 = px.line(monthly_fee, x="Month", y=" Broker Fee ", title="Tendencia de Comisiones por Mes")
st.plotly_chart(fig2)

# Display total broker fee
total_fee = filtered_df[" Broker Fee "].sum()
st.metric("Comisión Total", f"${total_fee:,.2f}")

st.metric(
    label="MoM %",
    value = "10",
    delta = "2"
)