import pandas as pd

df = pd.read_csv('data/researchers.csv')
# print(df.shape)
# print(df.head())

df = df.dropna()
df = df.drop_duplicates()

df = df[(df['h_index'] > 15) & 
(df['is_active']== True)].sort_values('joined_year', ascending=True)
print(*df['last_name'].str[0], sep=' ')