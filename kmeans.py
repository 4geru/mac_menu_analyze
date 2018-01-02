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

zipper = list(map(lambda x: [kcal[x], yen[x]], range(len(kcal))))

features = np.array(zipper)
km = KMeans(n_clusters=3, random_state=10)
y_km = km.fit_predict(features)

for x in range(len(title)):
    if re.search(r"\(S\)",title[x]) and re.search(r"\(M\)",title[x + 1]):
        print(title[x], kcal[x:x+2], yen[x:x+2]) 
        plt.plot(yen[x:x+2], kcal[x:x+2], linestyle="solid", color="red")
    if re.search(r"\(M\)",title[x-1]) and re.search(r"\(L\)",title[x]):
        print(title[x], kcal[x-1:x+1], yen[x-1:x+1]) 
        plt.plot(yen[x-1:x+1], kcal[x-1:x+1], linestyle="solid", color="blue")
# 分類先となったラベルを取得する
labels = km.labels_
plt.scatter(    [yen[x] for x in filter(lambda x: "チキンクリスプ" == title[x] , range(len(labels)))],#re.match(r"チキンクリスプ" , title[x]), range(len(labels)))],
                [kcal[x] for x in filter(lambda x: "チキンクリスプ" == title[x] , range(len(labels)))],#re.match(r"チキンクリスプ" , title[x]), range(len(labels)))],
                s=300,
                c='pink',
                marker='s',
                label='chickencrisp')

plt.scatter(    [yen[x] for x in filter(lambda x: labels[x] == 0, range(len(labels)))],
                [kcal[x] for x in filter(lambda x: labels[x] == 0, range(len(labels)))],
                s=50,
                c='lightgreen',
                marker='o',
                label='cluster 1')
plt.scatter(    [yen[x] for x in filter(lambda x: labels[x] == 1, range(len(labels)))],
                [kcal[x] for x in filter(lambda x: labels[x] == 1, range(len(labels)))],
                s=50,
                c='orange',
                marker='o',
                label='cluster 2')
plt.scatter(    [yen[x] for x in filter(lambda x: labels[x] == 2, range(len(labels)))],
                [kcal[x] for x in filter(lambda x: labels[x] == 2, range(len(labels)))],
                s=50,
                c='lightblue',
                marker='o',
                label='cluster 3')
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