import pandas as pd
import os
from collections import Counter

dataset = open("Data.txt", "w+")
counter = 0
appended_data = []

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


# # Create a list of sorted seasons
# seasons_ = os.listdir('Data')
# seasons = []
# for season in seasons_:
#     if season.startswith("season"):
#         seasons.append(season)
#         season_path = os.path.join(season)
#         ds = 'Data/'+season_path
#         episodes = []
#         for episode in os.listdir(ds):
#             if episode.endswith(".txt"):
#                 episodes.append(episode)
#         episodes.sort()
#         print(episodes)
#         # print (seasons[season])
# seasons.sort()
# print(seasons)

for season in os.listdir('Data'):
    if season.startswith("season"):
        season_path = os.path.join(season)
        ds = "Data/"+season_path

        for episode in os.listdir(ds):
            if episode.endswith(".txt"):
                episode_path = os.path.join(episode)
                dse=ds+"/"+episode_path
                line_prepender(dse, "person:line")
                # print(dse)
                df = pd.read_csv(dse, sep=":", error_bad_lines=False)
                if df.shape[1] == 2:
                    df.reset_index(inplace=True)
                    df.drop(df.columns[0], axis=1, inplace=True)
                df = df.dropna()  # Drop empty values
                df.columns = ["person", "line"]
                df['episode'] = episode_path
                counter = counter+1
                df['season'] = season_path
                appended_data.append(df)
                # print(appended_data)
                continue
            else:
                continue
    continue

df = pd.concat(appended_data)
# df.sort_values(by=['season'], axis = 0, inplace = True)



# ----------- Fist DataFrame formatting----------------

df['person'] = df['person'].str.lower()
df['person'] = df['person'].str.replace('/','')
df['person'] = df['person'].str.replace(r"\(.*\)","") # Delete everything between brackets
df['person'] = df['person'].str.replace(r'^(\s*(?:\S+\s+){1})\S+',r'\1') # Delete last name
df['person'] = df['person'].str.strip() # Delete preceding space

# ----------- Second DataFrame formatting--------------

read_file = pd.read_csv(r'got_characters.txt', header= 0, error_bad_lines=False)
read_file.to_csv(r'characters.csv', index=None)

df1 = pd.read_csv('characters.csv')
df1.drop(df1.columns[0],axis = 1, inplace = True)

df1['name'] = df1['name'].str.lower()
df1['name'] = df1['name'].str.replace(r'^(\s*(?:\S+\s+){1})\S+',r'\1') # Delete last name
df1['name'] = df1['name'].str.strip() # Delete preceding space
df1.loc[(df1.name == 'khal'),'name']='khal drogo'

# print(df1)
# print(df1.name.unique())

# ---------- Merge DataFrames------------------------

merged = df1.merge(df, left_on = 'name', right_on = 'person')
merged['words'] = [len(x.split()) for x in merged['line'].tolist()]

merged['season'] = merged['season'].map(lambda x: x.lstrip('season').rstrip('aAbBcC'))
merged['episode'] = merged['episode'].str.replace(r'.txt', '')
merged['episode'] = merged['episode'].map(lambda x: x.lstrip('e').rstrip('aAbBcC'))

print(merged.head())
print(df)
merged.to_csv('Data/all_episodes.csv')