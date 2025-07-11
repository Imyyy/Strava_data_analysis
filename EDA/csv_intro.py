import pandas as pd

data_name = "../Data/Download_csv_11July.csv"
data = pd.read_csv(data_name)

print(data.columns)
print(data.shape)
print(data.head())

print(data.type.unique())
