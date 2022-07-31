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


def load_excel(file):
    data = pd.read_excel(file, sheet_name="Sheet1")
    return data


def data_analysis(export_df, import_df, generation_df):
    # plotting
    # st.subheader("Plot export over time")
    # day_filter = st.sidebar.number_input("Day", 1, 31, 5)

    # plot the exported electric per hour for a given day
    # filtered_data = export_df[export_df[" Start"].dt.day == day_filter]
    # line_chart = alt.Chart(filtered_data.iloc[:, 0:2]).mark_line().encode(x=" Start:T", y="Consumption (kWh):Q")
    # st.altair_chart(line_chart)

    # plot the amount imported from the grid and exported to the grid per day over a month
    st.subheader("Daily comparison")
    # sort out daily exports
    daily_exports = export_df.groupby([export_df[' Start'].dt.month, export_df[' Start'].dt.day])['Consumption (kWh)'].sum()
    temp_df = pd.DataFrame(daily_exports)
    temp_df.rename(columns={"Consumption (kWh)": "Export (kWh)"}, inplace=True)
    daily_exports = temp_df
    # sort out daily imports
    daily_imports = import_df.groupby([export_df[' Start'].dt.month, export_df[' Start'].dt.day])['Consumption (kWh)'].sum()
    temp_df = pd.DataFrame(daily_imports)
    temp_df.rename(columns={"Consumption (kWh)": "Import (kWh)"}, inplace=True)
    daily_imports = temp_df

    # concatenate the import, export and generation data
    electric_use_df = pd.concat([daily_exports, daily_imports], axis=1)
    electric_use_df['Days generation'] = generation_df['Days generation'].values
    electric_use_df['Self use'] = electric_use_df['Days generation'] - electric_use_df['Export (kWh)']
    electric_use_df['House day total use'] = electric_use_df['Self use'] + electric_use_df['Import (kWh)']

    # change how the data is stored in the df for plotting purposes
    electric_use_df.index.rename(['Month', 'Day'], inplace=True)
    stacked = electric_use_df.stack()
    stacked_df = pd.DataFrame(stacked)
    stacked_df.index.rename(['Month', 'Day', 'Type'], inplace=True)
    stacked_df.columns = ['Value (kWh)']
    stacked_df.reset_index(inplace=True)

    st.altair_chart(alt.Chart(stacked_df).mark_bar().encode(
        x='Type:N',
        y='Value (kWh):Q',
        color='Type:N',
        column='Day:N',
        tooltip=[alt.Tooltip('Value (kWh):Q'),
                 alt.Tooltip('Type:N')]
    ))

    # st.subheader("A histogram that isn't so useful")
    # hist_values = np.histogram(export_df["Consumption (kWh)"], bins=30, range=(0, 3))
    # freqs = hist_values[0]
    # bins = hist_values[1]
    # st.bar_chart(data=freqs)

    # show data
    export_checkbox = st.checkbox("Show export data")
    if export_checkbox:
        st.write("Export data", export_df)

    import_checkbox = st.checkbox("Show import data")
    if import_checkbox:
        st.write("Import data", import_df)


export_data_file = st.file_uploader("Export data: Upload a csv")
import_data_file = st.file_uploader("Import data: Upload a csv")
days_generation_file = st.file_uploader("Upload Days Generation XSLX (Assumed to be Sheet1)")
if export_data_file and import_data_file and days_generation_file:
    export_data = load_data(export_data_file)
    import_data = load_data(import_data_file)
    generation_data = load_excel(days_generation_file)
    data_analysis(export_data, import_data, generation_data)
else:
    st.write("No file provided")


