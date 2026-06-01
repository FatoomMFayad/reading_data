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

# .idxmax() extracts the index name with the highest frequency
most_common_end = chess_df['victory_status'].value_counts().idxmax()
print(f"Most common way games end: {most_common_end}")

# Group by victory_status, calculate mean turns, and find the maximum
avg_turns_by_status = chess_df.groupby('victory_status')['turns'].mean()
highest_avg_status = avg_turns_by_status.idxmax()

print(avg_turns_by_status)
print(f"\nHighest average turns: {highest_avg_status}")

# Filter for Black wins, get the most common opening family
black_wins = chess_df[chess_df['winner'] == 'Black']
top_opening_black = black_wins['opening_family'].value_counts().idxmax()

# Filter for White wins, get the most common opening family
white_wins = chess_df[chess_df['winner'] == 'White']
top_opening_white = white_wins['opening_family'].value_counts().idxmax()

print(f"Most popular opening when Black wins: {top_opening_black}")
print(f"Most popular opening when White wins: {top_opening_white}")

# Group by 'rated' (True/False) and calculate the percentage of White wins
# We look for where winner == 'white'
white_win_rate_by_rating = chess_df.groupby('rated').apply(lambda g: (g['winner'] == 'White').mean() * 100)
print(white_win_rate_by_rating)

# 1. Define the classification function (adjust threshold boundaries if needed)
def classify_game_length(turns):
    if turns < 20:
        return 'Short'
    elif turns <= 60:
        return 'Medium'
    else:
        return 'Long'

# 2. Apply the function to create a new column
chess_df['game_length_category'] = chess_df['turns'].apply(classify_game_length)

# 3. Calculate percentages
length_percentages = chess_df['game_length_category'].value_counts(normalize=True) * 100
print(length_percentages)