'''
@Author: zhanghao.chen
@Date: 2020-08-01 16:23:15
LastEditors: b1b2b3b4b5b6 a1439458305@163.com
LastEditTime: 2022-11-16 10:28:51
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


def dump_memery(file_list, encoding='utf-8'):
    import subprocess
    sys_str = platform.system()
    if sys_str == "Windows":
        file_arg = ' '
        for file in file_list:
            file = file.replace('/', '\\')
            file_arg += f'\"{file}\" '
        res = subprocess.run(
            fr'common\tool\bin\windows\clang.exe -std=c++17 -Xclang -fdump-record-layouts {file_arg}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding)

    elif sys_str == "Linux":
        res = subprocess.run(
            ['clang', '-std=c++17', '-Xclang', '-fdump-record-layouts', *file_list], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding)

    else:
        logging.error(f'unknow system[{sys_str}]')
        exit(-1)

    if res.returncode != 0:
        logging.error(f'cmd[{res.args}] exec fail[{res.stderr}]')

    return res.stdout


def get_mem_by_class(data, class_name):
    logging.debug(f'try to find {class_name}')
    g = re.search(
        rf'(\*\*\* Dumping AST Record Layout\n\s+0 \| class {class_name}.*?\n)\n', data, re.DOTALL)
    if g is None:
        logging.error(f'can not find {class_name} mem')
        return None
    return g.group(1)


def ast_dump_all(file_list, encoding='utf-8'):
    import subprocess
    sys_str = platform.system()
    if sys_str == "Windows":
        file_arg = ' '
        for file in file_list:
            file = file.replace('/', '\\')
            file_arg += f'\"{file}\" '
        res = subprocess.run(
            fr'common\tool\bin\windows\clang.exe -cc1 -triple x86_64-unknown-unknown -ast-dump-all=json {file_arg}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding)

    elif sys_str == "Linux":
        res = subprocess.run(
            ['clang', '-cc1', '-triple', 'x86_64-unknown-unknown', '-std=gnu++17', '-ast-dump-all=json', *file_list], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding)

    else:
        logging.error(f'unknow system[{sys_str}]')
        exit(-1)

    if res.returncode != 0:
        logging.error(f'cmd[{res.args}] exec fail[{res.stderr}]')

    return res.stdout


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
