import pandas as pd
df_1= pd.read_csv("dataset_final_madura.csv")
df_2= pd.read_csv("data kabar madura.csv")

df_combine = pd.concat([df_1,df_2],ignore_index= True)

df_combine.to_csv("Full Data berita madura.csv", index=False)