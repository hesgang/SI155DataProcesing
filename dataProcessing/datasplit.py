#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/26 15:20 
# @Author : hesgang
# @File : 数据拆分求和.py
import os.path

from ReadData import *
import tkinter.filedialog as filedialog

if __name__ == '__main__':
    start_time = time.process_time()
    filepath = filedialog.askopenfilename()
    if filepath == '':
        filepath = os.getcwd()
    N1 = ReadData(filepath).get_df

    for i in ['A', 'B', 'C', 'D']:
        A = []
        N1[i] = N1[i].abs()
        start_index = input("请输入起始点位置：（并以回车结束）")
        start_index = int(start_index)
        A.append(start_index)
        for j in range(50):
            aa = np.average(N1[i][(start_index + j * 100): (start_index + j * 100 + 100)])
            A.append(aa)
        N1[i + '1'][0:len(A)] = A
    path = os.path.split(filepath)
    N1.to_excel(os.path.join(path[0], '1_'+path[1]))
    end = time.process_time() - start_time
    print('总耗时：%s' % end)
