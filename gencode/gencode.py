'''
@Author: zhanghao.chen
@Date: 2020-08-03 13:21:46
LastEditors: zhanghao.chen
LastEditTime: 2020-09-23 10:52:57
@Description: file content
'''

import logging
import sys
import os
import common.tool.tool as tool


def get_format_str(type_name):
    type_dict = {
        'char': '%c',
        'char *': '%s',
        'char[]': '%s',
        'short': '%d',
        'unsigned short': '%ud',
        'int': '%d',
        'unsigned int': '%ud',
        'u16': '%ud',
        'u32':  '%uld',
        'u64': '%ulld',
        'INT32': '%ld',
        'INT64': '%lld',
        'float': '%f',
        'double': '%f'
    }
    if type_name in type_dict:
        return type_dict[type_name]
    else:
        logging.fatal(type_name + ' is not exist!')
        assert None


def member_format(member_dict, prefix='default_prefix.'):
    format_list = []
    arg_list = []
    print(member_dict)
    for val in member_dict.values():
        name = val.name
        type_name = val.type_name.type
        format_list.append(name + '[' + get_format_str(type_name) + ']')
        arg_list.append(prefix + name)
    return format_list, arg_list


default_dict = {
    # same type val copy
    ('char', 'char'): {'format': '{0} = {1};'},
    ('char *', 'char *'): {'format': 'STRNCPY({0}, NULL2SPACE({1}));'},
    ('char[]', 'char[]'): {'format': 'STRNCPY({0}, NULL2SPACE({1}));'},
    ('short', 'short'): {'format': '{0} = {1};'},
    ('unsigned short', 'unsigned short'): {'format': '{0} = {1};'},
    ('int', 'int'): {'format': '{0} = {1};'},
    ('unsigned int', 'unsigned int'): {'format': '{0} = {1};'},
    ('u16', 'u16'): {'format': '{0} = {1};'},
    ('u32', 'u32'): {'format': '{0} = {1};'},
    ('u64', 'u64'): {'format': '{0} = {1};'},
    ('INT32', 'INT32'): {'format': '{0} = {1};'},
    ('INT64', 'INT64'): {'format': '{0} = {1};'},
    ('float', 'float'): {'format': '{0} = {1};'},
    ('double', 'double'): {'format': '{0} = {1};'},

    # indicate default val copy
    ('char', ''): {'format': '{0} = {1};\t//assign default value'},
    ('char *', ''): {'format': 'STRNCPY({0}, {1});\t//assign default value'},
    ('char[]', ''): {'format': 'STRNCPY({0}, {1});\t//assign default value'},
    ('short', ''): {'format': '{0} = {1};\t//assign default value'},
    ('unsigned ', ''): {'format': '{0} = {1};\t//assign default value'},
    ('int', ''): {'format': '{0} = {1};\t//assign default value'},
    ('unsigned ', ''): {'format': '{0} = {1};\t//assign default value'},
    ('u16', ''): {'format': '{0} = {1};\t//assign default value'},
    ('u32', ''): {'format': '{0} = {1};\t//assign default value'},
    ('u64', ''): {'format': '{0} = {1};\t//assign default value'},
    ('INT32', ''): {'format': '{0} = {1};\t//assign default value'},
    ('INT64', ''): {'format': '{0} = {1};\t//assign default value'},
    ('float', ''): {'format': '{0} = {1};\t//assign default value'},
    ('double', ''): {'format': '{0} = {1};\t//assign default value'},


    # different type val copy,char *,char[]
    ('char[]', 'char'): {'format': '{0}[0] = {1};\t//char to char[]'},
    ('char *', 'char'): {'format': '{0}[0] = {1};\t//char to char*'},


    # different type val copy,num
    ('INT64', 'int'): {'format': '{0} = {1};\t//int to INT64'},
    ('int', 'unsigned short'): {'format': '{0} = {1};\t//unsigned short to int'},
    ('int', 'char'): {'format': '{0} = {1};\t//char to int! please check [char] meaning'},
}


def val_copy(left_type, right_type, left_rep, right_rep, copy_dict=default_dict, comment=''):

    type_pair = (left_type, right_type)
    if type_pair in copy_dict:
        out_str = copy_dict[type_pair]['format'].format(left_rep, right_rep)

        if len(comment):
            out_str = tool.append_comment(out_str, comment)
        return out_str
    else:
        logging.fatal('{0} is not in copy dict'.format(type_pair))
        assert None
