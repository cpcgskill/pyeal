# -*-coding:utf-8 -*-
"""
:创建时间: 2022/8/29 15:30
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
import os
import sys
import subprocess

if False:
    from typing import List, Tuple, Dict, AnyStr, Any, Callable, Union

__all__ = ['compile_item', 'call_command']


def compile_item(item, data):
    new_data = dict()
    for k, v in os.environ.items():
        new_data[k] = v
    for k, v in data.items():
        new_data[k] = v
    return item.format(**new_data)


def call_command(argv, data=None):
    """
    :type argv: List[AnyStr]
    :type data: Dict[AnyStr, AnyStr or int or float] or None
    """
    if data is None:
        data = dict()
    argv = [compile_item(i, data) for i in argv]
    command = argv[0]
    argv = argv[1:]

    subprocess.check_call([command] + argv)


if __name__ == '__main__':
    do_command(['echo', '{PATH}'])
    do_command(['echo', '{PATH}'], {'PATH': 123})
