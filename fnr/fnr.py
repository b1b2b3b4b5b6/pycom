'''
Author: zhanghao.chen
Date: 2020-09-18 10:53:32
LastEditors: Please set LastEditors
LastEditTime: 2020-12-21 15:34:27
Description: file content
'''

import os
import re
import importlib
import logging
from types import FunctionType


def get_gen_func(gen_name, module_name):
    module = importlib.import_module(module_name)
    func = getattr(module, gen_name, '')
    if '' != func:
        return func

    module = importlib.import_module('common.gencode.com')
    func = getattr(module, gen_name, '')
    if '' != func:
        return func

    logging.error('gen_name[{}] is not define!'.format(gen_name))
    assert(None)


def replace_gen(common_str, rep, config, module_name):

    g = re.search(r'^(\w*)\(([\s\S]*)\)$', rep)
    if g == None:
        logging.error('rep[{}] is illgal'.format(rep))
        assert (None)

    gen_name = g[1]
    if g[2] == '':
        arg_list = []
    else:
        arg_list = g[2].split('$')
    arg_count = len(arg_list)
    logging.debug('{} < [{}][{}]'.format(
        gen_name, '$'.join(arg_list), arg_count))

    func = get_gen_func(gen_name, module_name)

    gen_str = ''
    if arg_count == 0:
        gen_str = func(config)

    if arg_count == 1:
        gen_str = func(config, arg_list[0])

    if arg_count == 2:
        gen_str = func(config, arg_list[0], arg_list[1])

    if arg_count == 3:
        gen_str = func(config, arg_list[0], arg_list[1], arg_list[2])

    if arg_count == 4:
        gen_str = func(config, arg_list[0],
                       arg_list[1], arg_list[2], arg_list[3])
    if arg_count == 5:
        gen_str = func(config, arg_list[0],
                       arg_list[1], arg_list[2], arg_list[3], arg_list[4])
    if arg_count == 6:
        gen_str = func(config, arg_list[0],
                       arg_list[1], arg_list[2], arg_list[3], arg_list[4], arg_list[5])
    if arg_count == 7:
        gen_str = func(config, arg_list[0],
                       arg_list[1], arg_list[2], arg_list[3], arg_list[4], arg_list[5], arg_list[6])
    if arg_count == 8:
        gen_str = func(config, arg_list[0],
                       arg_list[1], arg_list[2], arg_list[3], arg_list[4], arg_list[5], arg_list[6], arg_list[7])

    common_str = common_str.replace(
        '[[[{}]]]'.format(rep), gen_str)
    return common_str


def exec_func(code):
    foo_code = compile(code, "<string>", "exec")
    foo_func = FunctionType(foo_code.co_consts[0], globals(), "foo")

    return foo_func()


def replace(common_str, config, module_name):
    while True:
        offset = common_str.rfind('[[[')
        if offset == -1:
            return common_str
        res = re.findall(r'\[\[\[([\s\S]*?)\]\]\]', common_str[offset:])
        if len(res) <= 0:
            logging.error(common_str[offset - 20:offset + 20])
            logging.error('code str still have [[[ or ]]]')
            assert (None)
            return common_str

        for rep in res:
            if rep.find('[[[') > 0 or rep.find('[[[') > 0:
                logging.error('rep[{}] is not regular'.format(rep))
                assert (None)
            logging.debug('handle rep[{}]'.format(rep))
            g = re.search(r'^(\w*)\(([\s\S]*)\)$', rep)
            if g == None:
                logging.error('rep[{}] is not regular'.format(rep))
                assert (None)
            rep_name = g[1]
            rep_arg = g[2]

            if rep_name == 'snippet':
                common_str = common_str.replace('[[[{}]]]'.format(rep), open(
                    '{}.txt'.format(config['config']['template_path']+rep_arg), encoding='utf-8').read())
                break
            elif rep_name == 'flow':
                flow_val = config['config']['flow'][rep_arg]
                common_str = common_str.replace('[[[{}]]]'.format(rep), open(
                    '{}.txt'.format(config['config']['template_path']+flow_val), encoding='utf-8').read())
                break
            elif rep_name[0:4] == 'gen_':
                common_str = replace_gen(common_str, rep, config, module_name)
                break
            elif rep_name == 'field':
                common_str = common_str.replace(
                    '[[[{}]]]'.format(rep), config['config']['field'][rep_arg])
                break
            elif rep_name == 'exec':
                common_str = common_str.replace(
                    '[[[{}]]]'.format(rep), exec_func(rep_arg))
                break

            logging.error('rep[{}] is not be defined'.format(rep))
            assert (None)
