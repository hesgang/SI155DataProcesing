#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/13 15:08 
# @Author : hesgang
# @File : mian.py

from ReadData import *
from dataProcessing.add_random import *
import tkinter.filedialog as filedialog

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
# from lib.share import SI

start_time = time.time()
if __name__ == '__main__':
    aa = ReadData(r'C:\Users\He\Desktop\xiepo.xlsx').get_df
    print(aa.head())
    for cols in aa.columns:
        for index in range(len(aa[cols])):
            aa[cols][index] = aa[cols][index] + random_()
    aa.to_excel(r'C:\Users\He\Desktop\xiepo2.xlsx')
    end = time.time() - start_time
    print('总耗时：%s' % end)


