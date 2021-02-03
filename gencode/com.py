'''
Author: your name
Date: 2020-11-25 14:25:10
LastEditTime: 2021-02-03 14:19:26
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \codegen\common\gencode\com.py
'''

import time
import common.tool.codsty as codsty


def gen_datetime(config, format='default'):
    if format == 'default':
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_str


def gen_upper(config, in_str=''):
    return in_str.upper()


def gen_lower(config, in_str=''):
    return in_str.lower()


def gen_uc(config, in_str=''):
    return codsty.sc2ucc(in_str)
