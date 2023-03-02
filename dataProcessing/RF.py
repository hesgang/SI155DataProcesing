#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/28 16:02 
# @Author : hesgang
# @File : RF.py
# @Desc : 随机森林算法的使用
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score # 交叉检验
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ReadData import *
import joblib



# matplotlib inline
plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def get_dataset():
    # 加载数据集
    data = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\dataset.csv')
    x_df = data.get_df(['FBG1', 'FBG2'])
    y_df = data.get_df(['C'])
    min_max_scaler = preprocessing.MinMaxScaler()
    x = min_max_scaler.fit_transform(x_df)
    y = y_df['C'].to_list()
    return x, y


def run_rfc():
    # 加载数据集
    x, y = get_dataset()

    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    # 建立随机森林分类器模型，并获得得分
    rfc = RandomForestClassifier()
    rfc.fit(x_train, y_train)
    joblib.dump(rfc, r'C:\Users\He\OneDrive\触觉与温度耦合\rfc.pkl')
    r_score = rfc.score(x_test, y_test)
    print("Random Forest : ", r_score)


def rfc_study_line():
    # 加载数据集
    x, y = get_dataset()
    scores = []

    for i in range(1, 201):
        rfc = RandomForestClassifier(n_estimators=i, n_jobs=-1)
        scores.append(cross_val_score(rfc, x, y, cv=10).mean())
        print(time.time() - start_time)

    plt.plot(range(1, 201), scores)
    plt.show()
    with open(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\scores.txt', 'wb') as f:
        f.writelines(scores)
        f.close()

    print(max(scores), scores.index(max(scores)))







# r_scores = []
# for i in range(10):
#     rfr = RandomForestRegressor(n_estimators=25)
#     # 每一次交叉检验取平均值
#     r_scores.append(cross_val_score(rfr, x, y.astype('int'), cv=10).mean())
#
#
# plt.plot(range(1, 11), r_scores, label='Random Forest')
# plt.legend(loc='best')
# plt.show()



if __name__ == '__main__':
    start_time = time.time()
    # run_rfc()
    rfc_study_line()

    end = time.time() - start_time
    print('总耗时：%s' % end)

