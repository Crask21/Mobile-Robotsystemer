import pandas as pd


df = pd.read_excel('log0.xlsx', sheet_name=0)
df



data = df["Sheet1"]
print(data)
secondary_data = df["Sheet2"]

secondary_data.loc[2,0]