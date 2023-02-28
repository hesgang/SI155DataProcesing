#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/28 15:09 
# @Author : hesgang
# @File : RF-datasets.py
# @Desc : 随机森林数据制作
import numpy as np

from ReadData import *
from sklearn import preprocessing
import numpy as np


def peak2drift():
    FBG1_mean = 1531.637069
    FBG2_mean = 1541.618658
    _df = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\数据汇总.xlsx').get_df
    print(df.head())
    _df['FBG1'] = _df['FBG1'].map(lambda x: (x - FBG1_mean) * 1000)
    _df['FBG2'] = _df['FBG2'].map(lambda x: (x - FBG2_mean) * 1000)
    _df.to_excel(r'C:\Users\He\OneDrive\触觉与温度耦合\dataset.xlsx', index=False)


if __name__ == '__main__':
    df = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\dataset.xlsx').get_df
    min_max_scaler = preprocessing.MinMaxScaler()
    x_minmax = min_max_scaler.fit_transform(df)
    print(x_minmax)

