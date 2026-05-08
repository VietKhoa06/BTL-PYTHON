import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import io

df = pd.read_csv('cầu thủ thi đấu trên 90ph.csv')
features = ['90s', 'CrdY', 'CrdR', '2CrdY', 'Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'PKwon', 'PKcon', 'OG']

for col in features:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

X = df[features].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

K_range = range(2, 11)
inertia = []
silhouette_avg = []

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_avg.append(silhouette_score(X_scaled, kmeans.labels_))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertia, 'bx-')
plt.title('Elbow Method')
plt.xlabel('Number of clusters (k)')

plt.subplot(1, 2, 2)
plt.plot(K_range, silhouette_avg, 'rx-')
plt.title('Silhouette Score')
plt.xlabel('Number of clusters (k)')
plt.savefig('elbow_silhouette.png')

best_k = 4
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

pca_2d = PCA(n_components=2)
X_pca_2d = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(10, 6))
plt.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], c=df['Cluster'], cmap='viridis', alpha=0.7)
plt.title('Phân cụm cầu thủ trên không gian PCA 2D')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.colorbar(label='Cluster')
plt.savefig('pca_2d.png')

pca_3d = PCA(n_components=3)
X_pca_3d = pca_3d.fit_transform(X_scaled)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_pca_3d[:, 0], X_pca_3d[:, 1], X_pca_3d[:, 2], c=df['Cluster'], cmap='viridis', alpha=0.7)
ax.set_title('Phân cụm cầu thủ trên không gian PCA 3D')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
plt.savefig('pca_3d.png')