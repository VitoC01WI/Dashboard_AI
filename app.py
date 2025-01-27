import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt
from openai import OpenAI

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Streamlit App with GPT Chat Panel",
    layout="wide",
    page_icon="🤖",
)

# Create columns for layout: Main content (left) and GPT Chat Panel (right)
col1, col2 = st.columns([3, 1])  # Adjust column width ratios as needed

# GPT Chat Panel
with col2:
    st.title("🤖 GPT Chat Panel")

    st.write(
        "Upload a document below and ask a question about it – GPT will answer! "
        "You need to provide an OpenAI API key, which you can get "
        "[here](https://platform.openai.com/account/api-keys)."
    )

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

# Main Content Panel (Dashboards)
with col1:
    # GDP Dashboard
    st.title(":earth_americas: GDP Dashboard")

    @st.cache_data
    def get_gdp_data():
        DATA_FILENAME = Path(__file__).parent / "data/gdp_data.csv"
        raw_gdp_df = pd.read_csv(DATA_FILENAME)
        MIN_YEAR, MAX_YEAR = 1960, 2022
        gdp_df = raw_gdp_df.melt(
            ["Country Code"],
            [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
            "Year",
            "GDP",
        )
        gdp_df["Year"] = pd.to_numeric(gdp_df["Year"])
        return gdp_df

    gdp_df = get_gdp_data()

    st.write("Browse GDP data from the World Bank.")
    min_value, max_value = gdp_df["Year"].min(), gdp_df["Year"].max()

    from_year, to_year = st.slider(
        "Which years are you interested in?",
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value],
    )

    countries = gdp_df["Country Code"].unique()
    selected_countries = st.multiselect(
        "Which countries would you like to view?",
        countries,
        ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"],
    )

    filtered_gdp_df = gdp_df[
        (gdp_df["Country Code"].isin(selected_countries))
        & (gdp_df["Year"] <= to_year)
        & (from_year <= gdp_df["Year"])
    ]

    st.line_chart(
        filtered_gdp_df,
        x="Year",
        y="GDP",
        color="Country Code",
    )

    # Movies Dataset
    st.title("🎬 Movies Dataset")

    @st.cache_data
    def load_data():
        return pd.read_csv("data/movies_genres_summary.csv")

    df = load_data()
    genres = st.multiselect(
        "Genres",
        df.genre.unique(),
        ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
    )
    years = st.slider("Years", 1986, 2006, (2000, 2016))

    df_filtered = df[
        (df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))
    ]
    df_reshaped = df_filtered.pivot_table(
        index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
    )
    df_chart = pd.melt(
        df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
    )

    chart = (
        alt.Chart(df_chart)
        .mark_line()
        .encode(
            x=alt.X("year:N", title="Year"),
            y=alt.Y("gross:Q", title="Gross earnings ($)"),
            color="genre:N",
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)
