'''
Author: your name
Date: 2022-02-21 10:08:46
LastEditTime: 2022-02-24 15:42:22
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \codegen\common\tests\test_ast.py
'''
from copy import deepcopy
import unittest

from deepdiff.serialization import pretty_print_diff
import common.ast.base as base
import json
import common.tool.tool as tool
from deepdiff import DeepDiff


class CaseAst(unittest.TestCase):
    def test_records(self):
        json_str = tool.ast_dump_all(
            ['common/tests/llvm-project/clang/test/AST/ast-dump-records.cpp'], encoding='utf-8')
        ori_json_obj = json.loads(json_str)
        new_json_obj = base.parse_jsonobj(
            deepcopy(ori_json_obj)).get_restore_dict()

        res = DeepDiff(ori_json_obj, new_json_obj, ignore_order=True)
        self.assertEqual(res, {}, msg=f'diff res: {res}')
