#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023年2月23日
# @Author : hesgang
# @File : DeviationVar.py
# @Desc : 计算方差


import numpy as np
import pandas as pd

from ReadData import *
import matplotlib.pyplot as plt


def random_list(nums, st=0, ed=10):
    a = []
    while len(a) < nums:
        b = np.random.randint(st, ed)
        if b not in a:
            a.append(b)
    return a


# 提取滑动部分数据
df_1N = ReadData(r'E:\Documents\OneDrive\小波变换9.13\4N\4N.xlsx', False).get_df
print(df_1N.shape)
print(np.average(df_1N['B'][20000:35000]) * 1000)
print(np.average(df_1N['A'][20000:35000]) * 1000)
print(np.average(df_1N['D'][20000:35000]) * 1000)
print(np.average(df_1N['C'][20000:35000]) * 1000)

for col in ['B', 'A']:
    print('8' * 50)
    for i in random_list(30, 20000, 35000):
        print(df_1N[col][i] * 1000)
for col in ['D', 'C']:
    print('8' * 50)
    for i in random_list(30, 20000, 35000):
        print(df_1N[col][i] * 1000)
# data = df_1N['A']
# data1 = df_1N['B']
# data3 = df_1N['c']
# data4 = df_1N['d']

# r_a = random_list(30)
# print(r_a)
# for col in ['剪切力-FBG1', '剪切力-FBG2', '滑动-FBG1', '滑动-FBG2']:
#     print('*' * 60)
#     for i in r_a:
#         print(df_1N[col][i])
# plt.subplot(221)
# plt.plot(np.arange(0, len(data), 1), data)
# plt.subplot(222)
# plt.plot(np.arange(0, len(data1), 1), data1)
# plt.subplot(223)
# plt.plot(np.arange(0, len(data3), 1), data3)
# plt.subplot(224)
# plt.plot(np.arange(0, len(data4), 1), data4)
# plt.show()

# to_df = pd.DataFrame(columns=['剪切力-FBG1', '剪切力-FBG2', '滑动-FBG1', '滑动-FBG2'])
# print(df_1N['B'][25000:40000].to_list)
# to_df['剪切力-FBG1'] = df_1N['B'][25000:40000].to_list
# to_df['剪切力-FBG2'] = df_1N['A'][25000:40000].to_list
# to_df['滑动-FBG1'] = df_1N['D'][15000:30000].to_list
# to_df['滑动-FBG2'] = df_1N['C'][15000:30000].to_list
# print(to_df['滑动-FBG1'])
# to_df.to_excel(r'E:\Documents\OneDrive\科研\A大论文\5、特征辨识和解耦\数据\整体长度不同\局部1N.xlsx')

