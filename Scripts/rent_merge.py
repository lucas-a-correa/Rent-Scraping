import pandas as pd

df1 = pd.read_csv(r".\rent_clean.csv",encoding='UTF-8')
df2 = pd.read_csv(r".\rent_12_Jan_clean.csv",encoding='UTF-8')

rent_df = pd.concat([df1,df2])

rent_df = rent_df.drop_duplicates()

rent_df.to_csv(r".\rent_merged_12_Jan.csv", index=False, encoding="UTF-8")