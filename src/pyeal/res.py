# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/12/22 7:38
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function

import os
import sys
from abc import abstractmethod

from pyeal.exc import *

if False:
    from typing import List, Tuple, Dict, AnyStr, Any


class BaseRes(object):
    @abstractmethod
    def customize_read(self, path):
        """
        :type path: AnyStr
        :rtype: bytes
        """

    @abstractmethod
    def customize_write(self, path, data):
        """
        :type path: AnyStr
        :type data: bytes
        """

    @abstractmethod
    def customize_remove(self, path):
        """
        :type path: AnyStr
        """

    @abstractmethod
    def customize_make_dir(self, path):
        """
        :type path: AnyStr
        """

    @abstractmethod
    def customize_remove_dir(self, path):
        """
        :type path: AnyStr
        """

    @abstractmethod
    def customize_sep(self):
        """
        :rtype: AnyStr
        """

    @abstractmethod
    def customize_is_dir(self, path):
        """
        :type path: AnyStr
        :rtype: bool
        """

    @abstractmethod
    def customize_is_file(self, path):
        """
        :type path: AnyStr
        :rtype: bool
        """

    @abstractmethod
    def customize_walk(self):
        """

        :rtype: List[Tuple[AnyStr, List[AnyStr], List[AnyStr]]]
        """

    def to_customize_sep(self, path):
        """
        :type path: AnyStr
        :rtype: AnyStr
        """
        return self.customize_sep().join((i for i in path.split('/') if i != ''))

    def to_std_sep(self, path):
        """
        :type path: AnyStr
        :rtype: AnyStr
        """
        return '/'.join((i for i in path.split(self.customize_sep()) if i != ''))

    @staticmethod
    def join_path(*path):
        return '/'.join(path)

    def read(self, path):
        """
        :type path: AnyStr
        :rtype: bytes
        """
        return self.customize_read(self.to_customize_sep(path))

    def write(self, path, data):
        """
        :type path: AnyStr
        :type data: bytes
        """
        self.customize_write(self.to_customize_sep(path), data)
        return self

    def read_string(self, path):
        """
        :type path: AnyStr
        :rtype: AnyStr
        """
        return self.read(path).decode('utf-8')

    def write_string(self, path, data):
        """
        :type path: AnyStr
        :type data: AnyStr
        """
        self.write(path, data.encode('utf-8'))
        return self

    def remove(self, path):
        self.customize_remove(self.to_customize_sep(path))
        return self

    def make_dir(self, path):
        path = self.to_customize_sep(path)
        if not self.customize_is_dir(path):
            self.customize_make_dir(path)
        return self

    def remove_dir(self, path):
        path = self.to_customize_sep(path)
        if self.customize_is_dir(path):
            self.customize_remove_dir(path)
        return self

    def is_dir(self, path):
        path = self.to_customize_sep(path)
        return self.customize_is_dir(path)

    def is_file(self, path):
        path = self.to_customize_sep(path)
        return self.customize_is_file(path)

    def walk(self, prefix=''):
        """
        :type prefix: AnyStr
        :rtype: List[Tuple[AnyStr, List[AnyStr], List[AnyStr]]]
        """
        prefix = self.to_std_sep(prefix)
        data = [(self.to_std_sep(root), dirs, files) for root, dirs, files in self.customize_walk()]
        # 如果前缀不为空，则过滤所有不和前缀匹配的root
        if prefix != '':
            prefix = prefix.split('/')

            def path_prefix_match(matched_path):
                matched_path = matched_path.split('/')
                if len(prefix) > len(matched_path):
                    return True
                matched_path = matched_path[:len(prefix)]
                return all([i[0] == i[1] for i in zip(prefix, matched_path)])

            return [(root, dirs, files) for root, dirs, files in data if path_prefix_match(root)]
        return data

    def __files(self, prefix=''):
        for root, dirs, files in self.walk(prefix):
            for f in files:
                if root != '':
                    f = '/'.join((root, f))
                yield f

    def files(self, prefix=''):
        """
        :type prefix: AnyStr
        :rtype: List[AnyStr]
        """
        return list(self.__files(prefix))

    def __dirs(self, prefix=''):
        for root, dirs, files in self.walk(prefix):
            for d in dirs:
                if root != '':
                    d = '/'.join((root, d))
                yield d

    def dirs(self, prefix=''):
        """
        :type prefix: AnyStr
        :rtype: List[AnyStr]
        """
        return list(self.__dirs(prefix))

    def clean(self, path=''):
        """
        :type path: AnyStr
        """
        for f in self.files(path):
            # self.customize_remove(f)
            self.remove(f)
        for d in reversed(self.dirs(path)):
            # self.customize_remove_dir(d)
            self.remove_dir(d)
        return self


class LocalRes(BaseRes):
    def __init__(self, root):
        """

        :type root: AnyStr
        """
        self.root = os.path.abspath(root)
        if sys.platform == 'win32':
            # if len(self.root) > 256:
            self.root = '\\\\?\\' + self.root

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return "{}(root={})".format(self.__class__.__name__, repr(self.root))

    def customize_read(self, path):
        path = os.sep.join((self.root, path))
        # if len(path) > 256:
        #     path = '\\\\?\\' + path
        with open(path, "rb") as f:
            return f.read()

    def customize_write(self, path, data):
        # if path.find('elementwise_logical_ops_test.test_is_member_of.zip') != -1:
        #     pass
        path = os.sep.join((self.root, path))
        dir_, name = os.path.split(path)
        if not os.path.isdir(dir_):
            os.makedirs(dir_)
        # if sys.platform == 'win32':
        #     try:
        #         with open(path, "wb") as f:
        #             return f.write(data)
        #     except IOError as ex:
        #         if len(path) > 767:
        #             raise IOError('Accidents caused by too long path lengths at compile time', ex)
        #         else:
        #             raise
        # else:
        #     with open(path, "wb") as f:
        #         return f.write(data)
        with open(path, "wb") as f:
            return f.write(data)

    def customize_remove(self, path):
        path = os.sep.join((self.root, path))
        # old_cwd = os.getcwd()
        # try:
        #     os.chdir(os.path.dirname(path))
        #
        #     new_path = './' + path.split(self.customize_sep())[-1]
        #     try:
        #         os.remove(new_path)
        #     except WindowsError as ex:
        #         raise WindowsError('path {} error! {}'.format(path, ex))
        # finally:
        #     os.chdir(old_cwd)
        # if len(path) > 256:
        #     path = '\\\\?\\' + path
        os.remove(path)

    def customize_make_dir(self, path):
        path = os.sep.join((self.root, path))
        os.makedirs(path)

    def customize_remove_dir(self, path):
        path = os.sep.join((self.root, path))
        os.rmdir(path)

    def customize_sep(self):
        return os.sep

    def customize_is_dir(self, path):
        path = os.sep.join((self.root, path))
        return os.path.isdir(path)

    def customize_is_file(self, path):
        path = os.sep.join((self.root, path))
        return os.path.isfile(path)

    def customize_walk(self):
        for root, dirs, files in os.walk(self.root):
            root = root.split(self.customize_sep())[len(self.root.split(self.customize_sep())):]
            root = self.customize_sep().join(root)
            yield root, dirs, files


class DirectoryRes(BaseRes):
    def __init__(self, res, dir_):
        """

        :type res: BaseRes
        :type dir_: AnyStr
        """
        self.res = res
        self.dir = self.to_std_sep(dir_)
        self.dir_path_len = len(self.dir.split('/'))

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return "{}(res={}, dir={})".format(self.__class__.__name__, self.res, repr(self.dir))

    def new_customize_path(self, p):
        return self.customize_sep().join((self.dir, p))

    def new_std_path(self, p):
        return '/'.join((self.dir, p))

    def customize_read(self, path):
        return self.res.read(self.new_customize_path(path))

    def customize_write(self, path, data):
        return self.res.write(self.new_customize_path(path), data)

    def customize_remove(self, path):
        return self.res.customize_remove(self.new_customize_path(path))

    def customize_make_dir(self, path):
        return self.res.customize_make_dir(self.new_customize_path(path))

    def customize_remove_dir(self, path):
        return self.res.customize_remove_dir(self.new_customize_path(path))

    def customize_sep(self):
        return self.res.customize_sep()

    def customize_is_dir(self, path):
        return self.res.customize_is_dir(self.new_customize_path(path))

    def customize_is_file(self, path):
        return self.res.customize_is_file(self.new_customize_path(path))

    def customize_walk(self):
        return [
            ('/'.join(root.split('/')[self.dir_path_len:]), dirs, files)
            for root, dirs, files in self.res.walk(self.dir)
        ]


class MergeRes(BaseRes):
    def __init__(self, *res):
        """

        :type res: BaseRes
        """
        self.res = res

    def customize_read(self, path):
        for r in self.res:
            try:
                return r.read(path)
            except:
                pass
        raise ResException("找不到对应文件")

    def customize_write(self, path, data):
        raise RuntimeError('写入相关方法不可用')

    def customize_remove(self, path):
        raise RuntimeError('写入相关方法不可用')

    def customize_make_dir(self, path):
        raise RuntimeError('写入相关方法不可用')

    def customize_remove_dir(self, path):
        raise RuntimeError('写入相关方法不可用')

    def customize_sep(self):
        return '/'

    def customize_is_dir(self, path):
        return any((i.is_dir(i.to_customize_sep(path)) for i in self.res))

    def customize_is_file(self, path):
        return any((i.is_file(i.to_customize_sep(path)) for i in self.res))

    def customize_walk(self):
        return [t for i in self.res for t in i.walk()]
