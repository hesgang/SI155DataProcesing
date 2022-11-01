#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/5
# @Author : hesgang
# @File : UI.py

import time
import tkinter.filedialog as filedialog
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import re

version = 1.2


def get_date(file):
    with open(file, mode='r', encoding='GBK') as f:
        for i in f:
            tt = re.findall('Date', i)
            if len(tt) > 0:
                name_ = i[6:24]
        f.close()
    return name_


class AppUI(object):
    def __init__(self, master):
        self.openpath = os.getcwd()
        self.topath = os.getcwd()
        self.txt_file_path_ = []  # txt文件的绝对路径列表
        self.notebook = ttk.Notebook(master)
        self.frame1 = tk.Frame(master)
        self.frame2 = tk.Frame(master)

        self.notebook.add(self.frame1, text='转换')
        self.notebook.add(self.frame2, text='合并')
        self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # --------------------画布1begin-----------------
        self.entry11 = Entry(self.frame1, width=30)
        self.entry11.grid(sticky=W + N, row=0, column=0, columnspan=2, padx=10, pady=10)
        self.entry11.insert(0, os.getcwd())
        self.button11 = Button(self.frame1, text="选择")
        self.button11.bind("<ButtonRelease>", self.callback_enter)
        self.button11.grid(sticky=W + N, row=0, column=2, padx=5, pady=5)

        self.entry12 = Entry(self.frame1, width=30)
        self.entry12.grid(sticky=W + N, row=0, column=4, columnspan=2, padx=10, pady=10)
        self.entry12.insert(0, os.getcwd())
        self.button12 = Button(self.frame1, text="选择")
        self.button12.bind("<ButtonRelease>", self.callback_enter)
        self.button12.grid(sticky=W + N, row=0, column=6, padx=5, pady=5)

        # 创建loistbox用来显示所有文件名
        self.listbox_filename = Listbox(self.frame1, width=30, height=11, selectmode="extended")
        self.getdir()
        self.listbox_filename.grid(row=1, column=0, columnspan=3, rowspan=6,
                              padx=5, pady=5, sticky=W + E + N)

        self.mode_var = IntVar()
        self.mode_var.set(1)
        self.mode_button1 = Radiobutton(self.frame1, text="批量模式", variable=self.mode_var, value=1)
        self.mode_button1.grid(row=1, column=3, sticky=SW)
        self.mode_button2 = Radiobutton(self.frame1, text="选择模式", variable=self.mode_var, value=2)
        self.mode_button2.grid(row=2, column=3, sticky=NW)
        self.zhankong = Label(self.frame1, text=" ")
        self.zhankong.grid(sticky=W + N, row=3, column=3, padx=2, pady=6)
        self.Xuanxiang = IntVar()
        self.Xuanxiang.set(1)
        self.choice1 = Radiobutton(self.frame1, text="输出文件名", variable=self.Xuanxiang, value=1)
        self.choice1.grid(row=4, column=3, sticky=SW)
        self.choice2 = Radiobutton(self.frame1, text="输出日期", variable=self.Xuanxiang, value=2)
        self.choice2.grid(row=5, column=3, pady=1, sticky=NW)
        self.button2 = Button(self.frame1, text="转换", command=self.callback_change)
        self.button2.grid(row=6, column=3, pady=(0, 5), sticky=W + E + S)

        self.listbox2file = Listbox(self.frame1, width=40, height=11)
        self.listbox2file.grid(row=1, column=5, columnspan=2, rowspan=6, padx=5, pady=5, sticky=W + E + N)

        self.log = Text(self.frame1, height=9, bg='#27231f', font=('JetBrains Mono', 11), fg='white')
        self.log.grid(row=7, column=0, columnspan=7, padx=5, pady=10, sticky=W + E + N)

        self.log.insert(END, '程序启动成功 - V%s  点击转换开始执行\n' % version)
        # --------------------画布1end-----------------

        # --------------------画布2begin-----------------
        self.entry21 = Entry(self.frame2, width=75)
        self.entry21.grid(sticky=W + N, row=0, column=0, columnspan=6, padx=10, pady=10)
        self.entry21.insert(0, os.getcwd())
        self.button21 = Button(self.frame2, text="选择文件夹")
        self.button21.bind("<ButtonRelease>", self.callback_enter)
        self.button21.grid(sticky=W + N, row=0, column=6, padx=5, pady=5)

        # 创建loistbox用来显示所有文件名
        self.listbox_filename21 = Listbox(self.frame2, width=30, height=11, selectmode="extended")
        self.getdir()
        self.listbox_filename21.grid(row=1, column=0, columnspan=3, rowspan=6,
                              padx=5, pady=5, sticky=W + E + N)
        self.listbox2file21 = Listbox(self.frame1, width=40, height=11)
        self.listbox2file21.grid(row=1, column=5, columnspan=2, rowspan=6, padx=5, pady=5, sticky=W + E + N)

        # --------------------画布2end-----------------

    def callback_enter(self, event):
        if '{}'.format(event.widget) == '.!frame.!button':
            self.entry11.delete(0, END)  # 清空entry里面的内容
            self.entry12.delete(0, END)  # 清空entry里面的内容
            self.listbox_filename.delete(0, END)
            self.listbox2file.delete(0, END)
            # 调用filedialog模块的askdirectory()函数去打开文件夹
            self.openpath = filedialog.askdirectory()
            self.topath = self.openpath
            if self.openpath == '':
                self.openpath = os.getcwd()
            self.entry11.insert(0, self.openpath)  # 将选择好的路径加入到entry里面
            self.entry12.insert(0, self.topath)  # 将选择好的路径加入到entry里面
            self.getdir()
            self.log.delete('1.0', END)
            self.log.insert(END, '当前位置： %s \n' % filepath)
            self.log.see(END)
        elif '{}'.format(event.widget) == '.!frame.!button2':
            self.entry12.delete(0, END)  # 清空entry里面的内容
            # 调用filedialog模块的askdirectory()函数去打开文件夹
            self.topath = filedialog.askdirectory()
            if self.topath == '':
                self.topath = os.getcwd()
            self.entry12.insert(0, self.topath)  # 将选择好的路径加入到entry里面
        elif '{}'.format(event.widget) == '.!frame2.!button':
            self.entry21.delete(0, END)  # 清空entry里面的内容
            self.listbox_filename21.delete(0, END)
            self.listbox2file21.delete(0, END)
            # 调用filedialog模块的askdirectory()函数去打开文件夹
            self.openpath = filedialog.askdirectory()
            self.topath = self.openpath
            if self.openpath == '':
                self.openpath = os.getcwd()
            self.entry21.insert(0, self.openpath)  # 将选择好的路径加入到entry里面

    def getdir(self):
        """
        用于获取目录下的文件列表,并返回txt绝对路径列表
        :return:
        """
        self.txt_file_path_ = []
        cf = os.listdir(self.openpath)
        for i in cf:
            if os.path.splitext(i)[1] == '.txt':
                self.listbox_filename.insert(END, i)
                self.txt_file_path_.append(os.path.join(self.openpath, i))

    def callback_change(self):
        start_time = time.process_time()
        self.log.delete('1.0', END)
        self.log.insert(END, '开始执行转换程序\n')
        self.listbox2file.delete(0, END)
        if self.mode_var.get() == 1:
            self.get_FBG_data(self.txt_file_path_)
        elif self.mode_var.get() == 2:
            select_file = []
            for _i in self.listbox_filename.curselection():
                select_file.append(self.txt_file_path_[_i])
            self.get_FBG_data(select_file)
        self.log.insert(END, '本次耗时总计：%sS\n' % (time.process_time() - start_time))
        self.log.see(END)

    def get_FBG_data(self, files):
        if len(files) != 0:
            for i in files:
                try:
                    _st_time = time.process_time()
                    with open(i, mode='r', encoding='GBK') as f:
                        f.seek(0, 0)
                        f_line = f.readlines()
                        if self.Xuanxiang.get() == 2:
                            name = f_line[3][:23].replace(" ", '-').replace("/", '-').replace(":", '-') + '.xlsx'
                        else:
                            name = os.path.splitext(os.path.split(i)[1])[0].replace(".", '-') + '.xlsx'
                        self.log.insert(END, "    [%s] ---> [%s] \n" % (os.path.split(i)[1], name))
                        self.listbox2file.insert(END, name)
                        root.update()
                        for j in range(0, len(f_line)):
                            if 'Timestamp' in f_line[j] and len(f_line[j]) > 30:
                                FBG_data = f_line[j:]
                                break
                        f.close()
                    self.txt_to_excel(FBG_data, name)
                    self.log.insert(END, '耗时：%sS \n' % (time.process_time() - _st_time))
                    self.log.see(END)
                except Exception as e:
                    self.log.insert(END, '该文件存在错误：\n %s \n' % e)
                    self.log.see(END)

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
            self.log.insert(END, '该文件存在错误：\n %s \n' % e)
            self.log.see(END)
        df.to_excel(os.path.join(self.topath, file_name_), index=False)

    def refresh_data(self):
        # old_files = self.txt_file_path_
        # print(old_files)
        self.getdir()
        # if len(old_files) == len(self.txt_file_path_):




if __name__ == "__main__":

    filepath = os.getcwd()

    # -------------界面基础配置begin------------
    root = tk.Tk()
    root.resizable(False, False)  # 禁用最大化
    root.title("SI155--DataProcessing by hesgang")
    root.geometry("670x435")
    root.rowconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)
    root.columnconfigure(4, weight=2)
    # -------------界面基础配置end------------

    AppUI(root)
    root.mainloop()




