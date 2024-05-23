import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from umap import UMAP  # Import UMAP
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple

def f1score(df):
    maior = 0
    numClusters = len(df['cluster'].unique())
    for i in range(numClusters):
        dfi = df[df['cluster'] == i]
        totalAcertos = len(dfi[dfi['target'] == 1])
        totalErros = len(dfi[dfi['target'] == 0])
        try:
            ratio = totalAcertos/totalErros
        except:
            ratio = 0
        if(ratio > maior):
            maior = ratio
            clusterResultante = i

    dfBomb = df[df['cluster'] == clusterResultante]
    positivoVerdadeiro = len(dfBomb[dfBomb['target'] == 1])
    falsoPositivo = len(dfBomb[dfBomb['target'] == 0])
    dfOutro = df[df['cluster'] != clusterResultante]
    falsoNegativo = len(dfOutro[dfOutro['target'] == 1])
    negativoVerdadeiro = len(dfOutro[dfOutro['target'] == 0])
    print(f"Cluster escolhido = {clusterResultante}")
    print(f"    |  sim  |  não  |")
    print("---------------------|")
    print(f"sim | {positivoVerdadeiro} | {falsoNegativo}  |")
    print("---------------------|")
    print(f"nao | {falsoPositivo} | {negativoVerdadeiro}|")
    print("")
    recall = (positivoVerdadeiro)/(positivoVerdadeiro+falsoNegativo)
    precisao = (positivoVerdadeiro)/(positivoVerdadeiro+falsoPositivo)
    f1_score = 2 * ((precisao * recall) / (precisao + recall))
    print(f"recall = {recall:.4f}".replace('.', ','))
    print(f"precisão = {precisao:.4f}".replace('.', ','))
    print(f"f1 score = {f1_score:.4f}".replace('.', ','))


df = pd.read_csv('Jogos.csv')
df.fillna(0, inplace=True)
df.drop(columns=['plataforms'], inplace=True)
df = df[df['totalComments'] > 50]

# Select features
#features = df[['totalComments', 'totalAlike', 'metricScore', 'comments/reviews', 'meanToxicity', 'totalToxic', 'noteVariance']]
features = df[['totalComments', 'meanToxicity', 'totalAlike', 'userRtotal', 'totalCurse']]


# Standardize features
scaler = StandardScaler()
features_standardized = scaler.fit_transform(features)

# UMAP embedding
umap_model = UMAP(n_components=2, random_state=42)
umap_result = umap_model.fit_transform(features_standardized)

# K-means clustering
kmeans = KMeans(n_clusters=2, random_state=42)
df['cluster'] = kmeans.fit_predict(features_standardized)

# Plotting
plt.figure(figsize=(12, 8))

#seismic
#rainbow
#nipy_spectral178746
# UMAP scatter plot
colors = ['#178746', '#871733']
colors_dark = ['#6b122b', '#11683d']

plt.scatter(umap_result[df['target'] == 0, 0], umap_result[df['target'] == 0, 1],
            c=[colors[i] for i in df[df['target'] == 0]['cluster']], alpha=0.7, label='Target 0')
plt.scatter(umap_result[df['target'] == 1, 0], umap_result[df['target'] == 1, 1],
            c=[colors[i] for i in df[df['target'] == 1]['cluster']], marker='^', label='Target 1')



# Title annotations
#for i, title in enumerate(df['title']):
#    plt.text(umap_result[i, 0], umap_result[i, 1], title, fontsize=8, alpha=0.7)

centroids = kmeans.cluster_centers_
#plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=200, color='red', label='Centroids')
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Cluster 0',
           markerfacecolor=colors[0], markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Cluster 1',
           markerfacecolor=colors[1], markersize=10, linestyle='None', markeredgewidth=1),
]

# Cria os marcadores para o alvo
target_markers = [
    Line2D([0], [0], marker='^', color='w', markerfacecolor=colors[0], markersize=10, linestyle='None', markeredgewidth=1),
    Line2D([0], [0], marker='^', color='w', markerfacecolor=colors[1], markersize=10, linestyle='None', markeredgewidth=1)
]

# Configurações do plot
plt.xlabel('UMAP Dimensão 1')
plt.ylabel('UMAP Dimensão 2')

# Adiciona a legenda com um manipulador personalizado
plt.legend([*legend_elements, tuple(target_markers)], ['Cluster 0', 'Cluster 1', 'Alvos'], handler_map={tuple: HandlerTuple(ndivide=None)}, loc='upper right')
plt.show()

games_to_review_bomb = [
    'Bastion','Toy Soldiers: Cold War'
    ,"Fire Emblem: Three Houses", "Mass Effect 3", "Borderlands 3",
    "Madden NFL 21","Grand Theft Auto: The Trilogy - The Definitive Edition",
    "The Last of Us Part II", "Astral Chain", "Call of Duty: Modern Warfare",
    "Death Stranding", "Warcraft III: Reforged", 'Pokemon Sword', 'Pokemon Shield',
    'Metro Exodus',
    "AI: The Somnium Files", "Animal Crossing: New Horizons", "Gran Turismo 7",
    "Sonic Frontiers", "Call of Duty: Modern Warfare 3",

    'Horizon Forbidden West', 'Diablo IV', 'Overwatch 2',
    'Diabblo Immortal', 'Horizon Forbidden West: Burning Shores',
    'Battlefield V'
]

games_in_df = df[df['title'].isin(games_to_review_bomb)]
print(len(games_to_review_bomb))
print(f"Number of games in the dataframe: {len(games_in_df)}")
games_in_clusters = {cluster: 0 for cluster in df['cluster'].unique()}
total_games_in_clusters = {cluster: 0 for cluster in df['cluster'].unique()}

for index, row in df.iterrows():
    total_games_in_clusters[row['cluster']] += 1

for game in games_to_review_bomb:
    if game in df['title'].values:
        cluster = df[df['title'] == game]['cluster'].values[0]
        games_in_clusters[cluster] += 1

for cluster, count in games_in_clusters.items():
    print(f"Cluster {cluster}: {count} games from games_to_review_bomb, Total Games: {total_games_in_clusters[cluster]}")

print()

centroids_original = scaler.inverse_transform(centroids)

# Print the real numbers of the centroids
for i, centroid in enumerate(centroids_original):
    print(f"Real Centroid {i + 1}: {centroid}")

cluster_2_titles = df[df['cluster'] == 1]['title']
print()
print("Titles in Cluster 2:")
for title in cluster_2_titles:
    print(title)

print("-----------")
df2 = df[df['cluster'] == 0]
df2 = df2[df2['target'] == 1]['title']
for title in df2:
    print(title)
print('--------')
f1score(df)

cluster1_df = df[df['cluster'] == 0]
cluster2_df = df[df['cluster'] == 1]

# Salve os dataframes em arquivos CSV
cluster1_df.to_csv('livreAtaque.csv', index=False)
cluster2_df.to_csv('sofreuAtaque.csv', index=False)