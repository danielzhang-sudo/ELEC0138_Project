import sqlite3
import pandas as pd
import re
import random
import secrets
import argparse

import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.cluster import KMeans

DATABASE = '../unsecure_website/database.db'

def get_database(args):
    
    database = args.database

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    with conn:
      cur.execute('''SELECT searches.product_name, searches.searches, searches.date, products.price, users.username FROM searches JOIN users ON searches.user_id = users.user_id JOIN products ON products.name = searches.product_name ''')
      all_searches = cur.fetchall()

    name_list, searches_list, date_list, price_list, username_list = [], [], [], [], []

    for i in all_searches:
      name, searches, date, price, username = i
      name_list.append(name)
      searches_list.append(searches)
      date_list.append(date)
      price_list.append(price)
      username_list.append(username)

    df = pd.DataFrame({'name':name_list, 'searches':searches_list,'date':date_list,'price':price_list,'username':username_list})

    return df

def clean_dataset(args):
    path = args.path
    change_dates = args.dates_update

    with open('xato-net-10-million-usernames-dup.txt', 'r') as f:
        usernames = f.read().splitlines()[:5000]

    with open('10-million-password-list-top-1000.txt', 'r') as f:
        passwords = f.read().splitlines()

    df = pd.read_csv(path, encoding='ISO-8859-1')
    df_clean = df.copy()

    # Clean dataset
    ## Delete rows with no customer ID
    df = df[df['CustomerID'].notna()]

    ## Delete rows with no description
    df = df[df['Description'].notna()]

    ## Delete rows with stock code that do not correspond to products
    df = df[df['StockCode'].str.len() >= 5]
    df = df[df['StockCode'].str.len() <= 6]

    ## Delete rows with prices below 0
    df = df[df['UnitPrice'] >= 0]

    ## Delete items corresponding to returns or other
    df = df[df['Quantity'] > 0]

    # Delete rows with incorrect stock codes
    df = df[~df['StockCode'].str.contains(r'[a-z]+')]

    ## Rewrite descriptions of rows that have same StockCode but different Description
    df_drop = df[df.groupby(['StockCode'])['Description'].transform('nunique') > 1][['StockCode', 'Description']].sort_values(by='StockCode')
    codes = df_drop['StockCode'].unique()
    for i in df_drop['StockCode'].unique():
        df_drop.loc[df_drop['StockCode'] == i, 'Description'] = df_drop[df_drop['StockCode'] == i].iloc[0]['Description']

    df.update(df_drop)

    ## Rename descriptions of rows that have different StockCode but same Description
    df_drop = df[df.groupby(['Description'])['StockCode'].transform('nunique') > 1][['StockCode', 'Description']].sort_values(by='Description')
    for i, row in df_drop.iterrows():
        df_drop.loc[i, 'Description'] = ' Variant '+str(row['StockCode'])+': '+row['Description']


    # Change StockCode of same product with different price
    codes = df['StockCode'].unique()
    abc = 'A,B,C,D,E,F,G,H,I,H,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,_0,_1,_2,_3,_4,_5,_6,_7,_8,_9'.split(',')

    for code in codes:
        prices = df[df['StockCode'] == code]['UnitPrice'].unique()
        descriptions = df[df['StockCode'] == code]['Description'].unique()
        if (len(prices) > 1) and (len(descriptions) == 1):
            for i, price in enumerate(prices):
                df.loc[(df['StockCode'] == code) & (df['UnitPrice'] == price), 'StockCode'] = code+str(abc[i]) #[index, 'StockCode'] = row['StockCode']+str(abc[i])

    df.update(df_drop)

    df['Description'] = df['Description'].str.replace(',', '-', regex=True)

    # Remove unnecessary columns
    df = df[['StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID']]

    if change_dates:
        # Change dates
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) + (pd.Timestamp.today() - (pd.to_datetime(df['InvoiceDate'])).max()) - pd.Timedelta(days=1)

    # Rename columns
    df.rename(columns={'StockCode':'name', 'Description':'description', 'Quantity':'searches', 'InvoiceDate':'date', 'UnitPrice': 'price', 'CustomerID':'username'}, inplace=True)

    # Change customerIDs to usernames
    df['username'] = df['username'].astype(str).str.strip('.0')

    users = list(df['username'].unique())
    user_name = random.sample(usernames, len(users))
    user_pass = random.choices(passwords, k=len(users))

    for i, user in enumerate(users):
        # df.loc[df['username'] == user, 'password_plain'] = user_pass[i]
        # df.loc[df['username'] == user, 'salt'] = user_salt[i]
        df.loc[df['username'] == user, 'username'] = user_name[i]

    user_df = df[['username']].copy().drop_duplicates()
    user_df['password'] = user_pass

    products_df = df[['name', 'description', 'price']].copy().drop_duplicates()

    searches_df = df[['username', 'name', 'searches', 'date']]

    # Save cleaned dataset
    df.to_csv('dataset/clean_data.csv', index=False)

    # Save datasets to populate website database
    user_df.to_csv('../dataset/user.csv', index=False)
    products_df.to_csv('../dataset/products.csv', index=False)
    searches_df.to_csv('../dataset/searches.csv', index=False)

    return df






