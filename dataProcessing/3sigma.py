#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/13 14:27 
# @Author : hesgang
# @File : 3sigma.py
# @desc : 对实验数据基于3sigma原则进行处理，剔除不合理的数据，减小误差

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ReadData import *


# KS检验
def KsNormDetect(df):  # 输出结果是服从正态分布的数据列的名字
    from scipy.stats import kstest
    list_norm_T = []  # 用来储存服从正态分布的数据列的名字
    for col in df.columns:
        u = df[col].mean()  # 计算均值
        std = df[col].std()  # 计算标准差
        res = kstest(df[col], 'norm', (u, std))  # 计算P值
        print(res)
        if res[1] <= 0.05:  # 判断p值是否服从正态分布，p<=0.05 则服从正态分布，否则不服从
            print(f'{col}该列数据服从正态分布------')
            print('均值为：%.6f，标准差为：%.6f' % (u, std))
            print('-' * 40)
            list_norm_T.append(col)
        else:  # 这一段实际上没什么必要
            print(f'!!!{col}该列数据不服从正态分布**********')
            print('均值为：%.6f，标准差为：%.6f' % (u, std))
            print('*' * 40)
    return list_norm_T


# 对待处理数据中心服从正态分布的数据列
def three_sigma(Ser1):  # Ser1：表示传入DataFrame的某一列
    rule = []
    rule = (Ser1.mean() - 3 * Ser1.std() > Ser1) | (Ser1.mean() + 3 * Ser1.std() < Ser1)
    out = Ser1.index[rule]
    return out  # 返回落在3sigma之外的行索引值


def delete_out3sigma(data, list_norm):  # data：待检测的DataFrame；list_norm：服从正态分布的数据列名
    out_index = []  # 保存要删除的行索引
    for col in list_norm:  # 对每一列分别用3sigma原则处理
        index = three_sigma(data[col])
        out_index += index.tolist()
    delete_ = list(set(out_index))  # 去除 out_index 中的重复元素
    print(f'\n所删除的行索引共计{len(delete_)}个：\n', delete_)
    data.drop(delete_, inplace=True)  # 根据 delete_ 删除对应行的数据
    return data


if __name__ == '__main__':
    start_time = time.process_time()
    df1 = ReadData(r'D:\压力实验to表格\第一次-FBG2-加载.xlsx').get_df
    plt.subplot(2, 1, 1)
    # plt.hist(df1['10g'], bins=500, color='pink', edgecolor='b')
    plt.plot(df1['0g'])
    plt.subplot(2, 1, 2)
    df1 = delete_out3sigma(df1, ['0g', '10g'])
    plt.plot(df1['0g'])
    plt.show()

    end = time.process_time() - start_time
    print('总耗时：%s' % end)

