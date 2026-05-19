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
#get the id of the most cited paper
max_citations_idx = df1['citations'].idxmax()
#get the title of the most cited paper
highest_citations_title = df1.loc[max_citations_idx, 'title']
#get the author id of the most cited paper
highest_citations_author_id = df1.loc[max_citations_idx, 'researcher_id']
#get the author row of the most cited paper
author_row = df[df['researcher_id'] == highest_citations_author_id]
#get the author first name of the most cited paper
author_first_name =author_row['first_name'].values[0]
#get the author last name of the most cited paper
author_last_name = author_row['last_name'].values[0]
# concat the author first name and last name
author_name = f"{author_first_name} {author_last_name}"
#print the title and the author of the most cited paper
print(f"The most cited paper is {highest_citations_title} written by {author_name}")



