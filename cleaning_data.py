import pandas as pd

df = pd.read_csv('data/researchers.csv',
                 sep=";", #different delimiter
                 encoding="utf-8",
                 skiprows=1)
print(df.shape)
print('********')
print(df.head())
print('********')
print(df.describe())
print('********')
print(df.isnull().sum())
