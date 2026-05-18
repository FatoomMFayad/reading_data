import pandas as pd
import json
#read researchers file
df = pd.read_csv('data/researchers.csv')
#drop rows with null values 
df = df.dropna()
#drop duplicates
df = df.drop_duplicates()
#filter active is true and h_index > 15 then sort by joined_year ascending
df = df[(df['h_index'] > 15) & 
(df['is_active']== True)].sort_values('joined_year', ascending=True)
#print first letter of last names
print(*df['last_name'].str[0], sep=' ')

#read json file
with open(r'data\publications.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)
df1 = pd.json_normalize(json_data)
#drop rows with null values 
df1 = df1.dropna()
#drop duplicates
df1 = df1.drop_duplicates()
max_citations = df1['citations'].agg(['max'])
print(max_citations)



