#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/6 15:28 
# @Author : hesgang
# @File : WT.py 

import numpy as np
import matplotlib.pyplot as plt
import pywt
# 小波
sampling_rate = 1024
t = np.arange(0, 1.0, 1.0 / sampling_rate)
f1 = 100
f2 = 200
f3 = 300
f4 = 400
data = np.piecewise(t, [t < 1, t < 0.8, t < 0.5, t < 0.3],
                    [lambda t: 400*np.sin(2 * np.pi * f4 * t),
                     lambda t: 300*np.sin(2 * np.pi * f3 * t),
                     lambda t: 200*np.sin(2 * np.pi * f2 * t),
                     lambda t: 100*np.sin(2 * np.pi * f1 * t)])
wavename = 'cgau8'
totalscal = 256
fc = pywt.central_frequency(wavename)
cparam = 2 * fc * totalscal
scales = cparam / np.arange(totalscal, 1, -1)
[cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)
plt.figure(figsize=(8, 4))
plt.subplot(211)
plt.plot(t, data)
plt.xlabel("t(s)")
plt.title('shipinpu',  fontsize=20)
plt.subplot(212)
plt.contourf(t, frequencies, abs(cwtmatr))
plt.ylabel(u"prinv(Hz)")
plt.xlabel(u"t(s)")
plt.subplots_adjust(hspace=0.4)
plt.show()