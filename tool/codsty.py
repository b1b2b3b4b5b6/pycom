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


def ucc2sc(name):
    out_name = ''
    last = 'a'
    for c in name:
        if c.isupper() and last.islower():
            out_name += '_'
        out_name += c
        last = c
    out_name = out_name.strip('_')

    if len(out_name) >= 3:
        name = out_name
        out_name = ''
        for n in range(len(name) - 2):
            if name[n].isupper() and name[n+1].isupper() and name[n+2].islower():
                out_name += name[n]
                out_name += '_'
            else:
                out_name += name[n]
        out_name += name[-2]
        out_name += name[-1]
    out_name = out_name.upper()
    return out_name
    # print(sc2ucc('asdjfajs'))
    # print(sc2ucc(''))
    # print(sc2ucc('aasfd_alsdf'))
    # print(sc2ucc('aasfd_'))
    # print(sc2ucc('_aasfd'))
    # print(sc2ucc('_'))
