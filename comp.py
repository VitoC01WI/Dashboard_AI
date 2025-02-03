import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

def metric_row():
    col1, col2, col3 = st.columns(3)
    col1.metric("1 more lane reduces waiting time at cash desk by", "4 min")
    col2.metric("Free colleagues for cash desk", "2")
    col3.metric("Opened cash desks", "2 of 5")