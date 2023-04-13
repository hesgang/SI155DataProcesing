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
from logger import logger


class ReadData(object):
    def __init__(self, excel_path, cache=True):
        self.is_cache = cache
        self.tmp = self.__getTemp__()
        self.excel_path = excel_path
        self.path, self.file = os.path.split(self.excel_path)
        self.cache_file_name = base64.b64encode(self.excel_path.encode('utf-8')).decode('utf-8')
        self.cache_file = os.path.join(self.tmp, self.cache_file_name+'.csv')
        # print(base64.b64decode(self.cache_file).decode('utf-8'))
        self.file_name = self.file.split('.')[0]
        self.b64_name = base64.b64encode(self.file_name.encode('utf-8')).decode('utf-8')
        self.file_type = self.file.split('.')[1]
        self.npy_path = os.path.join(self.tmp, self.b64_name + '.npy')
        self.npy_c_path = os.path.join(self.tmp, self.b64_name + '_c' + '.npy')
        self.df_obj = self.__load_obj__()
        self.is_cached = self.__is_cached__()
        self.df = self.__load_data__()

        # self.sheet_name = sheet_name

    def __load_obj__(self):
        if self.file_type in ['xlsx', 'xls']:
            _df = pd.ExcelFile(self.excel_path)
            return _df
        elif self.file_type == 'csv':
            _df = pd.read_csv(self.excel_path)
            return _df
        else:
            raise TypeError

    def __load_data__(self):
        if isinstance(self.df_obj, pd.DataFrame):
            # CVS 格式无需缓存，直接读取，因此obj包含数据载入
            logger.info('原始文件：{}.{}--包含的{}'.format(self.file_name, self.file_type, self.df_obj.columns))
            return self.df_obj
        elif len(self.df_obj.sheet_names) == 1:
            # 单sheet文件，直接读取与缓存
            if self.is_cache and self.is_cached:
                _df = pd.read_csv(self.cache_file)
                logger.info('缓存文件：{}.{}--包含的{}'.format(self.file_name, self.file_type, _df.columns))
                return _df
            else:
                # _df = pd.read_excel(self.excel_path)
                _df = self.df_obj.parse(0)
                self.__cache__(_df)
                logger.info('原始文件：{}.{}--包含的{}'.format(self.file_name, self.file_type, _df.columns))
                return _df
        else:
            # 多sheet文件，缓存与读取
            if self.is_cache and self.is_cached:
                # 已缓存
                # self.cache_file为默认缓存第一个sheet，并读取返回
                _df = pd.read_csv(self.cache_file)
                logger.info('原始工作簿{}存在多个sheet，如下：\n {}'.format(self.file_name, self.df_obj.sheet_names))
                logger.info('其中缓存[{}]---包含的{}'.format(self.df_obj.sheet_names[0], _df.columns))
                return _df
            else:
                # 缓存，并返回第一个sheet
                _df1 = self.df_obj.parse(0)
                self.__cache__(_df1)
                self.__cache__(self.df_obj)
                logger.info('原始工作簿{}存在多个sheet，如下：\n {}'.format(self.file_name, self.df_obj.sheet_names))
                logger.info('其中原始[{}]---包含的{}'.format(self.df_obj.sheet_names[0], _df1.columns))
                return _df1

    def __is_cached__(self):
        if os.path.exists(self.cache_file):
            # 根据文件修改时间，选择最新的读取
            file_t = os.path.getmtime(self.excel_path)
            cache_t = os.path.getmtime(self.cache_file)
            if cache_t > file_t:
                return True
        return False

    def __cache__(self, _df):
        if isinstance(_df, pd.DataFrame):
            # 单sheet传入pd.DataFrame
            _df.to_csv(self.cache_file, index=False)
        elif isinstance(_df, pd.ExcelFile):
            # 多sheet传入pd.ExcelWriter
            # ToDo 存在缓存时间过程问题
            for i in self.df_obj.sheet_names[1:]:
                name = os.path.join(self.path, self.file_name + 's-' + i + '-s')
                name = base64.b64encode(name.encode('utf-8')).decode('utf-8')
                cache_file = os.path.join(self.tmp, name + '.csv')
                self.df_obj.parse(i).to_csv(cache_file, index=False)
        else:
            raise TypeError

    @staticmethod
    def __getTemp__() -> str:
        """
        根据不同的电脑，获取不同的缓存路径
        :return: TempPath
        """
        _temp = os.getenv('TEMP')
        if os.path.exists('/cache'):
            logger.debug('/cache')
            return '/cache'
        elif os.path.exists(_temp):
            logger.debug(_temp)
            return _temp
        else:
            logger.info(os.getcwd())
            return os.getcwd()

    def get_df(self,
               cols: list[str] = [],
               sheet_name: str = ''
               ) -> pd.DataFrame:
        if len(sheet_name) == 0 or sheet_name == self.df_obj.sheet_names[0]:
            # 返回默认df
            if len(cols) == 0:
                return self.df
            else:
                return self.df[cols]
        else:
            if sheet_name in self.df_obj.sheet_names:
                name = os.path.join(self.path, self.file_name + 's-' + sheet_name + '-s')
                name = base64.b64encode(name.encode('utf-8')).decode('utf-8')
                name = os.path.join(self.tmp, name + '.csv')
                if os.path.exists(name):
                    _df = pd.read_csv(name)
                else:
                    _df = self.df_obj.parse(sheet_name)
                logger.info('其中[{}]---包含的{}'.format(sheet_name, _df.columns))
                if len(cols) == 0:
                    return _df
                else:
                    return _df[cols]
            else:
                raise KeyError('[\'{}\'] not in sheet_names'.format(sheet_name))

if __name__ == '__main__':
    start_time = time.time()
    # f = pd.ExcelFile(r'D:\Temp\滑动4N-全过程.xlsx')
    aa = ReadData(r'D:\Temp\数据20230410 (筛选).xlsx').get_df()
    print(aa)
    end = time.time() - start_time
    print('总耗时：%s' % end)

    #     df1 = f.parse(sheet_name=i)
    #     df1.drop('Timestamp', axis=1, inplace=True)
    #     df1.to_excel(writer, sheet_name=i)