import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

cleaned_plays = pd.read_csv('data/plays_clean.csv')

assets = pd.read_csv('data/assets.csv')
asset_genre = assets[['asset_id', 'genre']]
cleaned_plays = pd.merge(cleaned_plays, asset_genre, on='asset_id')

# perform DBSCAN clustering
clustering = cleaned_plays[['user_id', 'minutes_viewed', 'genre']]

# pivot the table so that each row is a user and each column is a genre, with the values being the total minutes viewed
pivot_table = clustering.pivot_table(index='user_id', columns='genre', values='minutes_viewed', aggfunc='sum').fillna(0)

# scale the data, with respect to the mean and standard deviation
scaler = StandardScaler()
scaled_data = scaler.fit_transform(pivot_table)

# plot the elbow curve to determine the optimal epsilon value

# neigh = NearestNeighbors(n_neighbors=30)
# nbrs = neigh.fit(scaled_data)
# distances, indices = nbrs.kneighbors(scaled_data)
# distances = np.sort(distances, axis=0)
# distances = distances[:,1]
# plt.plot(distances)
# plt.show()


# perform DBSCAN clustering
dbscan = DBSCAN(eps=4, min_samples=4) # we tried to approach this methodically, but the recommended approaches gave bad results.
dbscan.fit(scaled_data)
# convert values back to watchtime minutes
pivot_table = pd.DataFrame(scaler.inverse_transform(scaled_data), columns=pivot_table.columns, index=pivot_table.index)

pivot_table['cluster'] = dbscan.labels_

# print number of clusters and noise points
print('Number of clusters: ', len(pivot_table['cluster'].unique()) - 1)
print('Number of noise points: ', len(pivot_table[pivot_table['cluster'] == -1]))

# calculate mean minutes viewed for each cluster
cluster_means = pivot_table.groupby('cluster').mean()
print(cluster_means)

# save the cluster labels to a csv file
pivot_table.groupby('cluster').mean().to_csv('data/clusters.csv')

# print genres sorted by watch time for each cluster, ignoring values less than 1 minute
for cluster in pivot_table['cluster'].unique():
    if cluster != -1:
        print('Cluster: ', cluster)
        print(cluster_means.loc[cluster][cluster_means.loc[cluster] > 1].sort_values(ascending=False))
        print('\n')




