# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/12/24 15:12
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function

from pyeal.res import BaseRes
from pyeal.exc import *


def file_ext(filename, sep='/'):
    return "." + ".".join(filename.split(sep)[-1].split(".")[1:])


def file_name(filename):
    return filename.split(".")[0]


class ModuleData(object):
    def __init__(self, source):
        """
        :type source: BaseRes
        """
        self.source = source
        self._check()
        self._module_index_table = self._init_module_index_table()
        self._lib_names = self._init_lib_names()
        pass

    def _check(self):
        module_names = set()
        for root, files in self.source.walk():
            if not root is None and "__init__.py" in files:
                module_name = ".".join(root.split(self.source.sep()))
                if module_name in module_names:
                    raise ModuleDataException("存在多个解析名称为{}的文件或文件夹".format(module_name))
                module_names.add(module_name)
            if root is None:
                for f in files:
                    if file_ext(f, self.source.sep()) == ".py":
                        module_name = file_name(f)
                        if module_name in module_names:
                            raise ModuleDataException("存在多个解析名称为{}的文件或文件夹".format(module_name))
                        module_names.add(module_name)

    def _init_module_index_table(self):
        table = dict()
        for root, files in self.source.walk():
            # 检查包
            if root is not None and "__init__.py" in files:
                table[".".join(root.split(self.source.sep()))] = self.source.sep().join((root, "__init__.py"))
            # 检查模块
            for f in files:
                if file_ext(f, self.source.sep()) == ".py":
                    f_name = file_name(f)
                    if root is None:
                        table[f_name] = f
                    else:
                        f_name = ".".join(self.source.sep().join((root, f_name)).split(self.source.sep()))
                        table[f_name] = self.source.sep().join((root, f))

        return table

    def _init_lib_names(self):
        return set((i.split(".")[0] for i in self._module_index_table.keys()))

    def lib_names(self):
        return (i for i in self._lib_names)

    def module_names(self):
        return (i for i in self._module_index_table.keys())

    def module_name_and_paths(self):
        return ((k, v) for k, v in self._module_index_table.items())

    def find_lib(self, n):
        if n in self._lib_names:
            return n
        return None

    def find_module(self, n):
        if n in self._module_index_table:
            return n
        return None

    def relative_find_module(self, n, parent_module):
        parent_names = parent_module.split(".")
        for m in self._module_index_table.keys():
            if len(m.split(".")) > len(parent_names):
                if parent_module == ".".join(m.split(".")[:len(parent_names)]):
                    if n == ".".join(m.split(".")[len(parent_names):]):
                        return m
        return None

    def get_module_path(self, n):
        return self._module_index_table[n]

    def __str__(self):
        body = "\n    ".join(("{}: {}".format(k, v) for k, v in self._module_index_table.items()))
        return self.__class__.__name__ + "{\n    %s\n}" % body

    def __repr__(self):
        return repr(self.__str__())
