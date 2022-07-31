import pandas as pd
import numpy as np
import altair as alt


# Messing about to explore the data
if __name__ == "__main__":
    file = r"C:\Users\Frederic\PycharmProjects\Solar\data\Export 5th Apr to 4th May raw data.csv"
    import_file = r"C:\Users\Frederic\PycharmProjects\Solar\data\Imported 5th Apr to 4th may raw data.csv"
    data = pd.read_csv(file)
    import_data = pd.read_csv(import_file)
    data[" Start"] = pd.to_datetime(data[" Start"])
    data[" End"] = pd.to_datetime(data[" End"])

    generation_file = r"C:\Users\Frederic\PycharmProjects\Solar\data\DaysGeneration.xlsx"
    generation_df = pd.read_excel(generation_file, sheet_name="Sheet1")

    hist_values = np.histogram(data["Consumption (kWh)"], bins=30, range=(0, 3))

    data['day'] = data[' Start'].dt.day
    data.dropna(inplace=True)

    export_series = data.groupby([data[' Start'].dt.month, data[' Start'].dt.day])['Consumption (kWh)'].sum()
    import_series = import_data.groupby([data[' Start'].dt.month, data[' Start'].dt.day])['Consumption (kWh)'].sum()

    temp_df = pd.DataFrame(export_series)
    temp_df.rename(columns={"Consumption (kWh)": "Export (kWh)"}, inplace=True)
    t = pd.concat([temp_df, import_series], axis=1)
    t.rename(columns={"Consumption (kWh)": "Import (kWh)"}, inplace=True)

    # add in days generation
    t['Days generation'] = generation_df['Days generation'].values
    t['Self use'] = t['Days generation'] - t['Export (kWh)']
    t['House day total use'] = t['Self use'] + t['Import (kWh)']

    t.index.rename(['Month', 'Day'], inplace=True)
    st = t.stack()
    dfst = pd.DataFrame(st)
    dfst.columns = ['Value (kWh)']
    dfst.index.rename(['Month', 'Day', 'Type'], inplace=True)
    dfst.reset_index(inplace=True)
    gp_chart = alt.Chart(dfst).mark_bar().encode(alt.Column('Day'), alt.X('Type'), alt.Y('Value (kWh)'),
                                                 alt.Color('Type'))
    gp_chart.display()
    # t.plot.bar(title="A title", color={"blue", "red"})
