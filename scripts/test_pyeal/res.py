# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/13 8:42
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
from unittest import TestCase, FunctionTestCase


class MyTestCase(TestCase):
    def test_walk(self):
        from pyeal.res import LocalRes
        data = LocalRes(r"./../../test/").walk('test1')
        self.assertTrue(type(data) == list, 'type check error')
        self.assertTrue(type(data[0]) == tuple, 'type check')
        for i in data:
            print('>> ', i)

    def test_files(self):
        from pyeal.res import LocalRes
        data = LocalRes(r"./../../test/").files('test1')
        self.assertTrue(type(data) == list, 'type check error')
        for i in data:
            print('>> ', i)

    def test_LocalRes_and_DirectoryRes(self):
        from pyeal.res import LocalRes, DirectoryRes
        res = LocalRes(r"./../../test/test_LocalRes_and_DirectoryRes/")
        # 创建两次，测试在重复创建时是否正常
        print('test make dir')
        print('  make dir', res.make_dir('test3'))
        print('  make dir', res.make_dir('test3'))
        # 测试DirectoryRes
        dir_res = DirectoryRes(res, 'test3')
        # 测试写入文件
        print('test write string to file')
        print('  write_string', dir_res.write_string('1.py', '1.py test data'))
        print('  write_string', dir_res.write_string('2.py', '2.py test data'))
        print('  write_string', dir_res.write_string('3.py', '3.py test data'))
        # 测试遍历功能
        print('test files function')
        for i in dir_res.files():
            print('  file >> ', i)
        # 测试读取文件
        print('test read file by string')
        print('  1.py >>', dir_res.read_string('1.py'))
        print('  2.py >>', dir_res.read_string('2.py'))
        print('  3.py >>', dir_res.read_string('3.py'))
        # 测试清空文件夹功能
        print('clean dir:', dir_res.clean())
        # 删除两次，测试在重复删除时是否正常
        print('test remove dir')
        print('  remove dir', res.remove_dir('test3'))
        print('  remove dir', res.remove_dir('test3'))

    def test_MergeRes(self):
        from pyeal.res import LocalRes, MergeRes
        d1 = LocalRes(r"./../../test/test_MergeRes/d1")
        d2 = LocalRes(r"./../../test/test_MergeRes/d2")
        res = MergeRes(d1, d2)

        print('Test is not read files')

        for i in res.files():
            print('>> ', i)

        print('Test is not writable')
        try:
            res.clean()
        except RuntimeError:
            pass
        else:
            raise RuntimeError('test error: 成功对不可写入的MergeRes进行了写入')
