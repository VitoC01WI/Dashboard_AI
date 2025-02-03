import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

@st.cache_data
def get_data():
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    return pd.read_csv(DATA_FILENAME)