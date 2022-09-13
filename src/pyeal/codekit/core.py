# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/4/21 21:55
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function
import ast
import astunparse


# import pyeal.code.unparse as astunparse

def _edit_node_blocks(rn, key):
    if hasattr(rn, "_fields"):
        for i in rn._fields:
            body = getattr(rn, i)
            if isinstance(body, list):
                new_body = key(body)
                for n in new_body:
                    _edit_node_blocks(n, key)
                setattr(rn, i, new_body)


class Code(object):
    def __init__(self, code):
        self.tree = ast.parse(code)

    def insert_to_head(self, *nodes):
        for i in reversed(nodes):
            self.tree.body.insert(0, i)
        return self

    def replace_node(self, check_key, key):
        def fn(body):
            new_body = []
            for n in body:
                if check_key(n):
                    new_body.append(key(n))
                else:
                    new_body.append([n])
            return [ii for i in new_body for ii in i]

        _edit_node_blocks(self.tree, fn)
        return self

    def delete_node(self, key):
        deleted_node = []

        def fn(n):
            deleted_node.append(n)
            return []

        self.replace_node(check_key=key, key=fn)
        return deleted_node

    def unparse(self):
        return astunparse.unparse(self.tree)
