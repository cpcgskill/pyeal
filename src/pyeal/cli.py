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
from __future__ import unicode_literals, print_function, division

import datetime
import json
import os.path
import sys
import uuid
from collections import OrderedDict

from pyeal.res import LocalRes, DirectoryRes, MergeRes
from pyeal.core import EncapsulationBuilder, InstallBuilder
from pyeal.exc import *
from pyeal._command import call_command

if False:
    from typing import List, Tuple, Dict, AnyStr, Any, Callable, Optional

PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    def __init__(self, root):
        root = os.path.abspath(root)
        self.root_path = os.path.abspath(root)
        self.src_path = os.sep.join((self.root_path, 'src'))
        self.lib_path = os.sep.join((self.root_path, 'lib'))
        self.build_path = os.sep.join((self.root_path, 'build'))
        self.middle_path = os.sep.join((root, 'build', 'middle'))
        self.out_path = os.sep.join((root, 'build', 'out'))

        self.root = LocalRes(self.root_path)
        self.src = LocalRes(self.src_path)
        self.lib = LocalRes(self.lib_path)
        self.build = LocalRes(self.build_path)
        self.middle = LocalRes(self.middle_path)
        self.out = LocalRes(self.out_path)

        self.config = json.loads(self.root.read_string("pyeal.json"))
        self.type = self.config["type"]
        self.name = self.config["name"]

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


def target_is_exec(config):
    EncapsulationBuilder(
        MergeRes(config.src, config.lib),
        config.out,
        config.name,
        config.get_script(),
        config.get('imp_name', config.name),
    ).build()


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


def target_is_template(config):
    template = DirectoryRes(config.root, 'template')
    template_output = DirectoryRes(config.out, config.ass('template-output'))

    for f in template.files():
        config.out.write(f, template.read(f))

    EncapsulationBuilder(
        MergeRes(config.src, config.lib),
        template_output,
        config.name,
        config.get_script(),
        config.get('imp_name', config.name),
    ).build()


target_types = {
    'package': target_is_exec,
    'maya-plugin': target_is_maya_plugin,
    'template': target_is_template,
}  # type: Dict[AnyStr, Callable[[Config], None]]


def _call_command_list(command_list, build_data):
    for i in command_list:
        if isinstance(i, list):
            call_command(i, build_data)
        elif isinstance(i, dict):
            try:
                is_do_command = eval(i.get('if_expression', 'True'), dict(), build_data)
            except:
                is_do_command = False
            if is_do_command:
                command = i.get('true_command', None)
                if command:
                    call_command(command, build_data)
            else:
                command = i.get('false_command', None)
                if command:
                    call_command(command, build_data)
        else:
            raise SealException("未知的命令格式")


def cmd_build(config, *args):
    """
    :type config: Config
    """
    config.build.clean()
    command_list_at_start = config.get('command_list_at_start', [])
    command_list_at_end = config.get('command_list_at_end', [])
    build_data = {
        'build_uuid': uuid.uuid4().hex,
        'build_time': datetime.datetime.now(),
        'src_path': config.src_path,
        'lib_path': config.lib_path,
        'build_path': config.build_path,
        'middle_path': config.middle_path,
        'out_path': config.out_path,
        'args': args,
        'name': config.name,
    }

    _call_command_list(command_list_at_start, build_data)

    target_type_func = target_types.get(config.type)

    if target_type_func is None:
        raise SealException("未知编译类型")

    target_type_func(config)

    _call_command_list(command_list_at_end, build_data)


config_templates = {
    "maya-plugin": OrderedDict([
        ("type", "maya-plugin"),
        ("source", "src"),
        ("target", "build"),
        ("name", "your-name"),
        ("exec_script", "your-script"),
    ])
}


def cmd_init(config):
    """
    :type config: Config
    """
    config.root.write_string("pyeal.json", json.dumps(config_templates["maya-plugin"], indent=2).encode("utf-8"))
    with open(os.sep.join((PATH, "log.ico")), "rb") as f:
        config.root.write("log.ico", f.read())
    src = os.sep.join((config.root_path, "src"))
    if not os.path.isdir(src):
        os.makedirs(src)
    build = os.sep.join((config.root_path, "build"))
    if not os.path.isdir(build):
        os.makedirs(build)


def cmd_clean(config):
    """
    :type config: Config
    """
    config.build.clean()


commands = {
    "build": cmd_build,
    "init": cmd_init,
    "clean": cmd_clean,
}  # type: Dict[AnyStr, Callable[[Config, ...], None]]


def main():
    root = os.path.abspath(".")
    command = commands.get(sys.argv[1])
    if command is None:
        raise SealException("未知指令")
    command(Config(root), *sys.argv[2:])
