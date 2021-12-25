# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/12/19 8:10
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

from seal.utils import read_string, write_string
from seal.res import LocalRes, DirectoryRes
from seal.core import EncapsulationBuilder, InstallBuilder

PATH = os.path.dirname(os.path.abspath(__file__))


class SealException(Exception):
    pass


MayaPlugin = "MayaPlugin"


class Config(object):
    def __init__(self, root):
        root = os.path.abspath(root)
        self.root = root
        root_res = LocalRes(root)
        config = json.loads(root_res.read("config.json").decode("utf-8"))
        self.type = config["type"]
        self.source = root_res.sep().join((root, config["source"]))
        self.target = root_res.sep().join((root, config["target"]))
        self.name = config["name"]
        self.exec_script = config["exec_script"]
        self.log = config["log"]
        self.annotation = config["annotation"]
        self.ord = config

    def __str__(self):
        return """{}<type={}, source={}, target={}>""".format(self.__class__.__name__, self.type, self.source,
                                                              self.target)


def go(root):
    root = os.path.abspath(root)
    config = Config(root)
    if config.type == MayaPlugin:
        root = LocalRes(config.root)
        src = LocalRes(config.source)
        build = LocalRes(config.target)
        m0 = DirectoryRes(build, "m0")
        dist = DirectoryRes(build, "dist")
        EncapsulationBuilder(src, m0, config.name, config.exec_script).build()
        InstallBuilder(m0, dist, log=root.read(config.log), ann=config.annotation).build()
    else:
        raise SealException("未知编译类型")


config_json_template = r'''{
  "type": "MayaPlugin",
  "source": "src",
  "target": "build",
  "name": <<name>>,
  "exec_script": <<exec_script>>,
  "log": "log.ico",
  "annotation": "这是这个插件的注释~"
}'''


def input_string(s):
    sys.stdout.write(s.encode("utf-8"))
    return sys.stdin.readline().strip("\n")


def init(root):
    root = os.path.abspath(root)
    name = input_string("name >> ")
    exec_script = input_string("exec_script >> ")
    name = json.dumps(name)
    exec_script = json.dumps(exec_script)
    config_json = config_json_template.replace("<<name>>", name).replace("<<exec_script>>", exec_script)
    config_json_path = os.sep.join((root, "config.json"))
    with open(config_json_path, "wb") as f:
        f.write(config_json.encode("utf-8"))

    with open(os.sep.join((PATH, "log.ico")), "rb") as f:
        with open(os.sep.join((root, "log.ico")), "wb") as wf:
            wf.write(f.read())
    src = os.sep.join((root, "src"))
    if not os.path.isdir(src):
        os.makedirs(src)
    build = os.sep.join((root, "build"))
    if not os.path.isdir(build):
        os.makedirs(build)


def main():
    argv = sys.argv[1:]
    root = os.path.abspath(".")
    if argv[0] == "init":
        init(root)
    elif argv[0] == "go":
        go(root)
    else:
        raise SealException("未知指令")

