#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/6
# @Author : hesgang
# @File : ReadData.py
# @description : 将txt文件合并后转换为一个整体CSV，便于后期数据处理
import tkinter as tk
import tkinter.filedialog as filedialog
import os
import pandas as pd
import re


def get_path():
    # 隐藏tk主窗口
    top = tk.Tk()
    top.geometry('0x0+999999+0')
    # 调用filedialog模块的askdirectory()函数去打开文件夹
    filepath = filedialog.askdirectory()
    top.destroy()
    return filepath if filepath != '' else os.getcwd()


def getdir(filetype='txt'):
    """
    用于获取目录下的文件列表,并返回txt绝对路径列表
    :param filetype: 需要筛选的文件类型，默认txt
    :return:
    """
    global path
    filetype = filetype if '.' in filetype else '.'+filetype
    filepath_ = []
    cf = os.listdir(path)
    for i in cf:
        if os.path.splitext(i)[1] == filetype:
            filepath_.append(i)
    return filepath_


def get_FBG_data(_files):
    all_data_ = {}
    global path
    if len(_files) != 0:
        for i_ in _files:
            try:
                with open(os.path.join(path, i_), mode='r', encoding='GBK') as f:
                    f.seek(0, 0)
                    f_line = f.readlines()
                    for j in range(0, len(f_line)):
                        if 'Timestamp' in f_line[j] and len(f_line[j]) > 30:
                            FBG_data = f_line[j:]
                            break
                    f.close()
                all_data_[i_] = txt_to_df(FBG_data)
            except Exception as e:
                print(e)
    return all_data_


def txt_to_df(txt_data_):
    sp_data = lambda n: n.split('\n')[0].split('\t')
    sp_list = list(map(sp_data, txt_data_[1:]))
    _df = pd.DataFrame(sp_list)
    _head = txt_data_[0].split('\n')[0].split('\t')
    data_len = len(_df.columns)
    head_len = len(_head)
    if data_len > head_len:
        for _j in range(data_len-head_len):
            _head.append("#-%s" % _j)
    _df.columns = _head

    try:
        for j in _df.columns:
            if j != 'Timestamp':
                _df[j] = pd.to_numeric(_df[j])
    except Exception as e:
        print(e)
    return _df


def get_name(_index, names):
    by_sort = []
    for _i in _index:
        for _j in names:
            if str(_i) == re.findall('[0-9]+', _j)[0]:
                by_sort.append(_j)
    return by_sort


def sort_temp(keys_, flag_, up_=True):
    up_list, up_name = [], []
    down_list, down_name = [], []
    for i_ in keys_:
        if flag_ in i_:
            if '+' in i_:
                up_list.append(int(re.findall('[0-9]+', i_)[0]))
                up_name.append(i_)
            else:
                down_list.append(int(re.findall('[0-9]+', i_)[0]))
                down_name.append(i_)
    up_list.sort()
    down_list.sort()

    if up_:
        return get_name(up_list, up_name)
    else:
        return get_name(down_list, down_name)


if __name__ == '__main__':
    # TODO
    file_type = 'txt'
    path = get_path()
    files = getdir(file_type)
    all_data = get_FBG_data(files)
    FBG1_df = pd.DataFrame()
    FBG2_df = pd.DataFrame()
    FBG3_df = pd.DataFrame()
    FBG4_df = pd.DataFrame()

    # 获得含有df的dict，正负需要修改函数里
    after_sort = sort_temp(all_data.keys(), 'sen', True)
    for i in after_sort:
        df = all_data[i]
        # FBG1_df = pd.concat([FBG1_df, df['#-0']], axis=1)
        # FBG2_df = pd.concat([FBG2_df, df['#-1']], axis=1)
        FBG1_df = pd.concat([FBG1_df, df['FBG_A1']], axis=1)
        FBG2_df = pd.concat([FBG2_df, df['FBG_A1']], axis=1)
        # FBG3_df = pd.concat([FBG3_df, df['#-2']], axis=1)
        # FBG4_df = pd.concat([FBG4_df, df['#-3']], axis=1)

    FBG1_df.to_excel(os.path.join(path, 'FBG1-sen升温.xlsx'), index=False)
    FBG2_df.to_excel(os.path.join(path, 'FBG2-sen升温.xlsx'), index=False)
    # FBG3_df.to_excel(os.path.join(path, 'FBG3-peak降温.xlsx'), index=False)
    # FBG4_df.to_excel(os.path.join(path, 'FBG4-peak降温.xlsx'), index=False)
    # FBG3_df.to_excel(os.path.join(path, '裸升温.xlsx'), index=False)



