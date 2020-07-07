import pandas as pd
import numpy as np
import regex as re
from collections import Counter

# Read the CSV file and split it by the separator ":"
df = pd.read_csv("e1.txt", sep = ":",names=['name','line'], error_bad_lines = False)

# Delete all the rows containing Nan cells 
df = df.dropna()

# Make all words lowercase
df['name'] = df['name'].str.lower()
df['line'] = df['line'].str.lower()

# repalce "," and "." by ""
df['line'] = df['line'].str.replace(',','')
df['line'] = df['line'].str.replace('.','')

# Delete everything between the brackets
df['line'] = df['line'].str.replace(r"\(.*\)","")
df['name'] = df['name'].str.replace(r"\(.*\)","")
# delete last name
df['name']=df['name'].str.replace(r"^(\s*(?:\S+\s+){1})\S+",r"\1")

# Delete preceding spaces
df['name'] = df['name'].str.strip()

# Count exclamation marks to show strong emotions
df['exc'] = df['line'].map(lambda x: x.count("!"))
# Count number of words in a line
df['nbr_words'] = [len(x.split()) for x in df['line'].tolist()]
# Count number of characters in a line
df['nbr_char'] = df.line.apply(len)

# Count the most repeated words
# wd = pd.DataFrame(Counter(nbr_words.split()).most_common(200), columns = ['word', 'frequency'])
print(df.groupby('name').mean().sort_values('nbr_char').round(2))
print(df.head())
