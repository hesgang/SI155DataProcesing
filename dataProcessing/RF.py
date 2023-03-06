#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/28 16:02 
# @Author : hesgang
# @File : RF.py
# @Desc : 随机森林算法的使用
import os

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


def get_dataset(data_path, _type='rfc'):
    min_max_scaler = preprocessing.MinMaxScaler()
    # 加载数据集
    data = ReadData(data_path)
    x_df = data.get_df(['FBG1', 'FBG2'])
    x = min_max_scaler.fit_transform(x_df)
    if _type == 'rfc':
        y_df = data.get_df(['C'])
        y = y_df['C'].to_list()
    elif _type == 'rfr':
        y_df = data.get_df(['T', 'N'])
        y = y_df.values
    else:
        raise TypeError
    return x, y


def run_rfc():
    """
    训练随机森林分类器模型
    :return:
    """
    # 加载数据集
    x, y = get_dataset(os.path.join(OneDrive, r'触觉与温度耦合\分类\dataset.csv'), 'rfc')
    to_path = os.path.join(OneDrive, r'触觉与温度耦合\分类\rfc.pkl')
    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    # 建立随机森林分类器模型，并获得得分
    _rfc = RandomForestClassifier()
    _rfc.fit(x_train, y_train)
    joblib.dump(_rfc, to_path)
    # _rfc = joblib.load(os.path.join(OneDrive, r'触觉与温度耦合\分类\rfc.pkl'))
    predict_y = _rfc.predict(x_test)
    pd.DataFrame({'predict_y': predict_y,
                  'true_y': y_test}).to_excel(os.path.join(OneDrive, r'触觉与温度耦合\分类\t.xlsx'), index=False)
    r_score = _rfc.score(x_test, y_test)
    print("Random Forest : ", r_score)


def rfc_study_line():
    """
    计算随机森林学习曲线
    :return:
    """
    # 加载数据集
    x, y = get_dataset(os.path.join(OneDrive, r'触觉与温度耦合\分类\dataset.csv'), 'rfc')
    scores = []

    for i in range(1, 50):
        _rfc = RandomForestClassifier(n_estimators=i, n_jobs=-1)
        scores.append(cross_val_score(_rfc, x, y, cv=10).mean())
        print(time.time() - start_time)

    print(scores)
    plt.plot(range(1, 50), scores)
    plt.show()
    with open(os.path.join(OneDrive, r'触觉与温度耦合\分类\scores.txt'), 'wb') as f:
        f.writelines(scores)
        f.close()

    print(max(scores), scores.index(max(scores)))


def run_rfr():
    # 加载数据集
    x, y = get_dataset(os.path.join(OneDrive, r'触觉与温度耦合\耦合\耦合数据汇总.xlsx'), 'rfr')
    scores = []
    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    # 建立随机森林回归器模型，并获得得分
    _rfr = RandomForestRegressor()
    _rfr.fit(x_train, y_train)
    p = _rfr.predict(x_test)
    for _i in range(20):
        print(p[_i], y_test[_i])




if __name__ == '__main__':
    start_time = time.time()
    OneDrive = os.getenv('OneDriveConsumer')
    # run_rfc()
    # rfc_study_line()
    run_rfr()
    # rfc = joblib.load(os.path.join(OneDrive, r'触觉与温度耦合\分类\rfc.pkl'))
    # predict_data = ReadData(os.path.join(OneDrive, r'触觉与温度耦合\分类\验证数据.xlsx')).get_df()
    # train_data = ReadData(os.path.join(OneDrive, r'触觉与温度耦合\分类\dataset.csv')).get_df()
    # all_data = pd.concat([predict_data, train_data])
    # all_x = all_data[['FBG1', 'FBG2']]
    # predict_x = preprocessing.MinMaxScaler().fit_transform(predict_data[['FBG1', 'FBG2']])[0:199]
    # predict_y = all_data['C'].to_list()[0:199]
    # mode_y = rfc.predict(predict_x)
    # print(type(mode_y))
    # print(predict_y)
    # pd.DataFrame(mode_y).to_excel(os.path.join(OneDrive, r'触觉与温度耦合\分类\t.xlsx'))

    end = time.time() - start_time
    print('总耗时：%s' % end)

