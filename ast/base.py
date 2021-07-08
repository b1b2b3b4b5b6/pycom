'''
@Author: zhanghao.chen
@Date: 2020-08-01 09:58:24
LastEditors: Please set LastEditors
LastEditTime: 2020-10-16 09:59:06
@Description: file content
'''
# -*- coding:utf-8 -*-

import json
import logging
import importlib
import dict_recursive_update
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

    'ConstantExpr': 'ToDo',

    'IntegerLiteral': 'ToDo'
}


def assert_json_dict_none(json_dict):
    if 0 < len(json_dict.keys()):
        logging.error(f'found left json_dict:\n{json_dict}\n')


class Base(object):
    def __init__(self):
        pass

    def get_restore_dict(self) -> str:
        attr_list = self.__dir__()
        out_dict = {}
        for k in attr_list:
            if k.find('__') >= 0:
                continue
            v = getattr(self, k)

            if callable(v):
                continue

            if v != None:
                if isinstance(v, list):
                    temp_list = []
                    for obj in v:
                        temp_list.append(obj.get_restore_dict())
                    out_dict[k] = temp_list
                elif isinstance(v, (str, bool, int)):
                    out_dict[k] = v
                elif isinstance(v, dict):
                    dict_recursive_update.recursive_update(out_dict, v)
                else:
                    out_dict[k] = v.get_restore_dict()
        return out_dict


class ToDo(Base):
    def __init__(self, json_dict=''):
        self.id = json_dict['id']
        self.json_dict = json_dict


class Loc(Base):
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


class Range(Base):
    def __init__(self, json_dict=''):
        class _Range(Base):
            def __init__(self, json_dict=''):
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

        self.begin = _Range(json_dict['begin'])
        json_dict.pop('begin')
        self.end = _Range(json_dict['end'])
        json_dict.pop('end')

        assert_json_dict_none(json_dict)


class Type(Base):
    def __init__(self, json_dict=''):
        self.qualType = json_dict['qualType']
        json_dict.pop('qualType')

        if 'desugaredQualType' in json_dict:
            self.desugaredQualType = json_dict['desugaredQualType']
            json_dict.pop('desugaredQualType')
        else:
            self.desugaredQualType = None

        assert_json_dict_none(json_dict)


class BaseType(Base):
    def __init__(self, json_dict=''):
        self.id = json_dict['id']
        json_dict.pop('id')

        self.kind = json_dict['kind']
        json_dict.pop('kind')

        self.type = Type(json_dict['type'])
        json_dict.pop('type')

        if 'decl' in json_dict:
            self.decl = BaseDecl(json_dict['decl'])
            json_dict.pop('decl')
        else:
            self.decl = None

        if 'size' in json_dict:
            self.size = json_dict['size']
            json_dict.pop('size')
        else:
            self.size = None

        if 'inner' in json_dict:
            self.inner = parse_obj(json_dict['inner'])
            json_dict.pop('inner')
        else:
            self.inner = None

        assert_json_dict_none(json_dict)


class BaseDecl(Base):
    def __init__(self, json_dict=''):
        class DefinitionData(Base):
            def __init__(self, json_dict=''):
                if 'canConstDefaultInit' in json_dict:
                    self.canConstDefaultInit = json_dict['canConstDefaultInit']
                    json_dict.pop('canConstDefaultInit')
                else:
                    self.canConstDefaultInit = None

                if 'canPassInRegisters' in json_dict:
                    self.canPassInRegisters = json_dict['canPassInRegisters']
                    json_dict.pop('canPassInRegisters')
                else:
                    self.canPassInRegisters = None

                if 'hasVariantMembers' in json_dict:
                    self.hasVariantMembers = json_dict['hasVariantMembers']
                    json_dict.pop('hasVariantMembers')
                else:
                    self.hasVariantMembers = None

                if 'isAggregate' in json_dict:
                    self.isAggregate = json_dict['isAggregate']
                    json_dict.pop('isAggregate')
                else:
                    self.isAggregate = None

                if 'isLiteral' in json_dict:
                    self.isLiteral = json_dict['isLiteral']
                    json_dict.pop('isLiteral')
                else:
                    self.isLiteral = None

                if 'isPOD' in json_dict:
                    self.isPOD = json_dict['isPOD']
                    json_dict.pop('isPOD')
                else:
                    self.isPOD = None

                if 'isStandardLayout' in json_dict:
                    self.isStandardLayout = json_dict['isStandardLayout']
                    json_dict.pop('isStandardLayout')
                else:
                    self.isStandardLayout = None

                if 'isTrivial' in json_dict:
                    self.isTrivial = json_dict['isTrivial']
                    json_dict.pop('isTrivial')
                else:
                    self.isTrivial = None

                if 'isTriviallyCopyable' in json_dict:
                    self.isTriviallyCopyable = json_dict['isTriviallyCopyable']
                    json_dict.pop('isTriviallyCopyable')
                else:
                    self.isTriviallyCopyable = None

                if 'hasConstexprNonCopyMoveConstructor' in json_dict:
                    self.hasConstexprNonCopyMoveConstructor = json_dict[
                        'hasConstexprNonCopyMoveConstructor']
                    json_dict.pop('hasConstexprNonCopyMoveConstructor')
                else:
                    self.hasConstexprNonCopyMoveConstructor = None

                if 'isEmpty' in json_dict:
                    self.isEmpty = json_dict[
                        'isEmpty']
                    json_dict.pop('isEmpty')
                else:
                    self.isEmpty = None

                class _DefinitionData(Base):
                    def __init__(self, json_dict):
                        if 'hasConstParam' in json_dict:
                            self.hasConstParam = json_dict['hasConstParam']
                            json_dict.pop('hasConstParam')
                        else:
                            self.hasConstParam = None

                        if 'implicitHasConstParam' in json_dict:
                            self.implicitHasConstParam = json_dict['implicitHasConstParam']
                            json_dict.pop('implicitHasConstParam')
                        else:
                            self.implicitHasConstParam = None

                        if 'needsImplicit' in json_dict:
                            self.needsImplicit = json_dict['needsImplicit']
                            json_dict.pop('needsImplicit')
                        else:
                            self.needsImplicit = None

                        if 'simple' in json_dict:
                            self.simple = json_dict['simple']
                            json_dict.pop('simple')
                        else:
                            self.simple = None

                        if 'trivial' in json_dict:
                            self.trivial = json_dict['trivial']
                            json_dict.pop('trivial')
                        else:
                            self.trivial = None

                        if 'defaultedIsConstexpr' in json_dict:
                            self.defaultedIsConstexpr = json_dict['defaultedIsConstexpr']
                            json_dict.pop('defaultedIsConstexpr')
                        else:
                            self.defaultedIsConstexpr = None

                        if 'exists' in json_dict:
                            self.exists = json_dict['exists']
                            json_dict.pop('exists')
                        else:
                            self.exists = None

                        if 'irrelevant' in json_dict:
                            self.irrelevant = json_dict['irrelevant']
                            json_dict.pop('irrelevant')
                        else:
                            self.irrelevant = None

                        if 'isConstexpr' in json_dict:
                            self.isConstexpr = json_dict['isConstexpr']
                            json_dict.pop('isConstexpr')
                        else:
                            self.isConstexpr = None

                        if 'nonTrivial' in json_dict:
                            self.nonTrivial = json_dict['nonTrivial']
                            json_dict.pop('nonTrivial')
                        else:
                            self.nonTrivial = None

                        assert_json_dict_none(json_dict)

                if 'copyAssign' in json_dict:
                    self.copyAssign = _DefinitionData(json_dict['copyAssign'])
                    json_dict.pop('copyAssign')
                else:
                    self.copyAssign = None

                if 'copyCtor' in json_dict:
                    self.copyCtor = _DefinitionData(json_dict['copyCtor'])
                    json_dict.pop('copyCtor')
                else:
                    self.copyCtor = None

                if 'defaultCtor' in json_dict:
                    self.defaultCtor = _DefinitionData(
                        json_dict['defaultCtor'])
                    json_dict.pop('defaultCtor')
                else:
                    self.defaultCtor = None

                if 'dtor' in json_dict:
                    self.dtor = _DefinitionData(json_dict['dtor'])
                    json_dict.pop('dtor')
                else:
                    self.dtor = None

                if 'moveAssign' in json_dict:
                    self.moveAssign = _DefinitionData(json_dict['moveAssign'])
                    json_dict.pop('moveAssign')
                else:
                    self.moveAssign = None

                if 'moveCtor' in json_dict:
                    self.moveCtor = _DefinitionData(json_dict['moveCtor'])
                    json_dict.pop('moveCtor')
                else:
                    self.moveCtor = None

                assert_json_dict_none(json_dict)

        class _Bases(Base):
            def __init__(self, json_dict):
                if 'access' in json_dict:
                    self.access = json_dict['access']
                    json_dict.pop('access')
                else:
                    self.access = None

                if 'isPackExpansion' in json_dict:
                    self.isPackExpansion = json_dict['isPackExpansion']
                    json_dict.pop('isPackExpansion')
                else:
                    self.isPackExpansion = None

                if 'type' in json_dict:
                    self.type = Type(json_dict['type'])
                    json_dict.pop('type')
                else:
                    self.type = None

                if 'isVirtual' in json_dict:
                    self.isVirtual = json_dict['isVirtual']
                    json_dict.pop('isVirtual')
                else:
                    self.isVirtual = None

                if 'writtenAccess' in json_dict:
                    self.writtenAccess = json_dict['writtenAccess']
                    json_dict.pop('writtenAccess')
                else:
                    self.writtenAccess = None

                assert_json_dict_none(json_dict)

        self.id = json_dict['id']
        json_dict.pop('id')

        self.kind = json_dict['kind']
        json_dict.pop('kind')

        if 'loc' in json_dict:
            self.loc = Loc(json_dict['loc'])
            json_dict.pop('loc')
        else:
            self.loc = None

        if 'range' in json_dict:
            self.range = Range(json_dict['range'])
            json_dict.pop('range')
        else:
            self.range = None

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

        if 'mangledName' in json_dict:
            self.mangledName = json_dict['mangledName']
            json_dict.pop('mangledName')
        else:
            self.mangledName = None

        if 'inline' in json_dict:
            self.inline = json_dict['inline']
            json_dict.pop('inline')
        else:
            self.inline = None

        if 'constexpr' in json_dict:
            self.constexpr = json_dict['constexpr']
            json_dict.pop('constexpr')
        else:
            self.constexpr = None

        if 'isReferenced' in json_dict:
            self.isReferenced = json_dict['isReferenced']
            json_dict.pop('isReferenced')
        else:
            self.isReferenced = None

        if 'explicitlyDefaulted' in json_dict:
            self.explicitlyDefaulted = json_dict['explicitlyDefaulted']
            json_dict.pop('explicitlyDefaulted')
        else:
            self.explicitlyDefaulted = None

        if 'depth' in json_dict:
            self.depth = json_dict['depth']
            json_dict.pop('depth')
        else:
            self.depth = None

        if 'isParameterPack' in json_dict:
            self.isParameterPack = json_dict['isParameterPack']
            json_dict.pop('isParameterPack')
        else:
            self.isParameterPack = None

        if 'isBitfield' in json_dict:
            self.isBitfield = json_dict['isBitfield']
            json_dict.pop('isBitfield')
        else:
            self.isBitfield = None

        if 'index' in json_dict:
            self.index = json_dict['index']
            json_dict.pop('index')
        else:
            self.index = None

        if 'definitionData' in json_dict:
            self.definitionData = DefinitionData(json_dict['definitionData'])
            json_dict.pop('definitionData')
        else:
            self.definitionData = None

        if 'previousDecl' in json_dict:
            self.previousDecl = json_dict['previousDecl']
            json_dict.pop('previousDecl')
        else:
            self.previousDecl = None

        def parse_bases(obj) -> _Bases:
            l = []
            for json_dict in obj:
                class_obj = _Bases(json_dict)
                l.append(class_obj)
            return l

        if 'bases' in json_dict:
            self.bases = parse_bases(json_dict['bases'])
            json_dict.pop('bases')
        else:
            self.bases = None

        if 'inner' in json_dict:
            self.inner = parse_obj(json_dict['inner'])
            json_dict.pop('inner')
        else:
            self.inner = None

        assert_json_dict_none(json_dict)


def parse_obj(obj) -> Base:
    if isinstance(obj, list):
        l = []
        for json_dict in obj:
            obj = importlib.import_module('common.ast.base')
            class_obj = getattr(obj, base_map[json_dict['kind']])(json_dict)
            l.append(class_obj)
        return l

    if isinstance(obj, dict):
        md = importlib.import_module('common.ast.base')
        class_obj = getattr(md, base_map[obj['kind']])(obj)
        return class_obj

    logging.error(f'unknow obj:\n{obj}\n')
