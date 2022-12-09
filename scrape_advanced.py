# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# %%
# get list of urls for players stats
players_url = 'https://www.basketball-reference.com/players/'
r = requests.get(players_url)
bs = BeautifulSoup(r.text)
r.ok

# %%
# get all last name directory links
    # links found in 'ul' tag with 'page_index' class
    # directory links will have a text with length 1 (e.g. "A")
    # base url must be added to directory path
letter_links = bs.find('ul', {'class': 'page_index'}).find_all('a')
letter_links = ['https://www.basketball-reference.com' + link.get('href') for link in letter_links if len(link.text) == 1]
print(len(letter_links))

# %%
# get all player links from last name directory links

# initialize empty list of player links
player_links = []

# player links found in 'th' tag w/specific scope and class
# active players with 'strong' tag
# add base url
for letter_link in letter_links:
    time.sleep(2)
    r = requests.get(letter_link)
    bs = BeautifulSoup(r.text)
    player_tags = bs.find('tbody').find_all('th', {'scope': 'row', 'class': 'left'})
    player_links += ['https://www.basketball-reference.com' + player_tag.find('a').get('href') for player_tag in player_tags]

print(len(player_links))

# %%
# build dataframe of all players' advanced stats by season

# initialize empty list to which dfs will be appended
appended_data = []

for i, player_link in enumerate(player_links):

    time.sleep(1)
    print(i)

    # get tables from player page
    dfs = pd.read_html(player_link)

    # loop through dfs
    # if 'BPM' column is in table, append df to appended_data
    for df in dfs:
        if 'BPM' in df.columns:
            # add url link as col to identify player
            df['url'] = player_link
            appended_data.append(df)

# %%
# combine all dfs together
nba = pd.concat(appended_data)

# %%
# drop all rows where Age is NaN (these are not specific years, could be career or specific team average)
nba = nba.dropna(subset=['Age'])

# reset index
nba = nba.reset_index(drop=True)

# %%
print(nba['url'].nunique())

# %%
nba.to_csv('nba_advanced.csv')
print('Complete!')

# %%



