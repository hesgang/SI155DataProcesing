#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/28 15:09 
# @Author : hesgang
# @File : RF-datasets.py
# @Desc : 随机森林数据制作
import numpy as np
import pandas as pd

from ReadData import *
from sklearn import preprocessing
import numpy as np


def peak2drift():
    FBG1_mean = 1531.710346
    FBG2_mean = 1541.635435

    _df = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\温度\温度.xlsx').get_df()
    print(_df.head())
    _df['FBG1'] = _df['FBG1'].map(lambda x: (x - FBG1_mean) * 1000)
    _df['FBG2'] = _df['FBG2'].map(lambda x: (x - FBG2_mean) * 1000)
    _df.to_excel(r'C:\Users\He\OneDrive\触觉与温度耦合\温度\温度dataset.xlsx', index=False)


if __name__ == '__main__':
    # df1 = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\触觉dataset.xlsx').get_df()
    # df2 = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\温度dataset.xlsx').get_df()
    # df3 = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\耦合dataset.xlsx').get_df()
    df = ReadData(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\dataset.csv').get_df()
    print(df.shape)

    # df = pd.concat([df1, df2, df3])
    # df3['T'] = df3['T'].map(lambda x: x * 10)
    # df3['N'] = df3['N'].map(lambda x: x * 10)
    # df.to_csv(r'C:\Users\He\OneDrive\触觉与温度耦合\分类\dataset.csv', index=False)

