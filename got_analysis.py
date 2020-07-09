import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib
from matplotlib.font_manager import FontProperties
import squarify  

df = pd.read_csv("Data/all_episodes.csv")
df.rename(columns = {' s': 'sex'}, inplace=True)
print(df.columns)
df['line'] = df['line'].map(lambda x: x.lstrip('ser').rstrip('aAbBcC')) # Get rid of a set of characters 
df['line'] = df['line'].str.replace(',','')
df['line'] = df['line'].str.replace('.','')

df.drop(df.columns[0], axis=1, inplace=True)
df['color'] = ""
df.loc[(df.sex == ' f'), 'color'] = 'red'
df.loc[(df.sex == ' m'), 'color'] = 'blue'


# ----------------- per name tree map ----------------------
df2 = df.groupby(['name', 'sex', 'color'])['words'].sum().reset_index()

x1 = pd.Series(df2['name'])
x2 = pd.Series(df2['words'])
x3 = pd.Series(df2['color'])

x2 = x2.tolist()
x1 = x1.tolist()
x3 = x3.tolist()

# squarify.plot(sizes=x2, label=x1, color =x3,alpha=.7,bar_kwargs=dict(linewidth=1, edgecolor="#000033") )
# plt.axis('off')
# plt.show()

# ----------------- per season stacked bar chart ---------------
df3 = df.groupby(['season', 'name', 'sex'])['words'].sum().reset_index(name = 'words_qt')
fig = px.bar(df3,
             x = 'season',
             y = 'words_qt',
             color = 'sex',
             barmode = 'stack')

fig.show()

# --------------- per name wordcloud -----------------------
df4 = df[df['name'] == 'arya']

word = ''

