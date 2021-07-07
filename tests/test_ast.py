import unittest
import common.ast.base as base
import json
import common.tool.tool as tool


class CaseAst(unittest.TestCase):
    def test_recode_decl(self):
        json_str = tool.ast_dump_all(
            ['common/tests/llvm-project/clang/test/AST/ast-dump-records.cpp'], encoding='utf-8')
        fp = open('temp.json', 'w')
        fp.write(json_str)
        fp.close()
        obj = base.parse_json_dict(json.loads(json_str))
        # obj = base.RecordDecl(json.loads(json_str))
        # self.assertEqual(obj.inner['b'], 'asf')
