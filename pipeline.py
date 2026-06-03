import pandas as pd
import os
chess_url = 'https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view'
chess_url='https://drive.google.com/uc?id=' + chess_url.split('/')[-2]
players_registry_url = 'https://drive.google.com/file/d/1wCSAkGagMzWiToedLC3ZGo_lGf_laF-k/view'
players_registry_url='https://drive.google.com/uc?id=' + players_registry_url.split('/')[-2]
def load_data(url: str, local_path: str)-> pd.DataFrame:
    if os.path.exists(local_path):
        print(f'Loading from cache: {local_path}')
        return pd.read_csv(local_path)
    print(f'Downloading from {url}...')
    df = pd.read_csv(url)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path, index=False)
    print(f'Saved to {local_path}')
    return df

# Stage 1 loading and exploring data
chess_df = load_data(chess_url, 'data/raw/chess_games.csv')
players_df = load_data(players_registry_url, 'data/raw/players_registry.csv')

print(f'Number of records is : {len(chess_df)}')
print(f'Number of duplicated records is : {chess_df.duplicated().sum()}')
print(f"Number of games having duplicate moves sequences is : {chess_df.duplicated(subset=['moves']).sum()}")
print(f"% of missing opening : {chess_df['opening_response'].isnull().mean() * 100}")
print(chess_df['opening_variation'].isnull().mean() * 100)
print(chess_df['turns'].min())

# stage 2 build clean_chess

#parse time_increment
chess_df[['time_base', 'time_inc']] = chess_df['time_increment'].str.split('+', expand=True).astype(int)

#Add rating_diff
chess_df['rating_diff'] = chess_df['white_rating'] - chess_df['black_rating']

#Extract opening_family
chess_df['opening_family'] = chess_df['opening_fullname'].str.split(':').str[0].str.strip()

#Drop high-null cloumn
chess_df = chess_df.drop(columns=['opening_response'])

#Flag short games
chess_df['is_suspicious'] = chess_df['turns'] < 5

#validate
assert chess_df['rating_diff'].notna().all()
assert chess_df.duplicated().sum() == 0

# Stage 3 
#win rate for White, Black, and Draw 
win_rates = chess_df['winner'].value_counts(normalize=True) * 100
print(win_rates)
#validate
assert win_rates.sum() == 100

# .idxmax() extracts the index name with the highest frequency
victory_proportions = chess_df['victory_status'].value_counts(normalize=True)
most_common_end = victory_proportions.idxmax()
most_common_pct = victory_proportions.max() * 100
print(f"Most common way games end: {most_common_end} ({most_common_pct:.1f}%)")

# Group by victory_status, calculate mean turns, and find the maximum
avg_turns_by_status = chess_df.groupby('victory_status')['turns'].mean()
highest_avg_status = avg_turns_by_status.idxmax()

print(avg_turns_by_status)
print(f"\nHighest average turns: {highest_avg_status}, {avg_turns_by_status['Draw']:.1f}%")

# Filter for Black wins, get the most common opening family

black_wins = chess_df[chess_df['winner'] == 'Black']
black_opening_counts = black_wins['opening_family'].value_counts()

# Get the name and the count
top_opening_black = black_opening_counts.idxmax()
top_opening_black_count = black_opening_counts.max()

# Filter for White wins, get the most common opening family
white_wins = chess_df[chess_df['winner'] == 'White']
white_opening_counts = white_wins['opening_family'].value_counts()
top_opening_white = white_opening_counts.idxmax()
top_opening_white_count = white_opening_counts.max()

print(f"Most popular opening when Black wins: {top_opening_black}, {top_opening_black_count}")
print(f"Most popular opening when White wins: {top_opening_white}, {top_opening_white_count}")

# Group by 'rated' (True/False) and calculate the percentage of White wins
# We look for where winner == 'white'
white_win_rate_by_rating = (chess_df['winner'] == 'White').groupby(chess_df['rated']).mean() * 100
white_win_rate_by_rating = white_win_rate_by_rating.round(2)
print(white_win_rate_by_rating)

# 1. Define the classification function (adjust threshold boundaries if needed)
chess_df['game_length'] = pd.cut(
    chess_df['turns'],
    bins=[0, 15, 70, 150], 
    labels=['Short', 'Medium', 'Long']
)

# Calculate the percentages for these specific buckets
length_percentages = chess_df['game_length'].value_counts(normalize=True) * 100
print(length_percentages.round(2))

#stage 4
#merge white player data with registry
merged = pd.merge(
    chess_df[['game_id', 'white_id', 'white_rating', 'winner']],
    players_df.rename(columns={'username': 'white_id'}),
    on='white_id', how='left')
#white players that have no registry entry
unique_missing_players = chess_df.loc[~chess_df['white_id'].isin(players_df['username']), 'white_id'].nunique()
print(f"Unique missing players: {unique_missing_players}")

#Standardize inconsistent country names
country_map = {'RUS': 'Russia', 'russian federation': 'Russia',
               'US': 'United States', 'USA':'United States', 'united states' : 'United States',
               'UA':'Ukraine', 'GB':'United Kingdom', 'united kingdom':'United Kingdom', 'UK' :'United Kingdom',
               'Deutschland':'Germany','DE':'Germany', 'ES':'Spain',
               'FR': 'France', 'france':'France', 'IN':'India', 'india':'India',
               'PL':'Poland', 'poland':'Poland','BRA':'Brazil', 'brazil':'Brazil'}

merged['country'] = merged['country'].map(country_map).fillna(merged['country'])

unique_country_strings = merged['country'].nunique()
print(f"Total unique country strings: {unique_country_strings}")

#Plot: bar chart of win counts by color. Save to output/wins_by_color.png
# Create the plot using pandas and assign it to 'ax'
ax = merged['winner'].value_counts().plot(
    kind='bar', 
    title='Wins by Color',
    color=['#C9A84C', '#1B3A2D', '#7A8C7E'],
    rot=0
)

# Add the value labels on top of the containers (the bars)
ax.bar_label(ax.containers[0], padding=3)

# Save the figure to PNG
ax.get_figure().savefig('plots/wins_by_color.png', bbox_inches='tight', dpi=300)

#Plot: scatter of white_rating vs turns for rated games
scatter_ax = chess_df.plot(
    kind='scatter', 
    x ='white_rating', y ='turns',
    alpha=0.3, title='Rating vs Game Length',
    color="#11B6E8")  
   
# Save the figure to PNG
scatter_ax.get_figure().savefig('plots/rating_vs_game_length.png', bbox_inches='tight', dpi=300)
