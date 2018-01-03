import pandas as pd
import numpy as np
import json
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

menu_json = open('./scrayping/menu.txt' , 'r')
menus = json.load(menu_json)

kcal = [int(menu['kcal']) for menu in menus ]
yen = [menu['yen'] for menu in menus ]
title = [menu['name'] for menu in menus ]
genres = [menu['genre'] for menu in menus ]

# グラフ作成
fig = plt.figure()
ax = Axes3D(fig)

# 軸ラベルの設定
ax.set_xlabel("yen")
ax.set_ylabel("kcal")
ax.set_zlabel("kcal/yen")

x = [int(x) for x in kcal]
y = yen
z = [ (_x / _y) for (_x, _y) in zip(x,y)]
# kcal / yen

ax.plot(x, y, z, "o", color="#cccccc", ms=4, mew=0.5)

def plotgenres(genre, color):
    ax.scatter3D(   [yen[x] for x in filter(lambda x: genre == genres[x] , range(len(genres)))],
                    [kcal[x] for x in filter(lambda x: genre == genres[x] , range(len(genres)))],
                    [kcal[x] / yen[x] for x in filter(lambda x: genre == genres[x] , range(len(genres)))],
                    c=color,
                    marker='o',
                    label=genre)
plotgenres("drink", "pink")
plotgenres("hamburger", "lightgreen")
plotgenres("morning", "lightblue")
plotgenres("side", "red")
plotgenres('dessert', 'yellow')
plotgenres('soup', 'white')

plt.savefig("graph3d.png")