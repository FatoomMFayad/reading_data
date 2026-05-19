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
print(merged_researchers_pub.head)






