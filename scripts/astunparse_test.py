# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/4/13 0:20
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function, division
import pyeal.astunparse as astunparse

with open('./astunparse_test_file.py', 'rb') as f:
    test_code = f.read()


def test():
    tree = astunparse.parser(test_code)
    code = astunparse.unparser(tree)
    print(code)


if __name__ == '__main__':
    test()
