# https://qiita.com/deaikei/items/11a10fde5bb47a2cf2c2
import pandas as pd
import numpy as np
import json
import re
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

menu_json = open('./scrayping/menu.txt' , 'r')
menus = json.load(menu_json)

kcal = [int(menu['kcal']) for menu in menus ]
yen = [menu['yen'] for menu in menus ]
title = [menu['name'] for menu in menus ]
genres = [menu['genre'] for menu in menus ]

zipper = list(map(lambda x: [kcal[x], yen[x]], range(len(kcal))))

features = np.array(zipper)
km = KMeans(n_clusters=3, random_state=10)
y_km = km.fit_predict(features)

# for x in range(len(title)):
#     if re.search(r"\(S\)",title[x]) and re.search(r"\(M\)",title[x + 1]):
#         print(title[x], kcal[x:x+2], yen[x:x+2]) 
#         # plt.plot(yen[x:x+2], kcal[x:x+2], linestyle="solid", color="red", linewidth=7.0)
#     if re.search(r"\(M\)",title[x-1]) and re.search(r"\(L\)",title[x]):
#         print(title[x], kcal[x-1:x+1], yen[x-1:x+1]) 
#         # plt.plot(yen[x-1:x+1], kcal[x-1:x+1], linestyle="solid", color="blue", linewidth=7.0)

# 分類先となったラベルを取得する
labels = km.labels_

def cluster(id, label, color):
    plt.scatter(    [yen[x] for x in filter(lambda x: labels[x] == id, range(len(labels)))],
                    [kcal[x] for x in filter(lambda x: labels[x] == id, range(len(labels)))],
                    s=150,
                    c=color,
                    marker='s',
                    label=label)

cluster(0, 'cluster 1', 'lightgreen')
cluster(1, 'cluster 2', 'orange')
cluster(2, 'cluster 3', 'lightblue')

def plotgenres(plt, genre, color):
    plt.scatter(    [yen[x] for x in filter(lambda x: genre == genres[x] , range(len(genres)))],#re.match(r"チキンクリスプ" , title[x]), range(len(labels)))],
                    [kcal[x] for x in filter(lambda x: genre == genres[x] , range(len(genres)))],#re.match(r"チキンクリスプ" , title[x]), range(len(labels)))],
                    s=50,
                    c=color,
                    marker='o',
                    label=genre)

plotgenres(plt, "drink", "pink")
plotgenres(plt, "hamburger", "lightgreen")
plotgenres(plt, "morning", "lightblue")
plotgenres(plt, "side", "red")
plotgenres(plt, 'dessert', 'yellow')
plotgenres(plt, 'soup', 'white')

plt.scatter(    km.cluster_centers_[:,0],   # km.cluster_centers_には各クラスターのセントロイドの座標が入っている
                km.cluster_centers_[:,1],
                s=250,
                marker='*',
                c='red',
                label='centroids')

# for x in filter(lambda x: labels[x] == 2, range(len(labels))):
#     print(features[x], title[x])
plt.xlabel("yen", fontsize=20) # x軸のタイトル
plt.ylabel(r"kcal", fontsize=20) # y軸

plt.legend(loc='lower right')
plt.grid()
plt.ylim([-50,1000])
plt.savefig("graph.png")