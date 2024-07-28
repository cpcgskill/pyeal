# -*-coding:utf-8 -*-
"""
:创建时间: 2024/7/28 15:41
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
from unittest import TestCase, FunctionTestCase
import os
from pyeal.cli import main

root = os.path.abspath('../../test/command_line')
if not os.path.isdir(root):
    os.makedirs(root)


def get_base_dir(name):
    if os.path.isdir(os.path.join(root, name)):
        shutil.rmtree(os.path.join(root, name))
        os.makedirs(os.path.join(root, name))
    else:
        os.makedirs(os.path.join(root, name))
    return os.path.join(root, name)


class MainTestCase(TestCase):
    def test_default_project(self):
        os.chdir(get_base_dir('default'))

        # init project
        main(['init', '-n', 'test_project'])
        self.assertTrue(os.path.isfile('pyeal.json'), 'init project failed')

        # build project
        main(['build'])
        self.assertTrue(os.path.isdir('build/out'), 'build project failed')

        # clean project
        main(['clean'])
        self.assertFalse(os.path.isdir('build/out'), 'clean project failed')

        # rebuild project
        main(['build'])
        self.assertTrue(os.path.isdir('build/out'), 'rebuild project failed')

    def test_maya_plugin_project(self):
        os.chdir(get_base_dir('maya_plugin'))

        # init project
        main(['init', '-t', 'maya-plugin'])
        self.assertTrue(os.path.isfile('pyeal.json'), 'init project failed')

        # build project
        main(['build'])
        self.assertTrue(os.path.isdir('build/out'), 'build project failed')

        # clean project
        main(['clean'])
        self.assertFalse(os.path.isdir('build/out'), 'clean project failed')

        # rebuild project
        main(['build'])
        self.assertTrue(os.path.isdir('build/out'), 'rebuild project failed')
