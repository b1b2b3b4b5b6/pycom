'''
@Author: zhanghao.chen
@Date: 2020-07-29 14:06:25
LastEditors: Please set LastEditors
LastEditTime: 2020-12-21 16:05:16
@Description: file content
'''

# -*- coding:utf-8 -*-
import os
import re
import string
import shutil
import logging
import common.tool.tool as tool
import common.prasecpp.base as base

# 去行前空白符，行后空白符，行中空白符合并成一个空格


class Declares:
    def __init__(self, typedef_struct={}, struct={}):
        self.typedef_struct = typedef_struct
        self.struct = struct


def get_typedef_struct(str_in):
    struct_dict = {}
    res = re.findall(
        r'typedef struct[\s\S]*?\{\n[\s\S]*?\}.*;', str_in)
    for val in res:
        logging.debug('struct str is \r{}'.format(val))
        struct = base.TypedefStruct(val)
        for val in struct.typedef_name_list:
            struct_dict[val] = struct
    logging.info('typedef struct conut: {0}'.format(len(struct_dict)))
    return struct_dict


def get_struct(str_in):
    struct_dict = {}
    res = re.findall(r'(?<!typedef )struct[\s\S]*?\{\n[\s\S]*?\}.*;', str_in)
    for val in res:
        s = base.Struct(val)
        struct_dict[s.name] = s
    logging.info('struct conut: {0}'.format(len(struct_dict)))
    return struct_dict


def parse_file(file_name, encoding_str, is_clean_comment=True):
    fp = open(file_name, encoding=encoding_str)
    code_str = fp.read()
    fp.close()
    if True == is_clean_comment:
        code_str = tool.clean_comment(code_str)

    fp = open('__temp__.cpp', 'w+', encoding='gb2312')
    fp.write(code_str)
    fp.close()
    tool.format_file('__temp__.cpp')

    fp = open('__temp__.cpp', 'r', encoding='gb2312')
    code_str = fp.read()
    fp.close()

    os.remove('__temp__.cpp')

    typedef_struct_dict = get_typedef_struct(code_str)
    struct = get_struct(code_str)
    return Declares(typedef_struct=typedef_struct_dict, struct=struct)
