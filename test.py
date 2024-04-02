import pandas as pd
import re

df = pd.read_csv('data.csv', encoding='ISO-8859-1')

lower = []

# Clean dataset
df = df[df['CustomerID'].notna()]
df = df[df['Description'].notna()]
df = df[df['StockCode'].str.len() >= 5]
df = df[df['StockCode'].str.len() <= 6]
df = df[df['UnitPrice'] >= 0]
df = df[df['Quantity'] > 0]

for idx, row in df.iterrows():
    code = row['StockCode']
    if bool(re.search(r'[a-z]+', code)):
        if code not in lower:
            lower.append(code)
            
df = df[~df['StockCode'].isin(lower)]



