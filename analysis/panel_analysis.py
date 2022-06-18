import numpy as np
import streamlit as st
import pandas as pd
import altair as alt

"""
# Solar Panel analysis
This page allows basic plotting of generated electric from panels and exported electric to the grid.
"""


def load_data(file):
    # file = r"C:\Users\Frederic\PycharmProjects\Solar\data\Export 5th Apr to 4th May raw data.csv"
    data = pd.read_csv(file)
    data[" Start"] = pd.to_datetime(data[" Start"])
    data[" End"] = pd.to_datetime(data[" End"])
    data = data[[" Start", "Consumption (kWh)", " End"]]
    return data


def data_analysis(data):
    # plotting
    st.subheader("Plot export over time")
    day_filter = st.sidebar.number_input("Day", 1, 31, 5)

    filtered_data = data[data[" Start"].dt.day == day_filter]
    chart = alt.Chart(filtered_data.iloc[:, 0:2]).mark_line().encode(x=" Start:T", y="Consumption (kWh)")
    st.altair_chart(chart)

    st.subheader("A histogram that isn't so useful")
    hist_values = np.histogram(data["Consumption (kWh)"], bins=30, range=(0, 3))
    freqs = hist_values[0]
    bins = hist_values[1]
    st.bar_chart(freqs)

    # show data
    export_checkbox = st.checkbox("Show export data")
    if export_checkbox:
        st.write("Export data", data)


file = st.file_uploader("Upload a csv")
if file:
    export_data = load_data(file)
    data_analysis(export_data)
else:
    st.write("No file provided")


