import pandas as pd
import re

df = pd.read_csv('data.csv', encoding='ISO-8859-1')

lower = []

# Clean dataset
## Delete rows with no customer ID
df = df[df['CustomerID'].notna()]
## Delete rows with no description
df = df[df['Description'].notna()]
## Delete rows with stock code that do not correspond to products
df = df[df['StockCode'].str.len() >= 5]
df = df[df['StockCode'].str.len() <= 6]
## Delete rows with prices below 0
# df = df[df['UnitPrice'] >= 0]
## Delete items corresponding to returns or other
df = df[df['Quantity'] > 0]
# Delete rows with incorrect stock codes
for idx, row in df.iterrows():
    code = row['StockCode']
    if bool(re.search(r'[a-z]+', code)):
        if code not in lower:
            lower.append(code)

df = df[~df['StockCode'].isin(lower)]
