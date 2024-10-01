import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')



st.set_page_config(page_title="PS Dash",page_icon=":bar_chart:",layout='wide')
st.title(" :bar_chart: ProShippiers Month Over Month Dashboard")

# st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True) # Remove the space from top to content

fl = st.file_uploader(":file_folder: Upload CSV file", type=['csv',"xls","xlsx"])
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)

else:
    os.chdir(r"C:\Users\sergi\PycharmProjects\psDashboard")
    df = pd.read_csv("data.csv")

st.sidebar.header("Filtrar datos:")
month = st.sidebar.multiselect("Seleccionar mes:",df["Month"].unique())
broker = st.sidebar.multiselect("Seleccionar broker:",df["Broker"].unique())

if not month and not broker:
    filtered = df
elif not month:
    filtered = df[df['Broker'].isin(broker)]
elif not broker:
    filtered = df[df['Month'].isin(month)]
else:
    filtered = df[df['Month'].isin(month)]
