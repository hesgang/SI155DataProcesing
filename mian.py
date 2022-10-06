#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/13 15:08 
# @Author : hesgang
# @File : mian.py

from ReadData import *
import tkinter.filedialog as filedialog


def getDataWithOpenWindow():
    filepath = filedialog.askopenfilenames()
    for _i in filepath:
        print(_i)



if __name__ == '__main__':
    getDataWithOpenWindow()
    # start_time = time.process_time()
    # aa = ReadData(r'D:\code\DataProcessing\data\2022\s5-20220805151008.xlsx').get_df
    # print(aa)
    # end = time.process_time() - start_time
    # print('总耗时：%s' % end)

