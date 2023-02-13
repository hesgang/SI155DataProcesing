#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/13 15:06 
# @Author : hesgang
# @File : Wave_filtering.py 


# 均值滤波
def ava_filter(_x, _filter_length):
    """
    用于单次计算给定窗口长度的均值滤波
    :param _x: 需要滤波数据
    :param _filter_length: 滤波窗口长度
    :return: 滤波后的数据
    """
    N = len(_x)
    res = []
    for i in range(N):
        if i <= _filter_length//2 or i >= N - (_filter_length//2):
            temp = _x[i]
        else:
            _sum = 0
            for j in range(_filter_length):
                _sum += _x[i - _filter_length//2 + j]
            temp = _sum * 1.0 / _filter_length
        res.append(temp)
    return res


# 均值滤波降噪
def denoise(_x, _filter_length, _n):
    """
    用于指定次数调用“ava_filter”函数，进行降噪处理
    :param _x: 需要降噪的数据
    :param _filter_length: 窗口长度
    :param _n: 指定的次数
    :return:
    """
    for i in range(_n):
        res = ava_filter(_x, _filter_length)
        _x = res
    return _x



