import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Dictionary to map month names to their chronological order
month_to_num = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}
# sorted_data = sorted(data, key=lambda x: (x[1], month_to_num[x[0]]))


st.set_page_config(page_title="PS Dash",page_icon=":bar_chart:",layout='wide')
st.title(" :chart_with_upwards_trend: ProShippiers Month Over Month Dashboard",anchor='title')
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
    df = pd.read_csv("datav2.csv")


def get_latest_data(df_1):
    # Ensure 'Year' and 'Month' columns are numeric
    df_1['Year'] = pd.to_numeric(df_1['Year'])
    df_1['MonthNum'] = df['Month'].map(month_to_num)

    # Get the max year
    max_year = df_1['Year'].max()

    # Filter for the max year
    df_latest_year = df_1[df_1['Year'] == max_year]

    # Get the max month for the latest year
    max_month = df_latest_year['Month'].max()

    # Filter for the max month in the latest year
    df_latest = df_latest_year[df_latest_year['Month'] == max_month].iloc[:1, :2]

    return df_latest

latest_data = get_latest_data(df)


def order_data_by_year_and_month(df):
    # Add a month number column for sorting
    df['MonthNum'] = df['Month'].map(month_to_num)

    # Sort the dataframe by Year and MonthNum
    df_sorted = df.sort_values(['Year', 'MonthNum'])

    # Drop the MonthNum column as it's no longer needed
    df_sorted = df_sorted.drop('MonthNum', axis=1)

    return df_sorted

unique_months = df["Month"].unique()
sorted_months = sorted(unique_months, key=lambda x: month_to_num[x])


# Create sidebar menu
st.sidebar.header("Filtrar datos:")
year = st.sidebar.multiselect("Seleccionar año:", options=df["Year"].unique(), default=latest_data["Year"].iloc[0])
month = st.sidebar.multiselect("Seleccionar mes:", options=sorted_months, default=latest_data["Month"].iloc[0])
broker = st.sidebar.multiselect("Seleccionar broker:", options=df["Broker"].unique(), default=df["Broker"].unique())

# Filter dataframe
filtered_df = df[(df["Month"].isin(month)) & (df["Broker"].isin(broker)) & (df["Year"].isin(year))]
ordered_df = order_data_by_year_and_month(filtered_df)
print(ordered_df)
# Row 1 ---------------------------------------------------------------------------------------
r1col1, r1col2, r1col3 = st.columns((1,1,1))
r2col1, r2col2, r2col3 = st.columns((1,1,1))

# Current month
r1col1.html('<span class="column1"></span>')
r1col1.metric(
    label="September",
    value = f"${10:,.2f}",
    delta = "2"
)


# Previous Month
r1col2.html('<span class="column2"></span>')
r1col2.metric(
    label="August",
    value = f"${10:,.2f}",
    delta = "2"
)

# MoM %
r1col3.html('<span class="colum3"></span>')
r1col3.metric(
    label="MoM %",
    value = "10%",
    delta = "-2"
)


# Line chart: Fee trend by month
monthly_fee = ordered_df.groupby("Month")["Broker Fee"].sum().reset_index()
# Sort the result based on the predefined month order
monthly_fee['Month'] = pd.Categorical(monthly_fee['Month'], categories=month_to_num, ordered=True)
monthly_fee = monthly_fee.sort_values('Month')

fig2 = px.line(monthly_fee, x="Month", y="Broker Fee", title="Sales by Month", markers=True, color_discrete_sequence=['rgb(204,102,119)'])
st.plotly_chart(fig2)


# Row 2 -------------------------------------------------------------------------------------
# Display current month loss
r2col2.html('<span class="column4"></span>')
total_loss = filtered_df["Loss"].sum()
r2col2.metric(
    label="Total",
    value= f"${total_loss:,.2f}"
)

# Display current month broker fee
r2col1.html('<span class="column4"></span>')
total_fee = filtered_df["Broker Fee"].sum()
r2col1.metric(
    label="Net",
    value= f"${total_fee:,.2f}"
)

# Display current month broker fee
r2col3.html('<span class="column4"></span>')
gross_fee = total_fee - total_loss
r2col3.metric(
    label="Gross",
    value= f"${gross_fee:,.2f}"
)
