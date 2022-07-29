import pandas as pd
import numpy as np


# Messing about to explore the data
if __name__ == "__main__":
    file = r"C:\Users\Frederic\PycharmProjects\Solar\data\Export 5th Apr to 4th May raw data.csv"
    data = pd.read_csv(file)
    data[" Start"] = pd.to_datetime(data[" Start"])
    data[" End"] = pd.to_datetime(data[" End"])

    hist_values = np.histogram(data["Consumption (kWh)"], bins=30, range=(0, 3))

    data['day'] = data[' Start'].dt.day
    data.dropna(inplace=True)

    data.groupby([data[' Start'].dt.month, data[' Start'].dt.day])['Consumption (kWh)'].sum()
