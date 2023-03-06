#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/22 11:06 
# @Author : hesgang
# @File : add_random
import numpy as np
from ReadData import *

def random_():
    return np.random.uniform(-1, 1)


def read_FBG():
    T = '#40'
    _df = pd.DataFrame(np.random.randint(0, 100, size=(3000, 2)), columns=['FBG1', 'FBG2'])
    FBG1_1 = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\FBG1-1.xlsx').get_df()
    FBG1_2 = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\FBG1-2.xlsx').get_df()
    FBG1_3 = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\FBG1-3.xlsx').get_df()
    FBG2_1 = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\FBG2-1.xlsx').get_df()
    FBG2_2 = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\FBG2-2.xlsx').get_df()
    FBG2_3 = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\FBG2-3.xlsx').get_df()
    for i in _df.index:
        if i % 1000 == 0:
            r = np.random.randint(0, 1000)
        if i < 1000:
            _df['FBG1'][i] = (FBG1_1[T][i + r] - FBG1_1['#0'][i + r])*1000
            _df['FBG2'][i] = (FBG2_1[T][i + r] - FBG2_1['#0'][i + r])*1000
        elif i < 2000:
            _df['FBG1'][i] = (FBG1_2[T][i + r - 1000] - FBG1_2['#0'][i + r - 1000]) * 1000
            _df['FBG2'][i] = (FBG2_2[T][i + r - 1000] - FBG2_2['#0'][i + r - 1000]) * 1000
        else:
            _df['FBG1'][i] = (FBG1_3[T][i + r - 2000] - FBG1_3['#0'][i + r - 2000]) * 1000
            _df['FBG2'][i] = (FBG2_3[T][i + r - 2000] - FBG2_3['#0'][i + r - 2000]) * 1000
    print(_df)
    _df.to_excel(r'E:\Documents\OneDrive\触觉与温度耦合\温度\{}.xlsx'.format(T), index=False)

def write_FBG():
    T = '#40'
    FBG1 = [[8.783, 9.108, 11.57],
            [39.007, 36.04, 37.955],
            [64.08, 62.251, 65.269],
            [89.773, 92.219, 95.475],
            [127.449, 129.732, 128.562]]
    FBG2 = [[63.374, 64.438, 66.601],
            [95.005, 95.206, 94.273],
            [142.091, 140.254, 143.303],
            [177.822, 175.71, 180.239],
            [209.399, 218.004, 212.846]]
    _df = ReadData(r'E:\Documents\OneDrive\触觉与温度耦合\温度\{}.xlsx'.format(T)).get_df()
    writer = pd.ExcelWriter(r'E:\Documents\OneDrive\触觉与温度耦合\温度\#{}.xlsx'.format(T))
    for F in range(5):
        new_df = pd.DataFrame(np.random.randint(0, 100, size=(3000, 2)), columns=['FBG1', 'FBG2'])
        for i in _df.index:
            if i < 1000:
                new_df['FBG1'].at[i] = _df['FBG1'][i] + FBG1[F][0] * 0.5
                new_df['FBG2'].at[i] = _df['FBG2'][i] + FBG2[F][0] * 0.6
            elif i < 2000:
                new_df['FBG1'].at[i] = _df['FBG1'][i] + FBG1[F][1] * 0.5
                new_df['FBG2'].at[i] = _df['FBG2'][i] + FBG2[F][1] * 0.6
            else:
                new_df['FBG1'].at[i] = _df['FBG1'][i] + FBG1[F][2] * 0.5
                new_df['FBG2'].at[i] = _df['FBG2'][i] + FBG2[F][2] * 0.6
        new_df.to_excel(writer, sheet_name='{}N'.format(1 + F * 0.5), index=False)
    writer.save()



if __name__ == '__main__':
    write_FBG()
    pass
