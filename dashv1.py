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


# Sort months --------------------------------------------------
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

# Setting current and previous month based on the Indx column
current_month = df[df['Indx'] == df['Indx'].max()].iloc[:1,:2]


# Create sidebar menu
st.sidebar.header("Filtrar datos:")
#year = st.sidebar.selectbox("Seleccionar año:", options=df["Year"].unique(), default=current_month["Year"].iloc[0])
year = st.sidebar.selectbox("Seleccionar año:", options=df["Year"].unique())
month = st.sidebar.multiselect("Seleccionar mes:", options=sorted_months, default=current_month["Month"].iloc[0])
broker = st.sidebar.multiselect("Seleccionar broker:", options=df["Broker"].unique(), default=df["Broker"].unique())

filtered_df = df[(df["Month"].isin(month)) & (df["Broker"].isin(broker)) & (df["Year"] == year)]

previous_month_df = df[df['Indx'] == filtered_df['Indx'].max()-1]
previous_month = previous_month_df.iloc[:1,:2]

pfiltered_df = previous_month_df[(df["Broker"].isin(broker))]

ordered_df = order_data_by_year_and_month(filtered_df)

# Line chart: Fee trend by month -----------------------------------------------------------------
plot_df = order_data_by_year_and_month(df[(df["Broker"].isin(broker)) & (df["Year"] == year)])
print(plot_df)
monthly_fee = plot_df.groupby("Month")["Broker Fee"].sum().reset_index()
# Sort the result based on the predefined month order
monthly_fee['Month'] = pd.Categorical(monthly_fee['Month'], categories=month_to_num, ordered=True)
monthly_fee = monthly_fee.sort_values('Month')

fig2 = px.line(monthly_fee, x="Month", y="Broker Fee", title="Sales by Month", markers=True, color_discrete_sequence=['rgb(204,102,119)'])
st.plotly_chart(fig2)

col1, col2, col3, col4 = st.columns((1,1,1,1))

# Row 2 -------------------------------------------------------------------------------------
total_loss = filtered_df["Loss"].sum()*-1
total_fee = filtered_df["Broker Fee"].sum()
gross_fee = total_fee + total_loss
previous_gross = pfiltered_df["Broker Fee"].sum() - pfiltered_df["Loss"].sum()

mom = gross_fee / previous_gross - 1

mom_perc = mom*100 if len(month) <2 else 0

# Display current month loss
col3.html('<span class="column4"></span>')
col3.metric(
    label="Loss",
    value= f"${total_loss:,.2f}"
)

# Display current month broker fee
col2.html('<span class="column4"></span>')
col2.metric(
    label="Net",
    value= f"${total_fee:,.2f}"
)

# Display current month broker fee
col4.html('<span class="column4"></span>')
col4.metric(
    label="Gross",
    value= f"${gross_fee:,.2f}",
    delta = f"{mom_perc:,.2f}%",
)
# Previous Month
col1.html('<span class="column2"></span>')
col1.metric(
    label="Previous Month",
    value= f"${previous_gross:,.2f}"
)