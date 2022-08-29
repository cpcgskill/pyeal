# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/4/12 20:10
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function, division

__all__ = ['SealException', 'ConfigException', 'ModuleDataException', 'ResException']


class SealException(Exception): pass


class ConfigException(SealException): pass


class ModuleDataException(SealException): pass


class ResException(SealException): pass
