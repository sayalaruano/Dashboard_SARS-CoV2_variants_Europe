# Imports
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from millify import prettify

# Attach customized ccs style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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

# Create streamlit app

st.header('Dashboard of weekly reports of SARS-CoV2 variants in European countries from 2020 until now')

st.subheader('by [Sebastián Ayala-Ruano](https://sayalaruano.github.io/)')

st.sidebar.header('About')

st.sidebar.write('A project created for the [30DaysOfStreamlit](https://share.streamlit.io/streamlit/30days) challenge.')

st.sidebar.header('How it works?')

st.sidebar.write('Select a country in the sidebar, and a year and week in the the main page to show the data of SARS-CoV2 variants.')

country = st.sidebar.selectbox('Country:', df["country"].unique())

# Filter data of the selected country
df_covid = df[df["country"] == country]

# Create donut plots of Sars-CoV2 variant distribution in european countries
donut_plots= {}

for j in df["year_week"].unique():
    df_temp = df_covid[(df_covid["year_week"] ==j) & (df_covid["source"] =="GISAID")]
    plot_temp = go.Figure(data=[go.Pie(labels=df_temp["variant"], 
    values=df_temp["percent_variant"], hole=.4)])
    donut_plots[j] = plot_temp
    
# Create bar plots of the number of detections of Sars-CoV2 variants in european countries
bar_plots = {}

for j in df["year_week"].unique():
    df_temp = df_covid[(df_covid["year_week"] ==j) & (df_covid["source"] =="GISAID")]
    plot_temp = px.bar(df_temp, y='number_detections_variant', x='variant',
            text_auto='.2s', labels={
                    "number_detections_variant": "Number of detections",
                    "variant": "Variant"
                })
    plot_temp.update_traces(textfont_size=12, textangle=0, textposition="outside", showlegend=False)
    bar_plots[j] = plot_temp

st.sidebar.write('**Note:** If no plots are displayed, it means that there are no data for those weeks.')

st.sidebar.header('Data')

st.sidebar.write('The entire dataset is available [here](https://www.ecdc.europa.eu/en/publications-data/data-virus-variants-covid-19-eueea). I only considered information from the [GISAID](https://www.gisaid.org/) database.')

st.sidebar.header('Code availability')

st.sidebar.write('The code for this project is available under the [MIT License](https://mit-license.org/) in this [GitHub repo](https://github.com/sayalaruano/Dashboard_SARS-CoV2_variants_Europe). If you use or modify the source code of this project, please provide the proper attributions for this work.')

st.sidebar.header('Contact')

st.sidebar.write('If you have comments or suggestions about this work, please DM by [twitter](https://twitter.com/sayalaruano) or [create an issue](https://github.com/sayalaruano/Dashboard_SARS-CoV2_variants_Europe/issues/new) in the GitHub repository of this project.')

year = st.selectbox('Year:', df["year"].unique())

week = st.slider('Choose a week', 1, 53, 9)

for i in df["year"].unique():
    for j in df["week"].unique():
        if (year == i) & (week == j):
            if j in range(1,10):
                year_week = i+'-'+'0'+str(j)
            else:
                year_week = i+'-'+str(j)

            if year_week in df["year_week"].unique():
                new_cases = df_covid[df_covid["year_week"] == year_week].iloc[1]['new_cases']
                seq_cases = df_covid[df_covid["year_week"] == year_week].iloc[1]['number_sequenced']
                perc_seq_cases = df_covid[df_covid["year_week"] == year_week].iloc[1]['percent_cases_sequenced']

                col1, col2, col3 = st.columns(3)
                col1.metric("New COVID-19 cases", prettify(new_cases))
                col2.metric("Sequenced COVID-19 cases", prettify(seq_cases))
                col3.metric("% of COVID-19 sequenced cases", str(perc_seq_cases)+"%")
            else: 
                st.write("No data available")
            st.markdown("#### **Variant distribution**")
            if year_week in donut_plots:
                donut_plot = donut_plots[year_week]
                st.plotly_chart(donut_plot)
            else:
                st.write("No data available")
            st.markdown("#### **Number of variants**")
            if year_week in bar_plots:
                bar_plot = bar_plots[year_week]
                st.plotly_chart(bar_plot)
            else: 
                st.write("No data available")
