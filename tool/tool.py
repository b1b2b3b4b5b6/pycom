'''
@Author: zhanghao.chen
@Date: 2020-08-01 16:23:15
LastEditors: Please set LastEditors
LastEditTime: 2021-01-15 10:19:05
@Description: file content
'''
import re
import os
import logging
import platform
import glob
import shutil
import csv


def trim(str):
    str, _ = re.subn(r"^\s*", "", str)
    str, _ = re.subn(r"\s*$", "", str)
    str, _ = re.subn(r"\s+", " ", str)
    return str


def clean_comment(str_in):
    code_str = re.sub(r'\/\*(\s|.)*?\*\/', '', str_in)
    code_str = re.sub(r'\r\n', '\n', code_str)
    code_str = re.sub(r'\/\/.*', '', code_str)
    code_list = code_str.split("\n")
    out_list = []
    for line in code_list:
        g = re.search(r'^\s*$', line)
        if g == None:
            line = trim(line)
            out_list.append(line + '\n')
    out_str = ""
    for line in out_list:
        out_str += line
    return out_str


def replace_define(str_in):
    res = re.findall(r'#define (\w*) (.*)', str_in)
    define_list = {}
    for val in res:
        logging.debug(val)
        define_list[val[0]] = val[1]
    for k, v in define_list.items():
        str_in = str_in.replace(k, v)
    return str_in


def append_comment(str_in, comment_str):
    offset = str_in.find('//')

    if offset >= 0:
        str_in = str_in.replace('//', '//{} | '.format(comment_str))
    else:
        str_in = '{}\t//{}'.format(str_in, comment_str)

    return str_in


def format_file(file_path):
    sys_str = platform.system()
    if sys_str == "Windows":
        os.system(fr'common\tool\bin\windows\clang-format.exe -i {file_path}')
    elif sys_str == "Linux":
        os.system(f'clang-format -i {file_path}')
    else:
        logging.error(f'unknow system[{sys_str}]')
        exit(-1)


def ast_dump_all(file_list, encoding='gb18030'):
    import subprocess
    sys_str = platform.system()
    if sys_str == "Windows":
        file_arg = ' '
        for file in file_list:
            file = file.replace('/', '\\')
            file_arg += f'\"{file}\" '
        res = subprocess.run(
            fr'common\tool\bin\windows\clang.exe -cc1 -triple x86_64-unknown-unknown -ast-dump-all=json {file_arg}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding)
        if res.returncode != 0:
            logging.error(f'cmd[f{res.args}] exec fail[{res.stderr}]')

        return res.stdout

    elif sys_str == "Linux":
        None
    else:
        logging.error(f'unknow system[{sys_str}]')
        exit(-1)


def glob_copy(src_rep, dst):
    file_list = glob.glob(src_rep)
    for file_name in file_list:
        shutil.copy(file_name, dst)


def list2csv(in_list, file_name, header=None):

    if header != None and len(in_list) > 0 and len(in_list[0]) != len(header):
        logging.error(
            'header[{}] is illgle, first line is [{}]'.format(header, in_list[0]))
        return

    fp = open(file_name, '+w', encoding='utf-8', newline='')
    writer = csv.writer(fp)

    if header != None:
        writer.writerow(header)
    writer.writerows(in_list)
    fp.close()
