import pandas as pd
import datetime

# Load in daa
data_name = "Data/Download_csv_11July.csv"
data = pd.read_csv(data_name)

# Process datetime column
data['start_date_local_dt'] = pd.to_datetime(data['start_date_local'])
data['date'] = data['start_date_local_dt'].dt.date

data['year'] = pd.DatetimeIndex(data['start_date_local_dt']).year
data['month'] = pd.DatetimeIndex(data['start_date_local_dt']).month

# Process activity metric columns
data['km'] = data['distance'] / 1000

# Activity time sort out
data['Moving_time_min'] = data['moving_time'] / 60
data['Elapsed_time_min'] = data['elapsed_time'] / 60


for col in data.columns:
    print(col)

data.to_csv("Data/Processed_data/Initial_processed.csv")