import pandas as pd
import re
import random
import secrets
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.cluster import KMeans
import pickle

def preprocess(df):

    # Get monetary column
    df['Monetary'] = df['searches'].astype(int) * df['price'].astype(float)

    # Transform InvoiceDate to datetime.
    df['date'] = pd.to_datetime(df['date'])

    # Calculate Recency in days as the difference from a recent date (which could be today or the last date of your dataset +1)
    curr_date = pd.Timestamp.today()
    df['Recency'] = (curr_date - df['date']).dt.days

    # Group by CustomerID to calculate Frequency and Monetary values per customer
    rm_df = df.groupby('username').agg({
        'Recency': 'min',            # The most recent purchase date for each customer
        'Monetary': 'sum'           # The total sum for monetary value
    })

    # Reset index
    rm_df.reset_index(inplace=True)
    rm_df.head()

    ax = sns.boxplot(x=rm_df['Recency'])
    plt.savefig('figures/recency.png')
    plt.figure()
    ax1 = sns.boxplot(x=rm_df['Monetary'])
    plt.savefig('figures/monetary.png')

    # Remove noise
    cols = list(rm_df.columns)
    cols.remove('username')
    for col in cols:
      col_zscore = col + '_zscore'
      rm_df[col_zscore] = (rm_df[col] - rm_df[col].mean())/rm_df[col].std(ddof=0)
    clean_df = rm_df[(rm_df['Recency_zscore'] < 3)]
    clean_df = clean_df[(rm_df['Monetary_zscore'] < 3)]
    clean_df = clean_df[['Recency','Monetary']]

    # Standarize
    col_names = ['Recency','Monetary']
    clean_df = rm_df[col_names]
    scaled_values = StandardScaler().fit_transform(clean_df.values)
    scaled_df = pd.DataFrame(scaled_values, columns = col_names)

    return scaled_df

def train(scaled_df):

    # Hyperparameter optimization
    km_scores= []
    km_silhouette = []
    db_score = []
    
    for i in range(2,12):
        km = KMeans(n_clusters=i, init='k-means++',random_state=0).fit(scaled_df)
        preds = km.predict(scaled_df)
    
        km_scores.append(-km.score(scaled_df))
        
        silhouette = silhouette_score(scaled_df,preds)
        km_silhouette.append(silhouette)
        
        db = davies_bouldin_score(scaled_df,preds)
        db_score.append(db)

    plot(title='The elbow method', x=range(2,12),y=km_scores, xlabel='Number of clusters', ylabel='K-means score', filename='elbow_method.png')
    plot(title='The silhouette coefficient method', x=range(2,12), y=km_silhouette, xlabel='Clusters', ylabel='Silhouette score', filename='silhouette_method.png')
    plot(title='The Davies-Boulding method', x=range(2,12), y=db_score, xlabel='Clusters', ylabel='Davies-Bouldin score', filename='davies_boulding_method.png')

    # Build a model with the optimal number of clusters
    kmeans = KMeans(n_clusters = 3, init='k-means++')
    kmeans.fit(scaled_df)

    pickle.dump(kmeans, open('model.pkl', 'wb'))

    print('Silhouette score of the model is: ', end='')
    print(silhouette_score(scaled_df, kmeans.labels_, metric='euclidean'))

    return kmeans

def predict(kmeans):
    pass
    """
    pred = kmeans.predict(scaled_df)
    pred_df = clean_df.copy()
    pred_df['cluster'] = pred
    """

def plot(title, x, y, xlabel, ylabel, filename):
    plt.figure()
    plt.title(title)
    plt.plot(x, y, marker='o')
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(x)
    plt.savefig('figures/'+filename)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='data.csv')
    parser.add_argument('--dates_update', action='store_true', default=True)
    parser.add_argument('--from_dataset', action='store_true', default=False)
    parser.add_argument('--database', type=str, default='../unsecure_website/database.db')
    parser.add_argument("-f", "--file", required=False)
    args = parser.parse_args()

    
    if args.from_dataset:
        print('Cleaning dataset')
        df = clean_dataset(args)
    else:
        print('Getting data from database')
        df = get_database(args)

    scaled_df = preprocess(df)

    # Train model for pivacy attack
    print('Running privacy attack')
    model = train(scaled_df)
    print('Model saved')
