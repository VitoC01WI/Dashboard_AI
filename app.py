import streamlit as st
import pandas as pd
import math
import altair as alt
import matplotlib.pyplot as plt
from openai import OpenAI
from pathlib import Path
from datetime import datetime
import comp
import functool as fnc
import numpy as np

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Interactive Dashboards with GPT Chat",
    layout="wide",
)

# date time header
#this code will get the actual time
#st.markdown(f"**Today:** {datetime.now().strftime('%d %B %Y, %I:%M%p')}", unsafe_allow_html=True)
#dummy time
st.markdown(f"**Today: 30 May 2024, 6:15pm**", unsafe_allow_html=True)
# making the top row of metrics
comp.metric_row()

# load data
#df = fnc.get_data(data_filename="movies.csv")

#dummy data
time_data = pd.DataFrame({
    "Time": ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"],
    "Average waiting time": [1,2,2,4,3,6,6,6,10,11,14,0,0,0,0],
    "Forecas": [0,0,0,0,0,0,0,0,0,0,0,13,15,6,3]
})
#this code will sort the time in order, if x axis is numerical, this should not be necessary
time_order = ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"]
time_data["Time"] = pd.Categorical(time_data["Time"], categories=time_order, ordered=True)
time_data = time_data.sort_values("Time")

sales_data = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
                           "Sales 2024": [280.000, 350.000, 370.000, 400.000, np.nan, np.nan, np.nan, np.nan, np.nan],
                           "Sales forecast 2024": [np.nan, np.nan, np.nan, 400.000, 350.000, 330.000, 220.000, 250.000, 320.000]
                           })
time_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
sales_data["Month"] = pd.Categorical(sales_data["Month"], categories=time_order, ordered=True)
sales_data = sales_data.sort_values("Month")

customer_data = pd.DataFrame({"Time": ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"]
                              , "# customers": [10,12,17,30,23,40,39,40,70,80,100,0,0,0,0]
                              , "Forecast": [0,0,0,0,0,0,0,0,0,0,0,90,30,20,15]
                              })
time_order = ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"]
customer_data["Time"] = pd.Categorical(customer_data["Time"], categories=time_order, ordered=True)
customer_data = customer_data.sort_values("Time")

product_data = pd.DataFrame({
        "Items": ["Banana", "Milk", "Chocolate", "Cheese"],
        "Apr 2024": [6000, 9300, 4600, 9500],
        "May 2024": [6200, 9200, 4500, 9700],
        "Sales Target May 2024": [6000, 10000, 4800, 9500]
    })
target_waiting_time = 6

#row 2
c1, c2 = st.columns([3,2])#use list for ratio, 3,2 will make 2 columns with ratio 3:2
with c1.container(height=260):
    st.markdown("Waiting time (in min) at cash desk")
    st.bar_chart(time_data,x='Time', height = 220)   

with c2.container(height=260):
    st.markdown("Product Sales and Forecast")
    st.line_chart(sales_data, x="Month", height = 220)


#row 3
c3, c4 = st.columns([3,2])
with c3.container(height=260):
    st.markdown("Customers per Day")
    st.bar_chart(customer_data, x="Time", height = 220,color = ["#1f77b4", "#ff7f0e"])


with c4.container(height=260):
    st.markdown("Product Variation List")
    st.dataframe(product_data, height = 220)

#template leftover
#    @st.cache_data
#    def get_gdp_data():
#        DATA_FILENAME = Path(__file__).parent / "data/gdp_data.csv"
#        raw_gdp_df = pd.read_csv(DATA_FILENAME)
#        MIN_YEAR, MAX_YEAR = 1960, 2022
#        gdp_df = raw_gdp_df.melt(
#            ["Country Code"],
#            [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
#            "Year",
#            "GDP",
#        )
#        gdp_df["Year"] = pd.to_numeric(gdp_df["Year"])
#        return gdp_df

#    gdp_df = get_gdp_data()

#    min_value, max_value = gdp_df["Year"].min(), gdp_df["Year"].max()

#    from_year, to_year = st.slider(
#        "Which years are you interested in?",
#        min_value=min_value,
#        max_value=max_value,
#        value=[min_value, max_value],
#    )

#    countries = gdp_df["Country Code"].unique()
#    selected_countries = st.multiselect(
#        "Which countries would you like to view?",
#        countries,
#        ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"],
#    )

#    filtered_gdp_df = gdp_df[
#        (gdp_df["Country Code"].isin(selected_countries))
#        & (gdp_df["Year"] <= to_year)
#        & (from_year <= gdp_df["Year"])
#    ]

#    st.line_chart(
#        filtered_gdp_df,
#        x="Year",
#        y="GDP",
#        color="Country Code",
#    )

#   genres = st.multiselect(
#        "Genres",
#        df.genre.unique(),
#        ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
#    )
#    years = st.slider("Years", 1986, 2006, (2000, 2016))

#    df_filtered = df[
#        (df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))
#    ]
#    df_reshaped = df_filtered.pivot_table(
#        index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
#    )
#    df_chart = pd.melt(
#        df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
#    )

#    chart = (
#        alt.Chart(df_chart)
#        .mark_line()
#        .encode(
#            x=alt.X("year:N", title="Year"),
#            y=alt.Y("gross:Q", title="Gross earnings ($)"),
#            color="genre:N",
#        )
#        .properties(height=320)
#    )
#    st.altair_chart(chart, use_container_width=True)

# AI Recommender Section
st.markdown("GPT Chat Recommender")


# import API key from secrets
openai_api_key = st.secrets["api_key"]

client = OpenAI(api_key=openai_api_key)

# File uploader for document
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

# Text area for user's question
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    #disabled=not uploaded_file,
)

if question:
    customer_data_csv=customer_data.to_csv(index=False)
    time_data_csv=time_data.to_csv(index=False)
    sales_data_csv=sales_data.to_csv(index=False)
    product_data_csv=product_data.to_csv(index=False)
    #you may need to modify the message to guide how chatgpt will analyse the data
    messages = [
        {
            "role": "user",
            "content": f"Here's 4 csv tables: {customer_data_csv},{time_data_csv},{sales_data_csv},{product_data_csv} \n\n---\n\n {question}",
        }
    ]

    # Generate an answer using the OpenAI API
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    # Display streamed response
    st.write("**Answer:**")
    for response in stream:
        st.write(response.choices[0].delta.content, end="")