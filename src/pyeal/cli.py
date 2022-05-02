# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/3/8 12:02
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function
import json
import os.path
import sys
from collections import OrderedDict

from pyeal.res import LocalRes, DirectoryRes, MergeRes
from pyeal.core import EncapsulationBuilder, InstallBuilder
from pyeal.exc import *

PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    def __init__(self, root):
        root = os.path.abspath(root)
        self.root = LocalRes(root)
        config = json.loads(self.root.read_string("pyeal.json"))
        self.config = config

        self.type = config["type"]

        self.src = LocalRes(os.sep.join((root, 'src')))
        self.lib = LocalRes(os.sep.join((root, 'lib')))
        self.build = LocalRes(os.sep.join((root, 'build')))
        self.middle = LocalRes(os.sep.join((root, 'build', 'middle')))
        self.out = LocalRes(os.sep.join((root, 'build', 'out')))

        self.name = config["name"]

    def get_script(self):
        script = self.config.get("exec_script", None)
        if script is None:
            index_module = self.config.get("index_module", "index.py")
            script = self.root.read(index_module)
        return script

    def get_icon(self):
        return self.root.read('icon.ico')

    def get(self, key, default=None):
        return self.config.get(key, default)

    def ass(self, key):
        c = self.get(key, None)
        if c is None:
            raise ConfigException("需要名为<{}>的配置项".format(key))
        return c

def target_is_maya_plugin(config):
    m0 = DirectoryRes(config.middle, "m0")

    EncapsulationBuilder(
        MergeRes(config.src, config.lib),
        m0,
        config.name,
        config.get_script(),
        config.get('imp_name', config.name)
    ).build()

    InstallBuilder(
        m0,
        config.out,
        log=config.get_icon(),
        ann=config.get("annotation", "这个插件作者很懒没有写注释哦~"),
        name=config.get('imp_name', config.name),
    ).build()


def target_is_exec(config):
    EncapsulationBuilder(
        MergeRes(config.src, config.lib),
        config.out,
        config.name,
        config.get_script(),
        config.get('imp_name', config.name),
    ).build()


target_types = {
    "package": target_is_exec,
    "maya-plugin": target_is_maya_plugin,
}


def cmd_build(root):
    config = Config(root)

    config.build.clean()

    target_type_func = target_types.get(config.type)
    if target_type_func is None:
        raise SealException("未知编译类型")
    target_type_func(config)


config_templates = {
    "maya-plugin": OrderedDict([
        ("type", "maya-plugin"),
        ("source", "src"),
        ("target", "build"),
        ("name", "your-name"),
        ("exec_script", "your-script"),
    ])
}


def cmd_init(root):
    config_json_path = os.sep.join((root, "pyeal.json"))
    with open(config_json_path, "wb") as f:
        config = config_templates["maya-plugin"]
        f.write(json.dumps(config, indent=2).encode("utf-8"))

    with open(os.sep.join((PATH, "log.ico")), "rb") as f:
        with open(os.sep.join((root, "log.ico")), "wb") as wf:
            wf.write(f.read())
    src = os.sep.join((root, "src"))
    if not os.path.isdir(src):
        os.makedirs(src)
    build = os.sep.join((root, "build"))
    if not os.path.isdir(build):
        os.makedirs(build)


def cmd_clean(root):
    config = Config(root)
    target = LocalRes(config.build)
    target.clean()


commands = {
    "build": cmd_build,
    "init": cmd_init,
    "clean": cmd_clean,
}


def main():
    argv = sys.argv[1:]
    root = os.path.abspath(".")
    command = commands.get(argv[0])
    if command is None:
        raise SealException("未知指令")
    command(root, *argv[1:])
