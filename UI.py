#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/5
# @Author : hesgang
# @File : UI.py

import time
import tkinter.filedialog as filedialog
import os
from tkinter import *
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


def get_FBG_data(files):
    if len(files) != 0:
        for i in files:
            try:
                _st_time = time.process_time()
                with open(i, mode='r', encoding='GBK') as f:
                    f.seek(0, 0)
                    f_line = f.readlines()
                    if Xuanxiang.get() == 2:
                        name = f_line[3][:23].replace(" ", '-').replace("/", '-').replace(":", '-') + '.xlsx'
                    else:
                        name = os.path.splitext(os.path.split(i)[1])[0].replace(".", '-') + '.xlsx'
                    log.insert(END, "    [%s] ---> [%s] \n" % (os.path.split(i)[1], name))
                    listbox2file.insert(END, name)
                    root.update()
                    for j in range(0, len(f_line)):
                        if 'Timestamp' in f_line[j] and len(f_line[j]) > 30:
                            FBG_data = f_line[j:]
                            break
                    f.close()
                txt_to_excel(FBG_data, name)
                log.insert(END, '耗时：%sS \n' % (time.process_time() - _st_time))
                log.see(END)
            except Exception as e:
                log.insert(END, '该文件存在错误：\n %s \n' % e)
                log.see(END)


def txt_to_excel(txt_data_, file_name_):
    global filepath
    sp_data = lambda n: n.split('\n')[0].split('\t')
    sp_list = list(map(sp_data, txt_data_[1:]))
    # df = df.append(sp_list)
    # df = pd.concat([df, sp_list])
    df = pd.DataFrame(sp_list)
    _head = txt_data_[0].split('\n')[0].split('\t')
    data_len = len(df.columns)
    head_len = len(_head)
    if data_len > head_len:
        for _j in range(data_len-head_len):
            _head.append("#-%s" % _j)
    df.columns = _head

    try:
        for j in df.columns:
            if j != 'Timestamp':
                df[j] = pd.to_numeric(df[j])
    except Exception as e:
        log.insert(END, '该文件存在错误：\n %s \n' % e)
        log.see(END)

    df.to_excel(os.path.join(filepath, file_name_), index=False)


def callback_enter():
    global filepath
    entry.delete(0, END)  # 清空entry里面的内容
    listbox_filename.delete(0, END)
    listbox2file.delete(0, END)
    # 调用filedialog模块的askdirectory()函数去打开文件夹
    filepath = filedialog.askdirectory()
    if filepath == '':
        filepath = os.getcwd()
    entry.insert(0, filepath)  # 将选择好的路径加入到entry里面
    getdir()
    log.delete('1.0', END)
    log.insert(END, '当前位置： %s \n' % filepath)
    log.see(END)


def callback_change():
    start_time = time.process_time()
    log.delete('1.0', END)
    log.insert(END, '开始执行转换程序\n')
    global txt_file_path_
    listbox2file.delete(0, END)
    if mode_var.get() == 1:
        get_FBG_data(txt_file_path_)
    elif mode_var.get() == 2:
        select_file = []
        for _i in listbox_filename.curselection():
            select_file.append(txt_file_path_[_i])
        get_FBG_data(select_file)
    log.insert(END, '本次耗时总计：%sS\n' % (time.process_time()-start_time))
    log.see(END)


def getdir():
    """
    用于获取目录下的文件列表,并返回txt绝对路径列表
    :return:
    """
    global txt_file_path_, filepath
    txt_file_path_ = []
    cf = os.listdir(filepath)
    for i in cf:
        if os.path.splitext(i)[1] == '.txt':
            listbox_filename.insert(END, i)
            txt_file_path_.append(os.path.join(filepath, i))


if __name__ == "__main__":
    txt_file_path_ = []  # txt文件的绝对路径列表
    filepath = os.getcwd()
    root = Tk()
    # 禁用最大化
    root.resizable(False, False)

    root.title("SI155--txt2excel by hesgang")
    root.geometry("670x400")
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(5, weight=2)

    entry = Entry(root, width=80)
    entry.grid(sticky=W + N, row=0, column=0, columnspan=6, padx=10, pady=10)
    entry.insert(0, os.getcwd())

    button1 = Button(root, text="选择文件夹", command=callback_enter)
    button1.grid(sticky=W + N, row=0, column=6, padx=5, pady=5)
    button2 = Button(root, text="选择文件夹", command=callback_enter)
    button2.grid(sticky=W + N, row=0, column=6, padx=5, pady=5)


    # 创建loistbox用来显示所有文件名
    listbox_filename = Listbox(root, width=40, height=11, selectmode="extended")
    getdir()
    listbox_filename.grid(row=1, column=0, columnspan=2, rowspan=6,
                          padx=5, pady=5, sticky=W + E + N)

    mode_var = IntVar()
    mode_var.set(1)
    mode_button1 = Radiobutton(root, text="批量模式", variable=mode_var, value=1)
    mode_button1.grid(row=1, column=3, sticky=SW)
    mode_button2 = Radiobutton(root, text="选择模式", variable=mode_var, value=2)
    mode_button2.grid(row=2, column=3, sticky=NW)

    Xuanxiang = IntVar()
    Xuanxiang.set(1)
    choice1 = Radiobutton(root, text="输出文件名", variable=Xuanxiang, value=1)
    choice1.grid(row=3, column=3, sticky=NW)
    choice2 = Radiobutton(root, text="输出日期", variable=Xuanxiang, value=2)
    choice2.grid(row=4, column=3, sticky=NW)
    button2 = Button(root, text="转换", command=callback_change)
    button2.grid(row=5, column=3, columnspan=2, pady=5, sticky=W + E + N)

    listbox2file = Listbox(root, width=40, height=11)
    listbox2file.grid(row=1, column=5, columnspan=2, rowspan=6, padx=5, pady=5, sticky=W + E + N)

    log = Text(root, height=8, bg='#27231f', font=('JetBrains Mono', 11), fg='white')
    log.grid(row=6, column=0, columnspan=7, padx=5, pady=10, sticky=W + E + N)

    log.insert(END, '程序启动成功 - V%s  点击转换开始执行\n' % version)

    root.mainloop()


