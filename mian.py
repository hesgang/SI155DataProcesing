#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/13 15:08 
# @Author : hesgang
# @File : mian.py

from ReadData import *
import tkinter.filedialog as filedialog

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
# from lib.share import SI



if __name__ == '__main__':
    app = QApplication([])
    main_ui = MainUI()
    main_ui.ui.show()
    app.exec_()


