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
from abc import abstractmethod


class BaseRes(object):
    @abstractmethod
    def read(self, p):
        """
        :type p: unicode
        :rtype: bytes
        """

    @abstractmethod
    def write(self, p, data):
        """
        :type p: unicode
        :type data: bytes
        :return:
        """

    @abstractmethod
    def sep(self):
        """
        :rtype: unicode
        """

    @abstractmethod
    def walk(self):
        """

        :rtype: list[tuple[unicode|None, list[unicode]]]
        """

    def files(self):
        for r, fs in self.walk():
            for f in fs:
                if r is not None:
                    f = self.sep().join((r, f))
                yield f


class LocalRes(BaseRes):
    def __init__(self, root):
        """

        :type root: unicode
        """
        self.root = root

    def read(self, p):
        p = self.sep().join((self.root, p))
        with open(p, "rb") as f:
            return f.read()

    def write(self, p, data):
        p = self.sep().join((self.root, p))
        dir_, name = os.path.split(p)
        if not os.path.isdir(dir_):
            os.makedirs(dir_)
        with open(p, "wb") as f:
            return f.write(data)

    def sep(self):
        return os.sep

    def walk(self):
        for root, _, files in os.walk(self.root):
            root = self.sep().join(root.split(self.sep())[len(self.root.split(self.sep())):])
            yield None if root == "" else root, files


class DirectoryRes(BaseRes):
    def __init__(self, res, dir_):
        """

        :type res: BaseRes
        :type dir_: unicode
        """
        self.res = res
        self.dir = dir_

    def new_path(self, p):
        return self.sep().join((self.dir, p))

    def read(self, p):
        return self.res.read(self.new_path(p))

    def write(self, p, data):
        return self.res.write(self.new_path(p), data)

    def sep(self):
        return self.res.sep()

    def walk(self):
        for r, fs in self.res.walk():
            if r is not None and self.dir in r:
                rs = r.split(self.sep())
                if self.dir == rs[0]:
                    r = self.sep().join(rs[1:])
                    yield None if r == "" else r, fs

if __name__ == "__main__":
    for i in LocalRes(r"D:\backup_to_cloud\dev\python_for_maya\package\seal").walk():
        print(i)
