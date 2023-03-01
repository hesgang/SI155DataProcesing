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
        self.file_name = self.file.split('.')[0]
        self.b64_name = base64.b64encode(self.file_name.encode('utf-8')).decode('utf-8')
        self.file_type = self.file.split('.')[1]
        self.npy_path = os.path.join(self.tmp, self.b64_name + '.npy')
        self.npy_c_path = os.path.join(self.tmp, self.b64_name + '_c' + '.npy')
        self.df = self.__read_data()
        # self.sheet_name = sheet_name

    def __read_data(self):
        '''
        读取文件，默认将首行作为列命，首列做为行名
        :return: DataFrame -> obj
        '''
        if self.file_type in ['xlsx', 'xls']:
            if self.is_cache:
                # 读取缓存文件
                try:
                    # 根据文件修改时间，选择最新的读取
                    excel_t = os.path.getmtime(self.excel_path)
                    npy_t = os.path.getmtime(self.npy_path)
                    if npy_t > excel_t:
                        _df = np.load(self.npy_path, allow_pickle=True)
                        df_c = np.load(self.npy_c_path, allow_pickle=True)
                        _df = pd.DataFrame(_df, columns=df_c)
                        logger.info('缓存文件：{}.{}--包含的{}'.format(self.file_name, self.file_type, _df.columns))
                        return _df
                    else:
                        raise FileNotFoundError
                except FileNotFoundError:
                    _df = pd.ExcelFile(self.excel_path)
                    if len(_df.sheet_names) == 1:
                        df_1 = pd.read_excel(_df, header=0)
                        self.__cache__(df_1)
                        logger.info('原始文件：{}.{}--包含的{}'.format(self.file_name, self.file_type, df_1.columns))
                        return df_1
                    else:
                        logger.info('原始工作簿{}存在多个sheet，如下：\n {}'.format(self.file_name, _df.sheet_names))
                        logger.info('其中[{}]---包含的{}'.format(_df.sheet_names[0], _df.parse(_df.sheet_names[0]).columns))
                        return _df
                except Exception as e:
                    logger.error(e)
                    sys.exit()
            else:
                try:
                    _df = pd.ExcelFile(self.excel_path)
                    if len(_df.sheet_names) == 1:
                        df_1 = pd.read_excel(_df, header=0)
                        self.__cache__(df_1)
                        logger.info('原始文件：{}.{}--包含的{}'.format(self.file_name, self.file_type, df_1.columns))
                        return df_1
                    else:
                        logger.info('原始工作簿{}存在多个sheet，如下：\n {}'.format(self.file_name, _df.sheet_names))
                        logger.info(
                            '其中[{}]---包含的{}'.format(_df.sheet_names[0], _df.parse(_df.sheet_names[0]).columns))
                        return _df
                except Exception as e:
                    logger.error(e)
                    sys.exit()

    def __cache__(self, df):
        col_types = list(set(df.dtypes.astype(str).to_list()))
        for _i in col_types:
            if _i not in ['float64', 'int64']:
                logger.debug('存在无法转换为ndarray的数据类型：{}.直接读取，不做缓存！'.format(_i))
                return 0
        df_c = np.array(df.columns.values)
        data_ndarray = df.to_numpy()
        np.save(self.npy_path, data_ndarray)
        np.save(self.npy_c_path, df_c)

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
               cols: list[str] = []
               ) -> pd.DataFrame:
        if len(cols) == 0:
            return self.df
        else:
            return self.df[cols]


if __name__ == '__main__':
    start_time = time.time()
    # f = pd.ExcelFile(r'D:\Temp\滑动4N-全过程.xlsx')
    aa = ReadData(r'D:\Temp\100g-400g滑动\1N.xlsx').get_df()
    print(aa.head())
    end = time.time() - start_time
    print('总耗时：%s' % end)

    #     df1 = f.parse(sheet_name=i)
    #     df1.drop('Timestamp', axis=1, inplace=True)
    #     df1.to_excel(writer, sheet_name=i)