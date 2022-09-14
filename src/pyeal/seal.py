# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/13 13:32
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
import uuid
import ast

from pyeal.codekit.core import Code
from pyeal.res import BaseRes
from pyeal.module_data import ModuleData

if False:
    from typing import List, Tuple, Dict, AnyStr, Any


class Sealer(object):
    """打包编译器"""

    def __init__(self, source, target, name, code, imp_name=None):
        """
        :type source: BaseRes
        :type target: BaseRes
        :type name: unicode
        """
        self.source = source
        self.target = target
        self.name = name
        self.code = code
        if imp_name is None:
            self.imp_name = name
        else:
            self.imp_name = imp_name
        self.module_data = ModuleData(self.source)
        self.uid = uuid.uuid4().hex[0:4]

    def seal_name(self):
        return "{}_{}".format(self.name, self.uid)

    def target_name(self, p):
        return "{}_{}".format(self.seal_name(), p)

    def target_path(self, p):
        if len(p.split('/')) == 1 and \
                p.split('.')[-1] != 'py':
            return p
        else:
            return "{}_{}".format(self.seal_name(), p)

    def target_dir_path(self, p):
        return "{}_{}".format(self.seal_name(), p)

    def compile_import_node(self, n, m):
        alias_list = []
        for i in n.names:
            if m is None:
                r_find_name = None
            else:
                r_find_name = self.module_data.relative_find_module(i.name, m)
            name = self.module_data.find_module(i.name)
            if r_find_name is None and name is not None:
                if i.asname is None:
                    alias_list.append(ast.alias(asname=i.name.split(".")[0],
                                                name=self.target_name(i.name.split('.')[0])))
                    alias_list.append(ast.alias(asname="_",
                                                name=self.target_name(name)))
                else:
                    target_asname = i.asname
                    alias_list.append(ast.alias(asname="_",
                                                name=self.target_name(i.name.split('.')[0])))
                    alias_list.append(ast.alias(asname=target_asname,
                                                name=self.target_name(name)))

            else:
                alias_list.append(i)
        return [ast.Import(names=[i]) for i in alias_list]

    def compile_import_from_node(self, n, m):
        if n.level == 0:
            nodes = []
            if m is None:
                r_find_name = None
            else:
                r_find_name = self.module_data.relative_find_module(n.module, m)
            name = self.module_data.find_module(n.module)
            if r_find_name is None and name is not None:
                nodes.append(ast.ImportFrom(level=0,
                                            module=self.target_name(name),
                                            names=n.names))
            else:
                nodes.append(n)
            return nodes
        else:
            return [n]

    def delete_future(self, n):
        if isinstance(n, ast.ImportFrom):
            if n.level == 0:
                if n.module == "__future__":
                    return True
        return False

    def compile_module(self, code, m=None):
        """
        :type code: bytes
        :type m: AnyStr or None
        :return:
        """
        code_editor = Code(code)

        code_editor.replace_node(
            check_key=lambda n: isinstance(n, ast.Import),
            key=lambda n: self.compile_import_node(n, m)
        ).replace_node(
            check_key=lambda n: isinstance(n, ast.ImportFrom),
            key=lambda n: self.compile_import_from_node(n, m)
        )

        deleted_future = code_editor.delete_node(key=self.delete_future)

        code_editor.insert_to_head(deleted_future)

        code = code_editor.unparse()

        return code.encode("utf-8")

    def build(self):
        for d in self.source.dirs():
            self.target.make_dir(self.target_dir_path(d))
        for f in self.source.files():
            self.target.write(self.target_path(f), self.source.read(f))
        for m, f in self.module_data.module_name_and_paths():
            code = self.source.read(f)
            code = self.compile_module(code, m)
            self.target.write(self.target_path(f), code)
        code = self.compile_module(self.code, None)
        self.target.write(self.imp_name + ".py", code)


def seal(source, target, name, code, imp_name=None):
    """
    :type source: BaseRes
    :type target: BaseRes
    :type name: AnyStr
    :type code: AnyStr
    :type imp_name: AnyStr or None
    """
    return Sealer(source, target, name, code, imp_name).build()
