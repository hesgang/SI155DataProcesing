#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/2/22 15:40 
# @Author : hesgang
# @File : DWT.py 

import pywt
from ReadData import *
import matplotlib.pyplot as plt


# totalscal小波的尺度，对应频谱分析结果也就是分析几个（totalscal-1）频谱
def TimeFrequencyCWT(data, fs, totalscal, wavelet='cgau8'):
    # 采样数据的时间维度
    t = np.arange(data.shape[0])/fs
    # 中心频率
    wcf = pywt.central_frequency(wavelet=wavelet)
    # 计算对应频率的小波尺度
    cparam = 2 * wcf * totalscal
    scales = cparam/np.arange(totalscal, 1, -1)
    # 连续小波变换
    [cwtmatr, frequencies] = pywt.cwt(data, scales, wavelet, 1.0/fs)
    # 绘图
    plt.figure(figsize=(8, 4))
    plt.subplot(211)
    plt.plot(t, data)
    plt.xlabel(u"time(s)")
    plt.title(u"Time spectrum")
    plt.subplot(212)
    plt.contourf(t, frequencies, abs(cwtmatr))
    plt.ylabel(u"freq(Hz)")
    plt.xlabel(u"time(s)")
    plt.subplots_adjust(hspace=0.4)
    plt.show()


if __name__ == '__main__':
    df = ReadData(r'C:\Users\He\OneDrive\科研\A大论文\5、特征辨识和解耦\数据\1N.xlsx').get_df
    data = df['w-FBG1'][4000:8000]
    TimeFrequencyCWT(data, fs=200, totalscal=4000, wavelet='cgau8')
