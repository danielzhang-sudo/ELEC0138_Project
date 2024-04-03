import pandas as pd
import re

def clean_data(args):
	path = args.path
	path = 'data.csv' # Delete later

	df = pd.read_csv(path, encoding='ISO-8859-1')

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

	## Delete rows that have different description for the same stock code
	df_drop = df[df.groupby(['StockCode'])['Description'].transform('nunique') > 1][['StockCode', 'Description']].sort_values(by='StockCode')
	df_unique = df[df.groupby(['StockCode'])['Description'].transform('nunique') > 1][['StockCode', 'Description']].sort_values(by='StockCode').drop_duplicates().drop_duplicates(subset=['StockCode'])
	df_drop = df_drop.drop(df_unique.index)
	df = df.drop(df_drop.index)

	## Delete rows with same description but different stock code
	df_drop = df[df.groupby(['Description'])['StockCode'].transform('nunique') > 1][['StockCode', 'Description']].sort_values(by='Description')
	df = df.drop(df_drop.index)

	# Save clean csv
	df.to_csv('out.csv', index=False)

	return df
