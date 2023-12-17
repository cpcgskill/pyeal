# -*-coding:utf-8 -*-
"""
:创建时间: 2023/12/15 0:15
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import shutil

if False:
    from typing import *

import os
import sys
import unittest
import pyeal.cli as cli

PATH = os.path.dirname(os.path.abspath(__file__))


class TestCli(unittest.TestCase):
    def force_an_empty_directory(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        if not os.path.isdir(path):
            os.makedirs(path)

    def test_integrity(self):
        test_root_dir = os.path.join(PATH, 'test_data/test_integrity')
        self.force_an_empty_directory(test_root_dir)

        test_dir = os.path.join(test_root_dir, 'test1')
        self.force_an_empty_directory(test_dir)

        os.chdir(test_dir)
        cli.main(['init'])
        with open(os.path.join(test_dir, 'src', 'test.py'), 'w') as f:
            f.write('print("hello world!")')
        cli.main(['build'])
        assert os.path.exists(os.path.join(test_dir, 'build', 'out', 'your_name.py'))
        cli.main(['clean'])

        test_dir = os.path.join(test_root_dir, 'test2')
        self.force_an_empty_directory(test_dir)

        os.chdir(test_dir)
        cli.main(['init', '-t', 'maya-plugin', '-n', 'test_name'])
        with open(os.path.join(test_dir, 'src', 'test.py'), 'w') as f:
            f.write('print("hello world!")')
        cli.main(['build'])
        assert os.path.exists(os.path.join(test_dir, 'build', 'out', 'install.mel'))
        assert os.path.exists(os.path.join(test_dir, 'build', 'out', 'dist', 'plugin', 'test_name.py'))
        assert os.path.exists(os.path.join(test_dir, 'build', 'out', 'dist', 'log.ico'))
        cli.main(['clean'])


        test_dir = os.path.join(test_root_dir, 'test3')
        self.force_an_empty_directory(test_dir)

        os.chdir(test_dir)
        cli.main(['init', '-t', 'template', '-n', 'test_name'])
        with open(os.path.join(test_dir, 'src', 'test.py'), 'w') as f:
            f.write('print("hello world!")')
        os.makedirs(os.path.join(test_dir, 'template/src'))
        with open(os.path.join(test_dir, 'template/src', 'test.txt'), 'w') as f:
            f.write('the file in template')
        cli.main(['build'])
        assert os.path.exists(os.path.join(test_dir, 'build', 'out', 'src', 'test_name.py'))
        cli.main(['clean'])
