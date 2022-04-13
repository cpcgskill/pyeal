# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/4/13 0:11
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function, division
import io
import ast
import contextlib
from pyeal.exc import *


def _repr(o):
    s = repr(o)
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return s


class Unparser(object):
    def __init__(self, tree, f=None):
        if f is None:
            f = io.StringIO()
        self.f = f
        self.col_off = 0
        self._dispatch(tree)
        # 记录最后一个写入的字符串， 配合_write_code， _write_line方法可以避免不必要的空行
        self.end_char = ''

    def _write_code(self, *s):
        if len(s) > 0:
            for i in s:
                if isinstance(i, bytes):
                    self.f.write(i.decode('utf-8'))
                else:
                    self.f.write(i)
            else:
                if len(i) > 0:
                    self.end_char = i[-1]

    @contextlib.contextmanager
    def _write_block(self):
        self.col_off += 1
        yield
        self.col_off -= 1

    @contextlib.contextmanager
    def _write_line(self):
        self._write_code('    ' * self.col_off)
        yield
        if self.end_char != '\n':
            self._write_code('\n')

    def _dispatch(self, node):
        if isinstance(node, ast.slice):
            self._dispatch_slice(node)
        elif isinstance(node, ast.stmt):
            self._dispatch_stmt(node)
        elif isinstance(node, ast.expr):
            self._dispatch_expr(node)
        elif isinstance(node, ast.unaryop):
            self._dispatch_unaryop(node)
        elif isinstance(node, ast.boolop):
            self._dispatch_boolop(node)
        elif isinstance(node, ast.operator):
            self._dispatch_operator(node)

        elif isinstance(node, ast.Module):
            self._module(node)
        elif isinstance(node, ast.ExceptHandler):
            self._except_handler(node)

        elif isinstance(node, ast.cmpop):
            self._cmpop(node)

        else:
            raise SealException("无法识别的节点: ", node)

    def _dispatch_slice(self, node):
        """
        :type node: ast.slice
        """
        if isinstance(node, ast.Index):
            self._dispatch(node.value)
        elif isinstance(node, ast.Slice):
            if node.lower is not None:
                self._dispatch(node.lower)
            self._write_code(':')
            if node.upper is not None:
                self._dispatch(node.upper)
            self._write_code(':')
            if node.step is not None:
                self._dispatch(node.step)
        elif isinstance(node, ast.ExtSlice):
            end_id = len(node.dims) - 1
            for id_, i in enumerate(node.dims):
                self._dispatch(i)
                if id_ != end_id:
                    self._write_code(', ')
        else:
            raise SealException("无法识别的节点: ", node)

    def _dispatch_expr(self, node):
        """
        :type node: ast.expr
        """
        if False:
            pass
        elif isinstance(node, ast.Yield):
            self._write_code('yield ')
            self._dispatch(node.value)

        elif isinstance(node, ast.Attribute):
            self._attribute(node)
        elif isinstance(node, ast.Call):
            self._call(node)
        elif isinstance(node, ast.Compare):
            self._compare(node)
        elif isinstance(node, ast.Subscript):
            self._subscript(node)
        elif isinstance(node, ast.IfExp):
            self._if_exp(node)

        elif isinstance(node, ast.UnaryOp):
            self._unary_op(node)
        elif isinstance(node, ast.BoolOp):
            self._bool_op(node)

        elif isinstance(node, ast.Set):
            self._set(node)
        elif isinstance(node, ast.Dict):
            self._dict(node)
        elif isinstance(node, ast.List):
            self._list(node)
        elif isinstance(node, ast.Tuple):
            self._tuple(node)

        elif isinstance(node, ast.Str):
            self._str(node)
        elif isinstance(node, ast.Num):
            self._num(node)
        elif isinstance(node, ast.Name):
            self._name(node)

        else:
            raise SealException("无法识别的节点: ", node)

    def _dispatch_stmt(self, node):
        """
        :type node: ast.stmt
        """
        if False:
            pass
        elif isinstance(node, ast.ClassDef):
            self._class_def(node)
        elif isinstance(node, ast.FunctionDef):
            self._function_def(node)
        elif isinstance(node, ast.For):
            self._for(node)
        elif isinstance(node, ast.If):
            self._if(node)
        elif isinstance(node, ast.Return):
            self._return(node)
        elif isinstance(node, ast.Pass):
            self._write_code('pass')
        elif isinstance(node, ast.Raise):
            self._write_code('raise ')
            self._dispatch(node.type)
        elif isinstance(node, ast.Global):
            self._write_code('global ', *node.names)

        elif isinstance(node, ast.AugAssign):
            self._dispatch(node.target)
            self._write_code(' = ')
            self._dispatch(node.target)
            self._dispatch(node.op)
            self._dispatch(node.value)

        elif isinstance(node, ast.Expr):
            self._expr(node)
        elif isinstance(node, ast.ImportFrom):
            self._import_from(node)
        elif isinstance(node, ast.Import):
            self._import(node)
        elif isinstance(node, ast.Assign):
            self._assign(node)

        elif isinstance(node, ast.With):
            self._with(node)
        elif isinstance(node, ast.TryExcept):
            self._try_except(node)
        elif isinstance(node, ast.TryFinally):
            self._try_finally(node)


        else:
            raise SealException("无法识别的节点: ", node)

    def _dispatch_unaryop(self, node):
        typemap = {
            ast.Invert: '~',
            ast.Not: 'not',
            ast.UAdd: '+',
            ast.USub: '-',
        }
        v = typemap.get(type(node), None)
        if v is None:
            raise SealException("无法识别的节点: ", node)
        self._write_code(v)

    def _dispatch_boolop(self, node):
        typemap = {
            ast.And: 'and',
            ast.Or: 'or',
        }
        v = typemap.get(type(node), None)
        if v is None:
            raise SealException("无法识别的节点: ", node)
        self._write_code(v)

    def _dispatch_operator(self, node):
        typemap = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
        }
        v = typemap.get(type(node), None)
        if v is None:
            raise SealException("无法识别的节点: ", node)
        self._write_code(v)

    def _module(self, node):
        """
        :type node: ast.Module
        """
        for i in node.body:
            with self._write_line():
                self._dispatch(i)

    def _class_def(self, node):
        """
        :type node: ast.ClassDef
        """

        # 类头部输出
        self._write_code('class ', node.name, '(')
        bases = ', '.join((i.id for i in node.bases))
        self._write_code(bases, '):\n')

        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _function_def(self, node):
        """
        :type node: ast.FunctionDef
        """

        # 函数头部输出
        self._write_code('def ', node.name, '(')
        args = ', '.join((i.id for i in node.args.args))
        self._write_code(args, '):\n')

        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _for(self, node):
        """
        :type node: ast.For
        """

        # 函数头部输出
        self._write_code('for ')
        self._dispatch(node.target)
        self._write_code(' in ')
        self._dispatch(node.iter)
        self._write_code(':\n')

        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _if(self, node):
        """
        :type node: ast.If
        """

        # 函数头部输出
        self._write_code('if ')
        self._dispatch(node.test)
        self._write_code(':\n')

        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _expr(self, node):
        """
        :type node: ast.Expr
        """
        self._dispatch(node.value)

    def _import_from(self, node):
        """
        :type node: ast.ImportFrom
        """
        co = 'from {} import '.format(node.module, )
        imps = (i.name if i.asname is None else '{} as {}'.format(i.name, i.asname) for i in node.names)
        imps = ', '.join(imps)
        self._write_code(co, imps)

    def _import(self, node):
        """
        :type node: ast.Import
        """
        imps = (i.name if i.asname is None else '{} as {}'.format(i.name, i.asname) for i in node.names)
        imps = ', '.join(imps)
        self._write_code('import ', imps)

    def _compare(self, node):
        """
        :type node: ast.Compare
        """
        self._dispatch(node.left)
        for o, c in zip(node.ops, node.comparators):
            self._write_code(' ')
            self._dispatch(o)
            self._write_code(' ')
            self._dispatch(c)

    def _assign(self, node):
        """
        :type node: ast.Assign
        """
        self._dispatch(node.targets[0])
        self._write_code(' = ')
        self._dispatch(node.value)

    def _with(self, node):
        """
        :type node: ast.With
        """
        self._write_code('with ')
        self._dispatch(node.context_expr)
        self._write_code(' as ')
        self._dispatch(node.optional_vars)
        self._write_code(':\n')
        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _try_except(self, node):
        """
        :type node: ast.TryExcept
        """
        self._write_code('try:\n')
        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)
        for i in node.handlers:
            with self._write_line():
                self._dispatch(i)

    def _try_finally(self, node):
        """
        :type node: ast.TryFinally
        """
        for i in node.body:
            self._dispatch(i)
        with self._write_line():
            self._write_code('finally:\n')
        with self._write_block():
            for i in node.finalbody:
                with self._write_line():
                    self._dispatch(i)

    def _except_handler(self, node):
        """
        :type node: ast.ExceptHandler
        """
        if node.name is None:
            self._write_code('except:\n')
        elif node.type is None:
            self._write_code('except ')
            self._dispatch(node.name)
            self._write_code(':\n')
        else:
            self._write_code('except ')
            self._dispatch(node.name)
            self._write_code(' as ')
            self._dispatch(node.type)
            self._write_code(':\n')
        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _return(self, node):
        """
        :type node: ast.Return
        """
        self._write_code('return ')
        self._dispatch(node.value)

    def _call(self, node):
        """
        :type node: ast.Call
        """
        self._dispatch(node.func)
        self._write_code('(')
        for i in node.args:
            self._dispatch(i)
            self._write_code(', ')
        self._write_code(')')

    def _attribute(self, node):
        """
        :type node: ast.Attribute
        """
        self._dispatch(node.value)
        self._write_code('.', node.attr)

    def _subscript(self, node):
        """
        :type node: ast.Subscript
        """

        self._dispatch(node.value)
        self._write_code('[')
        self._dispatch(node.slice)
        self._write_code(']')

    def _if_exp(self, node):
        """
        :type node: ast.IfExp
        """
        self._dispatch(node.body)
        self._write_code(' if ')
        self._dispatch(node.test)
        self._write_code(' else ')
        self._dispatch(node.orelse)

    def _unary_op(self, node):
        """
        :type node: ast.UnaryOp
        """
        self._dispatch(node.op)
        self._dispatch(node.operand)

    def _bool_op(self, node):
        """
        :type node: ast.BoolOp
        """
        end_id = len(node.values) - 1
        for id_, i in enumerate(node.values):
            self._dispatch(i)
            if id_ != end_id:
                self._write_code(' ')
                self._dispatch(node.op)
                self._write_code(' ')
        self._dispatch(node.op)

    def _set(self, node):
        """
        :type node: ast.Set
        """
        self._write_code('{')
        if len(node.elts) > 0:
            for i in node.elts:
                self._dispatch(i)
                self._write_code(', ')
        self._write_code('}')

    def _dict(self, node):
        """
        :type node: ast.Dict
        """
        self._write_code('{')
        if len(node.keys) > 0:
            for k, v in zip(node.keys, node.value):
                self._dispatch(k)
                self._write_code(': ')
                self._dispatch(v)
                self._write_code(', ')
        self._write_code('}')

    def _list(self, node):
        """
        :type node: ast.List
        """
        self._write_code('[')
        if len(node.elts) > 0:
            for i in node.elts:
                self._dispatch(i)
                self._write_code(', ')
        self._write_code(']')

    def _tuple(self, node):
        """
        :type node: ast.Tuple
        """
        self._write_code('(')
        if len(node.elts) > 0:
            for i in node.elts:
                self._dispatch(i)
                self._write_code(', ')
        self._write_code(')')

    def _str(self, node):
        """
        :type node: ast.Str
        """
        co = _repr(node.s)
        if co[0] == 'b' or co[0] == 'u':
            co = co[1:]
        if isinstance(co, bytes):
            self._write_code('b', co)
        else:
            self._write_code('u', co)

    def _num(self, node):
        """
        :type node: ast.Num
        """
        self._write_code(repr(node.n))

    def _name(self, node):
        """
        :type node: ast.Name
        """
        self._write_code(node.id)

    def _cmpop(self, node):
        """
        :type node: ast.cmpop
        """
        typemap = {
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.In: 'in',
            ast.NotIn: 'not in',
            ast.Eq: '==',
            ast.NotEq: '!=',
        }
        v = typemap.get(type(node), None)
        if v is None:
            raise SealException("无法识别的节点: ", node)
        self._write_code(' ', v, ' ')


def parser(code):
    """
    :type code: bytes
    :rtype: str
    """
    return ast.parse(code)


def unparse(tree):
    f = io.StringIO()
    Unparser(tree, f)
    return f.getvalue()
