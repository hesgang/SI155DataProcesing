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


def f2(x):
    return x + (random_() * 10 + 45.787)/1000


def f1(x):
    return x + (random_() * 10 + 13.907)/1000


start_time = time.time()
if __name__ == '__main__':
    df = pd.read_csv(r'C:\Users\He\OneDrive\触觉与温度耦合\dataset.csv')
    print(df.head())


