'''
@Author: zhanghao.chen
@Date: 2020-08-01 09:58:24
LastEditors: Please set LastEditors
LastEditTime: 2020-10-16 09:59:06
@Description: file content
'''
# -*- coding:utf-8 -*-

import re
import logging
import common.tool.tool as tool


def str2val(in_str):
    if in_str == '':
        return Variable()

    g = re.search(r'(^(?:\w+ )+\**)(\w+)((?:\[.*)*);(?:\s*//(.*))*', in_str)
    if g:
        front = g.group(1)
        name = g.group(2)
        if g.group(3):
            tail = g.group(3)
        else:
            tail = ''
        if g.group(4):
            comment = g.group(4)
        else:
            comment = ''
        type_name = TypeName(front.strip(), tail.strip())
        val = Variable(name, type_name, comment)
        return val
    else:
        logging.error('[{0}] can not be parse'.format(in_str))
        assert(None)


def list2val_dict(in_list):
    str_list = in_list.copy()
    member_dict = {}
    for line in str_list:
        val = str2val(line)
        member_dict[val.name] = val

    return member_dict


def get_struct_typedef_name(in_str):
    g = re.search(r'([^ ]*), ([^ ]*), ([^ ]*)$', in_str)
    if g:
        return [g.group(1), g.group(2), g.group(3)]

    g = re.search(r'([^ ]*), ([^ ]*)$', in_str)
    if g:
        return [g.group(1), g.group(2)]

    g = re.search(r'([^ ]*)$', in_str)
    if g:
        return [g.group(1)]
    logging.fatal(in_str + ' can not find typedef name')
    assert None
    return []


class TypeName:
    def __init__(self, front='', tail=''):
        self.name = front
        self.tail = tail
        if tail.find('[') != -1:
            self.type = front + '[]'
        else:
            self.type = front

    def __str__(self):
        return '{0} ,{1}'.format(self.name, self.tail)


class Variable:
    def __init__(self, name='', type_name=TypeName(), comment=''):
        self.name = name
        self.type_name = type_name
        self.comment = comment

    def __str__(self):
        type_name = self.type_name.__str__()
        out_str = type_name.replace(',', self.name)
        if len(self.comment):
            out_str += '//' + self.comment
        return out_str


class Struct:
    def __init__(self, str_in):
        g = re.search(
            r'(?<!typedef )struct([\s\S]*?)\{\n([\s\S]*?)\}(.*);', str_in)
        assert g
        self.name = g.group(1).strip()
        temp_list = g.group(2).split('\n')
        in_list = []
        for line in temp_list:
            line = tool.trim(line)
            line = line.strip()
            if line != '':
                in_list.append(line)
        self.member_dict = list2val_dict(in_list)

    def __str__(self):
        out_str = 'struct ' + self.name + '\n' + '{\n'
        for key in self.member_dict:
            out_str = out_str + '\t' + self.member_dict[key].__str__() + '\n'
        out_str = out_str + '};'
        return out_str


class TypedefStruct:

    def __init__(self, str_in):

        g = re.search(
            r'typedef struct([\s\S]*?)\{\n([\s\S]*?)\}(.*);', str_in)
        assert g
        self.origin_name = g.group(1).strip()
        temp_list = g.group(2).split('\n')
        in_list = []
        for line in temp_list:
            line = tool.trim(line)
            line = line.strip()
            if line != '':
                in_list.append(line)
        self.member_dict = list2val_dict(in_list)
        self.typedef_name_list = get_struct_typedef_name(g.group(3))

    def __str__(self):
        out_str = 'typedef struct ' + self.origin_name + '\n' + '{\n'
        for key in self.member_dict:
            out_str = out_str + '\t' + self.member_dict[key].__str__() + '\n'
        out_str = out_str + '} '
        out_str = out_str + ','.join(self.typedef_name_list) + ';'
        return out_str
