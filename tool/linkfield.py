'''
Author: zhanghao.chen
Date: 2020-09-04 19:41:23
LastEditors: Please set LastEditors
LastEditTime: 2020-12-01 10:41:52
Description: file content
'''
import logging
import common.tool.tool as tool
import common.tool.codsty as codsty
import re
import common.prasecpp.base as prasecpp
import csv


def insert_sql2dict(in_str):
    in_str = in_str.replace('\\', ' ')
    in_str = in_str.replace('\r\n', ' ')
    in_str = in_str.replace('\n', ' ')
    in_str = tool.trim(in_str)

    g = re.search(r'insert .* \((.*?)\) values \((.*?)\)', in_str)

    name_list = g.group(1).split(',')
    for n in range(len(name_list)):
        name_list[n] = tool.trim(name_list[n])
        name_list[n] = codsty.sc2ucc(name_list[n])

    num_list = g.group(2).split(',')
    for n in range(len(num_list)):
        num_list[n] = num_list[n].replace(':', ' ')
        num_list[n] = tool.trim(num_list[n])

    assert(len(name_list) == len(num_list))

    out_dict = dict(zip(name_list, num_list))
    return out_dict


def update_sql2dict(in_str):
    in_str = in_str.replace('\\', ' ')
    in_str = in_str.replace('\r\n', ' ')
    in_str = in_str.replace('\n', ' ')
    in_str = tool.trim(in_str)

    g = re.search(r'update \w* (\w*) set', in_str)
    name = g.group(1)

    format = r'{}.(\w*?)\s*=\s*:\s*(\d*)'.format(name)

    res = re.findall(format, in_str)

    out_dict = {}
    for val in res:
        name = val[0]
        name = codsty.sc2ucc(name)
        num = val[1]
        out_dict[name] = num
    return out_dict


def database_cmd2dict(in_str):
    in_str = tool.clean_comment(in_str)
    in_list = in_str.split('\n')

    out_dict = {}
    for line in in_list:
        line = tool.trim(line)
        if line == '':
            continue
        g = re.search(
            r'm_database_command.Param\((\d*)\).* = (.*?);', line)
        out_dict[tool.trim(g.group(1))] = tool.trim(g.group(2))

    return out_dict


def st2dict(in_str):
    out_list = in_str.split('\n')
    out_dict = {}
    for line in out_list:
        line = tool.trim(line)
        if line == '':
            continue
        val = prasecpp.str2val(line)
        out_dict[line] = val.name

    return out_dict


def str2dict(in_str, left_format=r'.*', right_format=r'.*'):
    out_dict = {}
    str_list = in_str

    for line in str_list:
        line = tool.trim(line)
        if line == '':
            continue
        gl = re.search(left_format, line)
        gr = re.search(right_format, line)
        out_dict[gl.group(1)] = gr.group(1)
    return out_dict


def dictlink(dict1, dict2, dict2_allow_remain=False, dict1_allow_remain=False):
    dict2_t = dict2
    out_dict = {}
    out_dict.clear()
    for key, val in dict1.items():
        if val in dict2_t.keys():
            out_dict[key] = dict2[val]
            dict2_t.pop(val)
        else:
            if dict1_allow_remain == False:
                out_dict[key] = ''
            else:
                out_dict[key] = val
    if dict2_allow_remain == False:
        if len(dict2_t) > 0:
            logging.error('dict link faild, dict has remain')
            print(dict2_t)
            assert(None)
    return (out_dict, dict2_t)


def invert_dict(dic):
    inverted_dict = dict(map(reversed, dic.items()))
    return inverted_dict


def dict_dump(file_name, in_dict):
    header = ['key', 'val']
    d = []
    for key, val in in_dict.items():
        dt = {}
        dt['key'] = key
        dt['val'] = val
        d.append(dt)

    fp = open(file_name, 'w+', encoding='utf-8', newline='')
    writer = csv.DictWriter(fp, fieldnames=header)
    writer.writeheader()
    writer.writerows(d)
    fp.close()
