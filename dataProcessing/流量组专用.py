#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : hesgang
# @Desc : 处理流量数据
import pandas as pd
import time


def drop_1(_df):
    """
    基于特定的Excel表格，剔除不满足下列条件的行
    遍历整个表格
    :param _df: pd.DataFrame
    :return: pd.DataFrame
    """
    # 判断数据类型是否正确
    if not isinstance(_df, pd.DataFrame):
        raise TypeError('Unexpected {}, <pd.Series or pd.DataFrame> is need!'.format(type(_df)))
    for item in _df.index:
        # if语句为判断的条件及列名位置
        if _df['# CH 1'][item] != 1 or _df['# CH 2'][item] != 1:
            _df.drop(item, inplace=True)
    return _df


def drop_3sigma(
        _df: pd.DataFrame,
        col_name: 'str | list[str]'
) -> pd.DataFrame:
    """
    基于特定的Excel表格，对表格某一列或者两列数据进行3sigma处理，并删除3sigma之外的数据
    :param _df: 需要处理的表格
    :param col_name: 列名
    :return: 处理之后的表格
    """
    # 判断数据类型是否正确
    if not isinstance(_df, pd.DataFrame):
        raise TypeError('Unexpected {}, <pd.Series or pd.DataFrame> is need!'.format(type(_df)))

    if type(col_name) == str:
        col_mean = round(_df[col_name].mean(), 10)  # 平均值
        col_std = round(_df[col_name].std(), 10)  # 标准差
        up3sigma = round(col_mean + 3 * col_std, 10)
        down3sigma = round(col_mean - 3 * col_std, 10)
        _df = _df[(_df[col_name] <= up3sigma) | (_df[col_name] >= down3sigma)]
    else:
        for item in col_name:
            col_mean = round(_df[item].mean(), 10)  # 平均值
            col_std = round(_df[item].std(), 10)  # 标准差
            up3sigma = round(col_mean + 3 * col_std, 10)  # 较大3sigma处
            down3sigma = round(col_mean - 3 * col_std, 10)  # 较小3sigma处
            _df = _df[(_df[item] <= up3sigma) | (_df[item] >= down3sigma)]
    return _df


def save_to_excel(_df, ex_writer, sheet_name):
    """
    保存文件，根据需求自己改
    :param _df:
    :param ex_writer:
    :param sheet_name:
    :return:
    """
    # a1 = round(_df['#-0'].mean(), 10)
    # b1 = round(_df['#-0'].std(), 10)
    # c1 = round(a1 + 3 * b1, 10)
    # d1 = round(a1 - 3 * b1, 10)
    # a2 = round(_df['#-1'].mean(), 10)
    # b2 = round(_df['#-1'].std(), 10)
    # c2 = round(a2 + 3 * b2, 10)
    # d2 = round(a2 - 3 * b2, 10)
    # _df.at[0, '#-00'] = a1
    # _df.at[1, '#-00'] = b1
    # _df.at[2, '#-00'] = c1
    # _df.at[3, '#-00'] = d1
    # _df.at[0, '#-01'] = a2
    # _df.at[1, '#-01'] = b2
    # _df.at[2, '#-01'] = c2
    # _df.at[3, '#-01'] = d2
    _df.to_excel(ex_writer, sheet_name=sheet_name, index=False)


if __name__ == '__main__':
    start_time = time.time()
    f = pd.ExcelFile(r'D:\Temp\merge.xlsx')
    writer = pd.ExcelWriter(r'D:\Temp\merge_ok.xlsx')
    for i in f.sheet_names:
        start_time1 = time.time()
        dff = f.parse(i)
        dff = drop_1(dff)
        for ii in range(2):
            dff = drop_3sigma(dff, ['#-0', '#-1'])
        save_to_excel(dff, writer, i)
        print('处理文件：{}-耗时：{}'.format(i, time.time() - start_time1))
    end = time.time() - start_time
    print('处理总耗时：%s' % end)
    writer.close()
    end = time.time() - start_time
    print('总耗时：%s' % end)
