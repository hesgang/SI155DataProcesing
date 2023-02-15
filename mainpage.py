#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/23 21:54 
# @Author : hesgang
# @File : mainpage.py 
import tkinter.filedialog as filedialog
import os
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QListWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QStringListModel, Qt
import time
import pandas as pd
from logger import *
# from lib.share import SI

version = 1.5


class MainUI:
    def __init__(self):
        self.open_path = os.getcwd()
        self.to_path = os.getcwd()
        self.txt_file_path_ = []  # txt文件的绝对路径列表
        self.writer = []
        # qfile_stats = QFile('ui/MainUI.ui')
        # qfile_stats.open(QFile.ReadOnly)
        # qfile_stats.close()
        #
        # self.ui = QUiLoader().load(qfile_stats)
        self.ui = QUiLoader().load('ui/MainUI.ui')
        self.ui.source_btn.clicked.connect(lambda: self. callback_enter('1'))
        self.ui.target_btn.clicked.connect(lambda: self.callback_enter('2'))
        self.ui.refresh_btn.clicked.connect(self.refreshing)
        self.ui.change_btn.clicked.connect(self.callback_change)
        self.ui.tab1_mode_choice.currentIndexChanged.connect(self.callback_mode_choice)
        self.ui.tab1_name_choice.currentIndexChanged.connect(self.callback_mode_choice)
        self.ui.open_list.itemSelectionChanged.connect(self.callback_item_changed)
        self.ui.tab1_console.setPlaceholderText('程序启动成功 - V{}  点击转换开始执行。\n拆分模式：转换的Excel'
                                                '文件为单独的文件。\n合并模式：生成一个Excel中包含多个sheet。'.format(version))
        # self.ui.tab1_merge_btn.clicked.connect(self.call_marge)

        # 文本获取
        self.mode_choice = self.ui.tab1_mode_choice.currentText()
        self.name_choice = self.ui.tab1_name_choice.currentText()

        # init
        self.callback_mode_choice()

    def callback_enter(self, param):
        # 调用filedialog模块的askdirectory()函数去打开文件夹
        # self.open_path = filedialog.askdirectory()
        if param == '1':
            self.txt_file_path_ = []
            self.open_path = QFileDialog.getExistingDirectory()
            self.to_path = self.open_path
            self.ui.tab1_SourceAddress_edt.setText(self.open_path)
            self.ui.tab1_TargetAddress_edt.setText(self.to_path)
            # 根据选择情况，列出文件
            if self.open_path:
                self.ui.open_list.clear()
                self.txt_file_path_ = self.get_dir(self.open_path)

                if self.mode_choice == '批量模式':
                    items_len = len(self.txt_file_path_)
                    self.ui.change_btn.setText('转换({})）'.format(items_len))
                else:
                    self.ui.change_btn.setText('转换(0)）')
                for item in self.txt_file_path_:
                    self.ui.open_list.addItem(os.path.split(item)[1])
            else:
                self.ui.open_list.clear()
        elif param == '2':
            self.to_path = QFileDialog.getExistingDirectory()
            self.ui.tab1_TargetAddress_edt.setText(self.to_path)

    def callback_mode_choice(self):
        self.mode_choice = self.ui.tab1_mode_choice.currentText()
        self.name_choice = self.ui.tab1_name_choice.currentText()
        if self.mode_choice == '选择模式':
            self.ui.open_list.setEnabled(True)
            self.ui.change_btn.setText('转换(0)）')
        else:
            self.ui.open_list.setEnabled(False)

    def callback_item_changed(self):
        if self.mode_choice == '选择模式':
            items_len = len(self.ui.open_list.selectedItems())
            self.ui.change_btn.setText('转换({})）'.format(items_len))
            self.ui.tab1_progressBar.setRange(0, items_len)

    def callback_change(self):
        start_time = time.process_time()
        self.ui.tab1_console.setPlainText('开始执行转换程序')
        change_items = []
        if self.ui.tab1_merge_btn.isChecked():
            self.call_marge()
        # 转换过程中禁用部分模式选择按钮按钮start
        self.ui.tab1_mode_choice.setEnabled(False)
        self.ui.tab1_name_choice.setEnabled(False)
        self.ui.tab1_split_btn.setEnabled(False)
        self.ui.tab1_merge_btn.setEnabled(False)
        # 转换过程中禁用部分模式选择按钮按钮end
        if self.mode_choice == '选择模式':
            currentItem = self.ui.open_list.selectedItems()
            for item in currentItem:
                change_items.append(os.path.join(self.open_path, item.text()))
            self.get_FBG_data(change_items)
        else:
            change_items = self.txt_file_path_
            self.get_FBG_data(change_items)
        if self.ui.tab1_merge_btn.isChecked():
            self.writer.save()
        self.ui.tab1_console.appendPlainText('本次耗时总计：%sS' % (time.process_time() - start_time))
        # 转换结束重新启用部分模式选择按钮按钮start
        self.ui.tab1_mode_choice.setEnabled(True)
        self.ui.tab1_name_choice.setEnabled(True)
        self.ui.tab1_split_btn.setEnabled(True)
        self.ui.tab1_merge_btn.setEnabled(True)
        # 转换过程中禁用部分模式选择按钮按钮end

    def get_dir(self, _path):
        """
        用于获取目录下的文件列表,并返回txt绝对路径列表
        :return:
        """
        items = []
        cf = os.listdir(_path)
        for i in cf:
            if os.path.splitext(i)[1] == '.txt':
                items.append(os.path.join(self.open_path, i))
        return items

    def get_FBG_data(self, files):
        if len(files) != 0:
            self.ui.tab1_target_textedit.clear()
            for i in files:
                try:
                    _st_time = time.process_time()
                    with open(i, mode='r', encoding='GBK') as f:
                        f.seek(0, 0)
                        f_line = f.readlines()
                        if self.name_choice == '时间':
                            name = f_line[3][:23].replace(" ", '-').replace("/", '-').replace(":", '-') + '.xlsx'
                        else:
                            name = os.path.splitext(os.path.split(i)[1])[0].replace(".", '-') + '.xlsx'
                        self.ui.tab1_console.appendPlainText("    [%s] ---> [%s] " % (os.path.split(i)[1], name))
                        self.ui.tab1_target_textedit.appendPlainText(name)
                        # root.update()
                        QApplication.processEvents()
                        for j in range(0, len(f_line)):
                            if 'Timestamp' in f_line[j] and len(f_line[j]) > 30:
                                FBG_data = f_line[j:]
                                break
                        f.close()
                    self.txt_to_excel(FBG_data, name)
                    self.ui.tab1_console.appendPlainText('耗时：%sS ' % (time.process_time() - _st_time))
                except Exception as e:
                    self.ui.tab1_console.appendPlainText('该文件存在错误：\n %s \n' % e)

    def txt_to_excel(self, txt_data_, file_name_):
        sp_data = lambda n: n.split('\n')[0].split('\t')
        sp_list = list(map(sp_data, txt_data_[1:]))
        # df = df.append(sp_list)
        # df = pd.concat([df, sp_list])
        df = pd.DataFrame(sp_list)
        _head = txt_data_[0].split('\n')[0].split('\t')
        data_len = len(df.columns)
        head_len = len(_head)
        if data_len > head_len:
            for _j in range(data_len - head_len):
                _head.append("#-%s" % _j)
        df.columns = _head

        try:
            for j in df.columns:
                if j != 'Timestamp':
                    df[j] = pd.to_numeric(df[j])
        except Exception as e:
            self.ui.tab1_console.appendPlainText('该文件存在错误：\n %s \n' % e)
        if self.ui.tab1_merge_btn.isChecked():
            df.to_excel(self.writer, sheet_name=file_name_)
        else:
            df.to_excel(os.path.join(self.to_path, file_name_), index=False)

    def refreshing(self):
        self.ui.open_list.clear()
        self.txt_file_path_ = self.get_dir(self.open_path)
        # _model = QStringListModel()
        # _model.setStringList(self.txt_file_path_)
        for item in self.txt_file_path_:
            logger.debug('{}'.format(os.path.split(item)))
            self.ui.open_list.addItem(os.path.split(item)[1])

    def call_marge(self):
        self.writer = pd.ExcelWriter(os.path.join(self.to_path, 'merge.xlsx'))


if __name__ == '__main__':
    app = QApplication([])
    main_ui = MainUI()
    main_ui.ui.show()
    app.exec_()
