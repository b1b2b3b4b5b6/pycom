'''
@Author: zhanghao.chen
@Date: 2020-08-01 09:58:24
LastEditors: Please set LastEditors
LastEditTime: 2020-10-16 09:59:06
@Description: file content
'''
# -*- coding:utf-8 -*-

import json
import re
import logging

import collections

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s]%(filename)s[%(lineno)d]:  %(message)s', datefmt='%d/%b/%Y %H:%M:%S')

base_map = {
    'TranslationUnitDecl': 'BaseDecl',
    'TypedefDecl': 'BaseDecl',
    'RecordDecl': 'BaseDecl',
    'CXXRecordDecl': 'BaseDecl',
    'FieldDecl': 'BaseDecl',
    'IndirectFieldDecl': 'BaseDecl',
    'ParmVarDecl': 'BaseDecl',
    'CXXMethodDecl': 'BaseDecl',
    'CXXDestructorDecl': 'BaseDecl',
    'ClassTemplateDecl': 'BaseDecl',
    'TemplateTypeParmDecl': 'BaseDecl',

    'RecordType': 'BaseType',
    'ConstantArrayType': 'BaseType',
    'PointerType': 'BaseType',
    'BuiltinType': 'BaseType',

    'ConstantExpr': 'BaseExpr',

    'IntegerLiteral': 'ToDo'
}


def assert_json_dict_none(json_dict):
    if 0 < len(json_dict.keys()):
        logging.error(f'found left json_dict:\n{json_dict}')


class ToDo():
    def __init__(self, json_dict=''):
        self.json_dict = json_dict


class Loc:
    def __init__(self, json_dict=''):
        if 'file' in json_dict:
            self.file = json_dict['file']
            json_dict.pop('file')
        else:
            self.file = None

        if 'offset' in json_dict:
            self.offset = json_dict['offset']
            json_dict.pop('offset')
        else:
            self.offset = None

        if 'line' in json_dict:
            self.line = json_dict['line']
            json_dict.pop('line')
        else:
            self.line = None

        if 'col' in json_dict:
            self.col = json_dict['col']
            json_dict.pop('col')
        else:
            self.col = None

        if 'tokLen' in json_dict:
            self.tokLen = json_dict['tokLen']
            json_dict.pop('tokLen')
        else:
            self.tokLen = None

        assert_json_dict_none(json_dict)


class _Range:
    def __init__(self, json_dict=''):
        if 'offset' in json_dict:
            self.offset = json_dict['offset']
            json_dict.pop('offset')
        else:
            self.offset = None

        if 'col' in json_dict:
            self.col = json_dict['col']
            json_dict.pop('col')
        else:
            self.col = None

        if 'tokLen' in json_dict:
            self.tokLen = json_dict['tokLen']
            json_dict.pop('tokLen')
        else:
            self.tokLen = None

        assert_json_dict_none(json_dict)


class Range:
    def __init__(self, json_dict=''):
        self.begin = _Range(json_dict['begin'])
        json_dict.pop('begin')
        self.end = _Range(json_dict['end'])
        json_dict.pop('end')

        assert_json_dict_none(json_dict)


class Type:
    def __init__(self, json_dict=''):
        self.qualType = json_dict['qualType']
        json_dict.pop('qualType')

        assert_json_dict_none(json_dict)


class BaseExpr():
    def __init__(self, json_dict=''):
        self.id = json_dict['id']
        json_dict.pop('id')

        self.kind = json_dict['kind']
        json_dict.pop('kind')

        self.type = Type(json_dict['type'])
        json_dict.pop('type')

        assert_json_dict_none(json_dict)


class BaseType():
    def __init__(self, json_dict=''):
        self.id = json_dict['id']
        json_dict.pop('id')

        self.kind = json_dict['kind']
        json_dict.pop('kind')

        self.type = Type(json_dict['type'])
        json_dict.pop('type')

        assert_json_dict_none(json_dict)


class BaseDecl:
    def __init__(self, json_dict=''):
        self.id = json_dict['id']
        json_dict.pop('id')

        self.kind = json_dict['kind']
        json_dict.pop('kind')

        self.loc = Loc(json_dict['loc'])
        json_dict.pop('loc')

        self.range = Range(json_dict['range'])
        json_dict.pop('range')

        if 'name' in json_dict:
            self.name = json_dict['name']
            json_dict.pop('name')
        else:
            self.name = None

        if 'tagUsed' in json_dict:
            self.tagUsed = json_dict['tagUsed']
            json_dict.pop('tagUsed')
        else:
            self.tagUsed = None

        if 'type' in json_dict:
            self.type = Type(json_dict['type'])
            json_dict.pop('type')
        else:
            self.type = None

        if 'completeDefinition' in json_dict:
            self.completeDefinition = json_dict['completeDefinition']
            json_dict.pop('completeDefinition')
        else:
            self.completeDefinition = None

        if 'isImplicit' in json_dict:
            self.isImplicit = json_dict['isImplicit']
            json_dict.pop('isImplicit')
        else:
            self.isImplicit = None

        if 'inner' in json_dict:
            self.inner = parse_inner(json_dict['inner'])
            json_dict.pop('inner')
        else:
            self.inner = None

        assert_json_dict_none(json_dict)


def parse_json_dict(json_dict):
    import importlib
    obj = importlib.import_module('common.ast.base')
    class_obj = getattr(obj, base_map[json_dict['kind']])(json_dict)
    return class_obj


def parse_inner(json_list):
    od = collections.OrderedDict()
    for json_dict in json_list:
        import importlib
        obj = importlib.import_module('common.ast.base')
        class_obj = getattr(obj, base_map[json_dict['kind']])(json_dict)
        od[class_obj.id] = class_obj
    return od
