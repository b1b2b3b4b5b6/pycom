'''
Author: your name
Date: 2020-10-21 15:14:39
LastEditTime: 2020-10-21 15:32:04
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \codegen\common\tool\codsty.py
'''


import re
import os
import logging
import platform


def sc2ucc(name):
    if name == '':
        return ''
    name = name.lower()
    name_list = name.split('_')
    for i in range(len(name_list)):
        name_list[i] = name_list[i].capitalize()
    out_name = ''
    for line in name_list:
        out_name = out_name + line
    return out_name


# print(sc2ucc('asdjfajs'))
# print(sc2ucc(''))
# print(sc2ucc('aasfd_alsdf'))
# print(sc2ucc('aasfd_'))
# print(sc2ucc('_aasfd'))
# print(sc2ucc('_'))
