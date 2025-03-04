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

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Interactive Dashboards with GPT Chat",
    layout="wide",
    #page_icon="🤖",
)

# date time header
st.markdown(f"**Today:** {datetime.now().strftime('%d %B %Y, %I:%M%p')}", unsafe_allow_html=True)

# formating layout
comp.metric_row()

# load data
df = fnc.get_data()

#dummy data
time_data = pd.DataFrame({"Time": ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"]
                          , "Waiting Time": [2, 3, 2, 3, 4, 5, 7, 6, 5, 9, 12, 14, 10, 5, 3]})
sales_data = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
                           , "Sales": [300000, 350000, 400000, 380000, 370000, 250000, 200000, 180000, 150000]})
customer_data = pd.DataFrame({"Time": ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"]
                              , "Customers": [5, 7, 10, 15, 20, 25, 35, 40, 50, 70, 100, 120, 80, 40, 20]})
product_data = pd.DataFrame({
        "Items": ["Banana", "Milk", "Chocolate", "Cheese"],
        "Apr 2024": [6000, 9300, 4600, 9500],
        "May 2024": [6200, 9200, 4500, 9700],
        "Sales Target May 2024": [6000, 10000, 4800, 9500]
    })

#row 2
c1, c2 = st.columns([3,2])#use list for ratio
with c1.container(height=260):
    st.markdown("Waiting time (in min) at cash desk")
    st.bar_chart(time_data, x="Time", y="Waiting Time", height = 220)   
    #fig, ax = plt.subplots(figsize=(10, 4))  # Define aspect ratio
    #ax.bar(time_data["Time"], time_data["Waiting Time"])
    #ax.set_xlabel("Time")
    #ax.set_ylabel("Waiting Time (min)")
    #st.pyplot(fig)
with c2.container(height=260):
    st.markdown("Product Sales and Forecast")
    st.line_chart(sales_data, x="Month", y="Sales", height = 220)
    #fig, ax = plt.subplots() 
    #ax.plot(sales_data["Month"], sales_data["Sales"], marker='o')
    #ax.set_xlabel("Month")
    #ax.set_ylabel("Sales (€)")
    #st.pyplot(fig)

#row 3

c3, c4 = st.columns([3,2])
with c3.container(height=260):
    st.markdown("Customers per Day")
    st.bar_chart(customer_data, x="Time", y="Customers", height = 220)
    #fig, ax = plt.subplots(figsize=(10, 4))  # Define aspect ratio
    #ax.bar(customer_data["Time"], customer_data["Customers"])
    #ax.set_xlabel("Time")
    #ax.set_ylabel("Customers")
    #st.pyplot(fig)

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

#st.write(
#    "Upload a document below and ask a question about it – GPT will answer! "
#    "You need to provide an OpenAI API key, which you can get "
#    "[here](https://platform.openai.com/account/api-keys)."
#)

# Ask for OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # File uploader for document
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Text area for user's question
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
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