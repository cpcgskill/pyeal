# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/12/19 9:54
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function

import os


def read(filename):
    """
    :type filename: unicode
    """
    with open(filename, 'rb') as f:
        return f.read()


def write(filename, b):
    """

    :type filename: unicode
    :type b: bytes
    """
    with open(filename, 'rb') as f:
        return f.write(b)


def read_string(filename):
    """
    :type filename: unicode
    """
    return read(filename).decode("utf-8")


def write_string(filename, s):
    """

    :type filename: unicode
    :type s: unicode
    """
    write(filename, s.encode("utf-8"))


def all_files(path):
    return (os.sep.join((root, f)) for root, dirs, fs in os.walk(path) for f in fs)


def all_partial_paths(path):
    path_size = len(path.split(os.sep))
    return (os.sep.join(f.split(os.sep)[path_size:]) for f in all_files(path))


def all_full_and_partial_paths(path):
    path_size = len(path.split(os.sep))
    return ((f, os.sep.join(f.split(os.sep)[path_size:])) for f in all_files(path))


def all_lib_names(path):
    """获得所有库的名称（不是模块或者包的，并不会深入包内部）"""
    for f, p in all_full_and_partial_paths(path):
        items = p.split(os.sep)
        if len(items) == 1:
            i = items[0]
            split_char_index = i.find(".")
            ext = i[split_char_index:]
            if ext == ".py" or ".pyd" or ".pyo":
                yield i[:split_char_index], f
        elif len(items) == 2:
            if items[1] == "__init__.py":
                yield items[0], f.split(os.sep)[:-1]


__all__ = ['read_string', 'write_string', 'all_files', 'all_partial_paths', 'all_full_and_partial_paths',
           'all_lib_names']
