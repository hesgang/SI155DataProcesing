#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/28 16:02 
# @Author : hesgang
# @File : RF.py
# @Desc : 随机森林算法的使用
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score # 交叉检验
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ReadData import *


# matplotlib inline
plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 加载数据集
data = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\dataset.xlsx')
df = data.get_df(['FBG1', 'FBG2'])
df1 = data.get_df(['T', 'N'])
min_max_scaler = preprocessing.MinMaxScaler()
x = min_max_scaler.fit_transform(df)
y = df1.values

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
print(X_train, X_test)

# 训练随机森林，决策树模型，比较两种模型

# 建立随机森林分类器模型，并获得得分
rfc = RandomForestClassifier(random_state=1)
rfc.fit(X_train, y_train)
r_score = rfc.score(X_test, y_test)

# 建立分类决策树模型，并获得得分
dtc = DecisionTreeClassifier(random_state=1)
dtc.fit(X_train, y_train)
d_score = dtc.score(X_test, y_test)

print("Decision Tree:{}\nRandom Forest: {}".format(d_score, r_score))
# Decision Tree:0.8703703703703703
# Random Forest: 0.9259259259259259

if __name__ == '__main__':
    pass
