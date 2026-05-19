import pandas as pd
import json
#read researchers file
researchers_df = pd.read_csv('data/researchers.csv')
#drop rows with null values 
researchers_df = researchers_df.dropna()
#drop duplicates
researchers_df = researchers_df.drop_duplicates()
#read json file
with open(r'data\publications.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)
pub_df = pd.json_normalize(json_data)
#drop rows with null values 
pub_df = pub_df.dropna()
#drop duplicates
pub_df = pub_df.drop_duplicates()
#function to clean funding dataframe
def clean_funding_data(df, numeric_column = 'amount_cad'):
    #make a copy of dataframe
    clean_df = df.copy()
    #change strings into zeros
    clean_df[numeric_column] = pd.to_numeric(
    clean_df[numeric_column].astype(str).str.replace('N/A','', regex=False), 
    errors='coerce'
    ).fillna(0)
    #drop rows with null values
    clean_df = clean_df.dropna(subset=[numeric_column])
    #take only positive amounts
    clean_df = clean_df[clean_df[numeric_column] > 0]

    return clean_df

#load the excel file
funding_df = pd.read_excel('data/funding.xlsx')
funding_df = clean_funding_data(funding_df, 'amount_cad')
#merge the three data frames and keep only the matching researchers
merged_researchers_pub = pd.merge(
researchers_df,
pub_df,
on='researcher_id',
how='inner' 
).merge(
    funding_df,
    on='researcher_id',
    how='inner' 
)
highest_citations_sum = merged_researchers_pub.groupby('researcher_id')['citations'].sum()
highest_citations_author_id = highest_citations_sum.idxmax()
#get the author row of the most cited paper
author_row = merged_researchers_pub[merged_researchers_pub['researcher_id'] == highest_citations_author_id]
#get the author first name of the most cited paper
author_first_name =author_row['first_name'].values[0]
#get the author last name of the most cited paper
author_last_name = author_row['last_name'].values[0]
# concat the author first name and last name
author_name = f"{author_first_name} {author_last_name}"
print(author_name)
#field received the most total funding
highest_total_funding = merged_researchers_pub.groupby('field')['amount_cad'].sum()
highest_total_funding_id = highest_total_funding.idxmax()
print(highest_total_funding_id)
#joined first and still active
first_active_joined = merged_researchers_pub[(merged_researchers_pub['is_active']== True)].sort_values('joined_year', ascending=True)
full_name = f"{first_active_joined.iloc[0]['first_name']} {first_active_joined.iloc[0]['last_name']}"
join_year = first_active_joined.iloc[0]['joined_year']
print(f"{full_name} joined {join_year}")

merged_researchers_pub.to_csv('data/my_merged_files.csv', index=False)




