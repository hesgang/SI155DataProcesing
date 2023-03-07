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
import matplotlib.pyplot as plt
from ReadData import *
import joblib
from sympy import *
from tqdm import tqdm

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
    x, y = get_dataset(os.path.join(OneDrive, r'触觉与温度耦合\耦合\merage_train.xlsx'), 'rfr')
    xx, yy = get_dataset(os.path.join(OneDrive, r'触觉与温度耦合\耦合\merage_test.xlsx'), 'rfr')
    to_path = os.path.join(OneDrive, r'触觉与温度耦合\耦合\rfr.pkl')
    scores = []
    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    xx_train, xx_test, yy_train, yy_test = train_test_split(xx, yy, test_size=0.9)
    # 建立随机森林回归器模型，并获得得分
    # _rfr = RandomForestRegressor()
    # _rfr.fit(x, y)
    # joblib.dump(_rfr, to_path)

    _rfr = joblib.load(to_path)
    predict_y = _rfr.predict(xx_test)
    print(predict_y.shape)
    for i in range(20):
        print(predict_y[i], yy_test[i])
    # pd.DataFrame({'原始': xx,
    #               'predict_y': predict_y,
    #               'true_y': yy}).to_excel(os.path.join(OneDrive, r'触觉与温度耦合\耦合\out.xlsx'), index=False)

    r_score = _rfr.score(xx_test, yy_test)
    print("Random Forest : ", r_score)


def rfr_test():
    model_path = os.path.join(OneDrive, r'触觉与温度耦合\耦合\rfr.pkl')
    # xx, yy = get_dataset(os.path.join(OneDrive, r'触觉与温度耦合\耦合\merage_test.xlsx'), 'rfr')
    data_df = ReadData(os.path.join(OneDrive, r'触觉与温度耦合\耦合\merage_test.xlsx'))
    x = preprocessing.MinMaxScaler().fit_transform(data_df.get_df(['FBG1', 'FBG2']))
    y = data_df.get_df(['T', 'N']).values
    # 分割并打乱数据
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    _rfr = joblib.load(model_path)
    # predict_y = _rfr.predict(x)
    # df1 = pd.concat([pd.DataFrame(data_df.get_df(['FBG1', 'FBG2'])), pd.DataFrame(y), pd.DataFrame(predict_y)], axis=1)
    # df1.to_excel(os.path.join(OneDrive, r'触觉与温度耦合\耦合\predict.xlsx'), index=False)
    r_score = _rfr.score(x, y)
    print("Random Forest : ", r_score)


def cal_xy():
    x = symbols('x')
    y = symbols('y')
    _df = ReadData(os.path.join(OneDrive, r'触觉与温度耦合\耦合\predict.xlsx')).get_df()
    f1 = 60.022 * x - 52.673 + 17.174 * y
    f2 = 69.553 * x + 14.404 * y
    scale = _df.shape[0]
    with tqdm(total=scale) as pbar:
        pbar.set_description('Processing:')
        for i in _df.index:
            result = solve([f1 - _df['FBG1'][i], f2 - _df['FBG2'][i]], [x, y])
            _df['calT'].at[i] = result[y]
            _df['calN'].at[i] = result[x]
            pbar.update(1)
        _df.to_excel(os.path.join(OneDrive, r'触觉与温度耦合\耦合\predict-1.xlsx'))




if __name__ == '__main__':
    start_time = time.time()
    OneDrive = os.getenv('OneDriveConsumer')
    # run_rfc()
    # rfc_study_line()
    # run_rfr()
    # rfr_test()
    cal_xy()
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

