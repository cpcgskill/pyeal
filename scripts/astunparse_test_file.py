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
from . import os, sys as s
import os as o, sys as s
from abc import abstractmethod as a, get_cache_token as g

from pyeal.exc import *

def undo_block(fn):
    @functools.wraps(fn)
    def _(*args, **kwargs):
        mc.undoInfo(ock=True)
        try:
            return fn(*args, **kwargs)
        finally:
            mc.undoInfo(cck=True)

    return _

def test(a, b=0, c=1, *args, **kwargs):
    pass
test(0, 1, *[3, 4, 5], c=3, **{a:'s'})

if r is not None and self.dir and 1 or 2 in r:
    rs = r.split(self.sep())
    if self.dir == rs[0]:
        r = self.sep().join(rs[1:])
        yield None if r == "" else r, fs

+a
-a
~1
1 > 0
1 < 0
1 >= 0
1 <= 0
1 == 0
1 != 0
1 + 0
1 - 0
1 * 0
1 / 0
1 & 0
1 | 0
1 ^ 0
1 >> 0
1 << 0
1 < 0
1 > 0
1 ** 1
1 // 1
"%s:" % 'get '

a += 1
a *= 1
a /= 1
a -= 1
a ^= 1
a &= 1
a |= 1
a <<= 1
a >>= 1
a //= 1
a **= 1

s = [(i, t) for i in range(10) if i > 0 if i < 0 for t in range(10) if i != -1 if i > 0]

s = {i: 0 for i in range(10)}
s = {i for i in range(10)}
s = [i for i in range(10)]
s = (i for i in range(10))

if True:
    pass
elif True:
    pass
elif True:
    pass
else:
    pass
a = (1,)
b = [1, ]
c = {1, }
d = {1: 1}
global a, b, c

try:
    pass
except Exception as e:
    pass
except:
    pass
else:
    pass
finally:
    pass
with open('./astunparse_test_file.py', 'rb'):
    pass
with open('./astunparse_test_file.py', 'rb') as f:
    test_code = f.read()
for i in range(10):
    pass
while True:
    pass

assert True
assert True, "msg"
raise
raise IndexError
raise IndexError("error")

@abstractmethod
class BaseRes(object):
    t = 1

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

    def read_string(self, p):
        return self.read(p).decode('utf-8')

    def write_string(self, p, s):
        self.write(p, s.encode('utf-8'))

    @abstractmethod
    def clean(self, p=None):
        """
        :rtype:
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
                    ((xx,), xxx)[0, 0:, ::] = ((1,), 2)
                    xxx, = (1,)
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
        with open(p, "rb") as f, open(p, "rb") as f2:
            return f.read()

    def write(self, p, data):
        p = self.sep().join((self.root, p))
        dir_, name = os.path.split(p)
        if not os.path.isdir(dir_):
            os.makedirs(dir_)
        with open(p, "wb") as f:
            return f.write(data)

    def clean(self, p=None):
        file_list = []
        dir_list = []
        root = self.root if p is None else self.sep().join([self.root, p])
        for root, ds, fs in os.walk(root):
            for i in fs:
                file_list.append(self.sep().join([root, i]))
            for i in ds:
                dir_list.append(self.sep().join([root, i]))
        for i in file_list:
            os.remove(i)
        for i in reversed(dir_list):
            os.rmdir(i)

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

    def clean(self, p=None):
        p = self.dir if p is None else self.new_path(p)
        self.res.clean(p)

    def walk(self):
        for r, fs in self.res.walk():
            if r is not None and self.dir and 1 or 2 in r:
                rs = r.split(self.sep())
                if self.dir == rs[0]:
                    r = self.sep().join(rs[1:])
                    yield None if r == "" else r, fs


class MergeRes(BaseRes):
    def __init__(self, *res):
        """

        :type res: BaseRes
        """
        self.res = res

    def read(self, p):
        for r in self.res:
            try:
                return r.read(p)
            except:
                pass
            else:
                pass
            try:
                return r.read(p)
            except:
                pass
            else:
                pass
            finally:
                pass
        raise ResException("找不到对应文件")

    def write(self, p, data):
        return self.res[0].write(p, data)

    def sep(self):
        return self.res[0].sep()

    def clean(self, p=None):
        for r in self.res:
            r.clean(p)

    def walk(self):
        for r in self.res:
            for r, fs in r.walk():
                yield r, fs


if __name__ == "__main__":
    for i in LocalRes(r"D:\backup_to_cloud\dev\python_for_maya\package\seal").walk():
        print(i, *(0, 1), sep="-")
import cpmel.cmds as cc
from rig_lib.ctx import Ctx
from rig_lib.joint_tree import create_real_joints_from_root
from rig_lib_feather import gen_feather
from rig_lib_name import enter_new_name_space
import rig_lib_shape as shape

from cpform import item, core
from maya_utils import call_block


@call_block
def call(p_con, p_joint, con_nurbs_surface, con_curve, ik_count, fk_count):
    ctx = Ctx()
    p_con = cc.new_object(p_con)
    p_joint = cc.new_object(p_joint)
    con_nurbs_surface = cc.new_object(con_nurbs_surface)
    con_curve = cc.new_object(con_curve)
    jins = cc.selected()
    # pickWalk -d down;
    cc.pickWalk(d='down')
    end_jins = cc.selected()
    main_con = cc.curve(d=1, p=[(0.0955899456935, 0.0955899456935, 0.824480077314),
                                (-0.0955899456935, 0.0955899456935, 0.824480077314),
                                (-0.0955899456935, -0.0955899456935, 0.824480077314),
                                (0.0955899456935, -0.0955899456935, 0.824480077314),
                                (0.0955899456935, 0.0955899456935, 0.824480077314),
                                (0.0955899456935, 0.0955899456935, 0.633300185927),
                                (0.0955899456935, -0.0955899456935, 0.633300185927),
                                (0.0955899456935, -0.0955899456935, 0.824480077314),
                                (-0.0955899456935, -0.0955899456935, 0.824480077314),
                                (-0.0955899456935, -0.0955899456935, 0.633300185927),
                                (-0.0955899456935, 0.0955899456935, 0.633300185927),
                                (-0.0955899456935, 0.0955899456935, 0.824480077314),
                                (-0.0955899456935, -0.0955899456935, 0.824480077314),
                                (-0.0955899456935, -0.0955899456935, 0.633300185927),
                                (0.0955899456935, -0.0955899456935, 0.633300185927),
                                (0.0955899456935, 0.0955899456935, 0.633300185927),
                                (-0.0955899456935, 0.0955899456935, 0.633300185927),
                                (-0.0955899456935, -0.0955899456935, 0.633300185927)],
                        k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0,
                           17.0])
    shape.setColorId(main_con, 6)

    ik_con = cc.curve(d=1, p=[(0.35, 0.35, 0.35),
                              (-0.35, 0.35, 0.35),
                              (-0.35, -0.35, 0.35),
                              (0.35, -0.35, 0.35),
                              (0.35, 0.35, 0.35),
                              (0.35, 0.35, -0.35),
                              (0.35, -0.35, -0.35),
                              (0.35, -0.35, 0.35),
                              (-0.35, -0.35, 0.35),
                              (-0.35, -0.35, -0.35),
                              (-0.35, 0.35, -0.35),
                              (-0.35, 0.35, 0.35),
                              (-0.35, -0.35, 0.35),
                              (-0.35, -0.35, -0.35),
                              (0.35, -0.35, -0.35),
                              (0.35, 0.35, -0.35),
                              (-0.35, 0.35, -0.35),
                              (-0.35, -0.35, -0.35)],
                      k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0,
                         17.0])
    shape.setColorId(ik_con, 14)

    fk_con = cc.curve(d=1, p=[(1.09237352925e-33, 0.291346265418, -1.78398135694e-17),
                              (-1.261465315e-17, 0.20601291995, 0.20601291995),
                              (-1.78398135694e-17, 1.78398135694e-17, 0.291346265418),
                              (-1.261465315e-17, -0.20601291995, 0.20601291995),
                              (-1.09237352925e-33, -0.291346265418, 1.78398135694e-17),
                              (1.261465315e-17, -0.20601291995, -0.20601291995),
                              (1.78398135694e-17, -1.78398135694e-17, -0.291346265418),
                              (1.261465315e-17, 0.20601291995, -0.20601291995),
                              (1.09237352925e-33, 0.291346265418, -1.78398135694e-17)],
                      k=[0.0, 0.7653668647301797, 1.5307337294603593, 2.296100594190539, 3.0614674589207187,
                         3.8268343236508984, 4.592201188381078, 5.357568053111258, 6.122934917841437])
    shape.setColorId(fk_con, 13)

    try:
        with ctx.enter_new_tag_rt('radiant_joint_tool'):
            for id_, (jin, end_jin) in enumerate(zip(jins, end_jins)):
                with enter_new_name_space("{}_".format(jin.name())):
                    g = gen_feather(ctx,
                                    jin, end_jin,
                                    con_nurbs_surface, con_curve,
                                    ik_count, fk_count,
                                    ["id_{}".format(id_)])
                    p_con.add_child(g)
            create_real_joints_from_root(ctx.root_joint, p_joint)
            for i in ctx.filter().tag_equal('controller').tag_equal('feather'):
                shape.replace(i, main_con)
            for i in ctx.filter().tag_equal('controller').tag_equal('ik').tag_equal('feather_secondary'):
                shape.replace(i, ik_con)
            for i in ctx.filter().tag_equal('controller').tag_equal('fk').tag_equal('feather_secondary'):
                shape.replace(i, fk_con)

    finally:
        cc.delete(main_con, ik_con, fk_con)


def show():
    core.log_docker(title='radiant_joint_tool', doit_text="选择羽毛关节", form=(
        item.Select("父控制器"),
        item.Select("父蒙皮关节"),
        item.Select("控制曲面"),
        item.Select("控制曲线"),
        item.IntSlider("Ik控制器数量", 2, 10, 3),
        item.IntSlider("Fk控制器数量", 2, 10, 5),
    ), func=call)


if __name__ == "__main__":
    show()
