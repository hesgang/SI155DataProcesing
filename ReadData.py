#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/7/18 10:08
# @Author : hesgang
# @File : ReadData.py

import re
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
import time
from datetime import date, timedelta
import pandas as pd
from pandas import ExcelWriter
import numpy as np
# import matplotlib.pyplot as plt
import base64


class ReadData(object):
    def __init__(self, excel_path, sheet_name=0):
        self.tmp = self.__getTemp__()
        self.excel_path = excel_path
        self.path, self.file = os.path.split(self.excel_path)
        self.file_name = self.file.split('.')[0]
        self.b64_name = base64.b64encode(self.file_name.encode('utf-8')).decode('utf-8')
        self.file_type = self.file.split('.')[1]
        self.npy_path = os.path.join(self.tmp, self.b64_name + '.npy')
        self.npy_c_path = os.path.join(self.tmp, self.b64_name + '_c' + '.npy')
        self.sheet_name = sheet_name

    def __read_data(self):
        '''
        读取文件，默认将首行作为列命，首列做为行名
        :return: DataFrame -> obj
        '''
        if self.file_type in ['xlsx', 'xls']:
            # 读取缓存文件
            try:
                # 根据文件修改时间，选择最新的读取
                excel_t = os.path.getmtime(self.excel_path)
                npy_t = os.path.getmtime(self.npy_path)
                if npy_t > excel_t:
                    df = np.load(self.npy_path, allow_pickle=True)
                    df_c = np.load(self.npy_c_path, allow_pickle=True)
                    df = pd.DataFrame(df, columns=df_c)
                    return df
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                df = pd.read_excel(self.excel_path, header=0, sheet_name=self.sheet_name)
                df_c = np.array(df.columns.values)
                data_ndarray = df.to_numpy()
                np.save(self.npy_path, data_ndarray)
                np.save(self.npy_c_path, df_c)
                return df
            except Exception as e:
                print(e)
                sys.exit()

    @staticmethod
    def __getTemp__() -> str:
        """
        根据不同的电脑，获取不同的缓存路径
        :return: TempPath
        """
        _temp = os.getenv('TEMP')
        if os.path.exists('/cache'):
            return '/cache'
        elif os.path.exists(_temp):
            return _temp
        else:
            return os.getcwd()

    @property
    def get_df(self):
        return self.__read_data()


if __name__ == '__main__':
    start_time = time.process_time()
    aa = ReadData(r'D:\code\DataProcessing\data\2022\s5-20220805151008.xlsx').get_df
    end = time.process_time() - start_time
    print('总耗时：%s' % end)

