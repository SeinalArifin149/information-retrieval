import pandas as pd

df = pd.read_csv("dataset_kabar_madura.csv")

df ['sumber'] = ""

i = 0

while i < len(df):
    df.at[i,'sumber'] = "kabar madura"
    i += 1

df.to_csv("data kabar madura.csv",index=False)
print (df.head())