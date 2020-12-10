'''
Author: your name
Date: 2020-11-25 14:25:10
LastEditTime: 2020-12-09 16:16:08
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \codegen\common\gencode\com.py
'''

import time


def gen_datetime(config, format='default'):
    if format == 'default':
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_str


def gen_upper(config, in_str=''):
    return in_str.upper()
