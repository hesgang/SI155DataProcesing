#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/28 19:11 
# @Author : hesgang
# @File : logger.py 

import logging

# 1、创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 2、创建一个handler，用于写入日志文件
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 3、定义handler的输出格式（formatter）
formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

# 4、给handler添加formatter
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 5、给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)


if __name__ == '__main__':
    pass
