# Imports
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Function to load data of Sars-CoV2 variants in Europe
@st.cache
def load_data():
    df_covid = pd.read_csv("data.csv")

    # Add common names of variants 
    df_covid.loc[(df_covid["variant"] =="B.1.1.529"), "variant"] = "B.1.1.529 - Omicron"
    df_covid.loc[(df_covid["variant"] =="B.1.351"), "variant"] = "B.1.351 - Beta"
    df_covid.loc[(df_covid["variant"] =="B.1.617.2"), "variant"] = "B.1.617.2 - Delta"
    df_covid.loc[(df_covid["variant"] =="P.1"), "variant"] = "P.1 - Gamma"
    df_covid.loc[(df_covid["variant"] =="B.1.1.7"), "variant"] = "B.1.1.7 - Alpha"
    df_covid.loc[(df_covid["variant"] =="B.1.525"), "variant"] = "B.1.525 - Eta"
    df_covid.loc[(df_covid["variant"] =="B.1.617.1"), "variant"] = "B.1.617.1 - Kappa"
    df_covid.loc[(df_covid["variant"] =="B.1.621"), "variant"] = "B.1.621 - Mu"
    df_covid.loc[(df_covid["variant"] =="C.37"), "variant"] = "C.37 - Lambda"
    df_covid.loc[(df_covid["variant"] =="B.1.427/B.1.429"), "variant"] = "B.1.427/B.1.429 - Epsilon"
    df_covid.loc[(df_covid["variant"] =="UNK"), "variant"] = "Unknown"

    # Separate year_week column into two columns 
    df_covid[['year', 'week']] = df_covid["year_week"].str.split('-', 1, expand=True)

    # Convert week column data type into integer 
    df_covid["week"] = df_covid["week"].astype(int)

    return df_covid

# Load data
df = load_data()



# Filter data of Germany
df_covid_ger = df[df["country"] == "Germany"]

# Create donut plots of Sars-CoV2 variant distribution in european countries
donut_plots= {}

for j in df["year_week"].unique():
    df_temp = df_covid_ger[(df_covid_ger["year_week"] ==j) & (df_covid_ger["source"] =="GISAID")]
    plot_temp = go.Figure(data=[go.Pie(labels=df_temp["variant"], 
    values=df_temp["percent_variant"], hole=.4)])
    donut_plots[j] = plot_temp
    

# Create bar plots of the number of detections of Sars-CoV2 variants in european countries
bar_plots = {}

for j in df["year_week"].unique():
    df_temp = df_covid_ger[(df_covid_ger["year_week"] ==j) & (df_covid_ger["source"] =="GISAID")]
    plot_temp = px.bar(df_temp, y='number_detections_variant', x='variant',
            text_auto='.2s', labels={
                    "number_detections_variant": "Number of detections",
                    "variant": "Variant"
                })
    plot_temp.update_traces(textfont_size=12, textangle=0, textposition="outside", showlegend=False)
    bar_plots[j] = plot_temp

# Create streamlit app

st.header('Dashboard of weekly reports of SARS-CoV2 variants in Germany from 2020 until now')

st.subheader('by [Sebasti??n Ayala-Ruano](https://sayalaruano.github.io/)')

st.sidebar.header('About')

st.sidebar.write('I created this project as part of the [30DaysOfStreamlit](https://share.streamlit.io/streamlit/30days) challenge.')

st.sidebar.header('How it works?')

st.sidebar.write('Select a year in the sidebar and a week in the slidebar of the main page to show the data of SARS-CoV2 variants of that date.')

year = st.sidebar.selectbox('Year:', df["year"].unique())

st.sidebar.write('**Note:** If no plots are displayed, it means that there are no data on those weeks.')

st.sidebar.header('Data')

st.sidebar.write('The entire dataset is available [here](https://www.ecdc.europa.eu/en/publications-data/data-virus-variants-covid-19-eueea). I only considered the data from the [GISAID](https://www.gisaid.org/) database.')

st.sidebar.header('Contact')

st.sidebar.write('If you have comments or suggestions about this work, please DM by [twitter](https://twitter.com/sayalaruano) or [create an issue](https://github.com/sayalaruano/Dashboard_SARS-CoV2_variants_Europe/issues/new) in the GitHub repository of this project.')

week = st.slider('Choose a week', 1, 53, 5)

for i in df["year"].unique():
    for j in df["week"].unique():
        if (year == i) & (week == j):
            if j in range(1,10):
                year_week = i+'-'+'0'+str(j)
            else:
                year_week = i+'-'+str(j)
            st.write(year_week)
            st.markdown("**Variant distribution**")
            if year_week in donut_plots:
                donut_plot = donut_plots[year_week]
                st.plotly_chart(donut_plot)
            else:
                st.write("No data available")
            st.markdown("**Number of variants**")
            if year_week in bar_plots:
                bar_plot = bar_plots[year_week]
                st.plotly_chart(bar_plot)
            else: 
                st.write("No data available")
