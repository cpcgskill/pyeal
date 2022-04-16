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
        # 记录最后一个写入的字符串， 配合_write_code， _write_line方法可以避免不必要的空行
        self.end_char = ''

        self._dispatch(tree)

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
        if self.end_char == '\n':
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
        elif isinstance(node, ast.cmpop):
            self._dispatch_cmpop(node)

        elif isinstance(node, ast.mod):
            self._dispatch_mod(node)

        elif isinstance(node, ast.ExceptHandler):
            self._except_handler(node)
        elif isinstance(node, ast.comprehension):
            self._comprehension(node)

        else:
            raise SealException("无法识别的节点: ", node)

    def _dispatch_mod(self, node):
        """
        :type node: ast.mod
        """
        if False:
            pass
        elif isinstance(node, ast.Module):
            self._module(node)
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
            if node.value is None:
                self._write_code('yield')
            else:
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
        elif isinstance(node, ast.BinOp):
            self._bin_op(node)

        elif isinstance(node, ast.Set):
            self._set(node)
        elif isinstance(node, ast.Dict):
            self._dict(node)
        elif isinstance(node, ast.List):
            self._list(node)
        elif isinstance(node, ast.Tuple):
            self._tuple(node)

        elif isinstance(node, ast.DictComp):
            self._dict_comp(node)
        elif isinstance(node, ast.SetComp):
            self._set_comp(node)
        elif isinstance(node, ast.ListComp):
            self._list_comp(node)
        elif isinstance(node, ast.GeneratorExp):
            self._generator_exp(node)

        elif isinstance(node, ast.Str):
            self._str(node)
        elif isinstance(node, ast.Num):
            self._num(node)
        elif isinstance(node, ast.Name):
            self._name(node)
        elif isinstance(node, ast.Lambda):
            self._lambda(node)

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
            if node.type is None:
                self._write_code('raise')
            else:
                self._write_code('raise ')
                self._dispatch(node.type)
        elif isinstance(node, ast.Assert):
            self._write_code('assert ')
            self._dispatch(node.test)
            if node.msg is not None:
                self._write_code(', ')
                self._dispatch(node.msg)
        elif isinstance(node, ast.Print):
            self._write_code('print ')
            for id_, i in enumerate(node.values):
                if id_ != 0:
                    self._write_code(', ')
                self._dispatch(i)
        elif isinstance(node, ast.Delete):
            self._write_code('del ')
            for id_, i in enumerate(node.targets):
                if id_ != 0:
                    self._write_code(', ')
                self._dispatch(i)

        elif isinstance(node, ast.Global):
            self._write_code('global ', ', '.join(node.names))
        elif isinstance(node, ast.Continue):
            self._write_code('continue')
        elif isinstance(node, ast.Break):
            self._write_code('break')

        elif isinstance(node, ast.AugAssign):
            self._dispatch(node.target)
            self._write_code(' ')
            self._dispatch(node.op)
            self._write_code('= ')
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
        elif isinstance(node, ast.While):
            self._while(node)
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
            ast.FloorDiv: '//',
            ast.RShift: '>>',
            ast.LShift: '<<',
            ast.BitAnd: '&',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.Mod: '%',
            ast.Pow: '**',
        }
        v = typemap.get(type(node), None)
        if v is None:
            raise SealException("无法识别的节点: ", node)
        self._write_code(v)

    def _dispatch_cmpop(self, node):
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
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Lt: '<',
            ast.LtE: '<=',
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
        for i in node.decorator_list:
            with self._write_line():
                self._write_code('@')
                self._dispatch(i)
        # 类头部输出
        with self._write_line():
            self._write_code('class ', node.name, '(')
            end_id = len(node.bases) - 1
            for id_, i in enumerate(node.bases):
                self._dispatch(i)
                if id_ != end_id:
                    self._write_code(', ')
            self._write_code('):')

        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _function_def(self, node):
        """
        :type node: ast.FunctionDef
        """
        for i in node.decorator_list:
            with self._write_line():
                self._write_code('@')
                self._dispatch(i)
        # 函数头部输出
        with self._write_line():
            self._write_code('def ', node.name, '(')
            end_id = len(node.args.args) - 1
            id_ = 0
            if node.args.vararg is not None:
                end_id += 1
            if node.args.kwarg is not None:
                end_id += 1

            args = node.args.args[:len(node.args.args) - len(node.args.defaults)]
            def_args = node.args.args[len(node.args.args) - len(node.args.defaults):]
            for i in args:
                self._dispatch(i)
                if id_ != end_id:
                    self._write_code(', ')
                id_ += 1
            for i, v in zip(def_args, node.args.defaults):
                self._dispatch(i)
                self._write_code('=')
                self._dispatch(v)
                if id_ != end_id:
                    self._write_code(', ')
                id_ += 1
            if node.args.vararg is not None:
                self._write_code('*', node.args.vararg)
                if id_ != end_id:
                    self._write_code(', ')
                id_ += 1
            if node.args.kwarg is not None:
                self._write_code('**', node.args.kwarg)
                if id_ != end_id:
                    self._write_code(', ')
                id_ += 1
            self._write_code('):')

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
        if len(node.orelse) > 0:
            with self._write_line():
                self._write_code('else:')
            with self._write_block():
                for i in node.orelse:
                    with self._write_line():
                        self._dispatch(i)

    def _if(self, node, is_elif=False):
        """
        :type node: ast.If
        :type is_elif: bool
        """

        # 函数头部输出
        if is_elif:
            self._write_code('elif ')
        else:
            self._write_code('if ')
        self._dispatch(node.test)
        self._write_code(':\n')

        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)
        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            node = node.orelse[0]
            with self._write_line():
                self._if(node, True)
        else:
            if len(node.orelse) > 0:
                with self._write_line():
                    self._write_code('else:\n')
                with self._write_block():
                    for i in node.orelse:
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

        co = 'from {}{} import '.format(''.join(('.' for i in range(node.level))),
                                        '' if node.module is None else node.module)
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
        if node.optional_vars is not None:
            self._write_code(' as ')
            self._dispatch(node.optional_vars)
        self._write_code(':\n')
        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)

    def _while(self, node):
        """
        :type node: ast.While
        """
        self._write_code('while ')
        self._dispatch(node.test)
        self._write_code(':\n')
        with self._write_block():
            for i in node.body:
                with self._write_line():
                    self._dispatch(i)
        if len(node.orelse) > 0:
            with self._write_line():
                self._write_code('else:')
            with self._write_block():
                for i in node.orelse:
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
        if len(node.orelse) > 0:
            with self._write_line():
                self._write_code('else:')
            with self._write_block():
                for i in node.orelse:
                    with self._write_line():
                        self._dispatch(i)

    def _try_finally(self, node):
        """
        :type node: ast.TryFinally
        """
        if len(node.body) == 1 and isinstance(node.body[0], ast.TryExcept):
            with self._write_line():
                self._dispatch(node.body[0])
        else:
            with self._write_line():
                self._write_code('try:')
            with self._write_block():
                for i in node.body:
                    with self._write_line():
                        self._dispatch(i)
        with self._write_line():
            self._write_code('finally:')
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
        if node.value is None:
            self._write_code('return')
        else:
            self._write_code('return ')
            self._dispatch(node.value)

    def _call(self, node):
        """
        :type node: ast.Call
        """
        self._dispatch(node.func)
        self._write_code('(')
        id_ = 0
        end_id = len(node.args) + len(node.keywords) - 1
        if node.starargs is not None:
            end_id += 1
        if node.kwargs is not None:
            end_id += 1

        for i in node.args:
            self._dispatch(i)
            if id_ != end_id:
                self._write_code(', ')
                id_ += 1
        for i in node.keywords:
            self._write_code(i.arg, '=')
            self._dispatch(i.value)
            if id_ != end_id:
                self._write_code(', ')
                id_ += 1
        if node.starargs is not None:
            self._write_code('*')
            self._dispatch(node.starargs)
            if id_ != end_id:
                self._write_code(', ')
                id_ += 1
        if node.kwargs is not None:
            self._write_code('**')
            self._dispatch(node.kwargs)
            if id_ != end_id:
                self._write_code(', ')
                id_ += 1
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
        self._write_code(' ')
        self._dispatch(node.operand)

    def _bool_op(self, node):
        """
        :type node: ast.BoolOp
        """
        for id_, i in enumerate(node.values):
            if id_ != 0:
                self._write_code(' ')
                self._dispatch(node.op)
                self._write_code(' ')
            self._dispatch(i)

    def _bin_op(self, node):
        """
        :type node: ast.BinOp
        """
        self._dispatch(node.left)
        self._write_code(' ')
        self._dispatch(node.op)
        self._write_code(' ')
        self._dispatch(node.right)

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
            for k, v in zip(node.keys, node.values):
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

    def _dict_comp(self, node):
        """
        :type node: ast.DictComp
        """
        self._write_code('{')
        self._dispatch(node.key)
        self._write_code(': ')
        self._dispatch(node.value)
        for i in node.generators:
            self._write_code(' ')
            self._dispatch(i)
        self._write_code('}')

    def _set_comp(self, node):
        """
        :type node: ast.SetComp
        """
        self._write_code('{')
        self._dispatch(node.elt)
        for i in node.generators:
            self._write_code(' ')
            self._dispatch(i)
        self._write_code('}')

    def _list_comp(self, node):
        """
        :type node: ast.ListComp
        """
        self._write_code('[')
        self._dispatch(node.elt)
        for i in node.generators:
            self._write_code(' ')
            self._dispatch(i)
        self._write_code(']')

    def _generator_exp(self, node):
        """
        :type node: ast.GeneratorExp
        """
        self._write_code('(')
        self._dispatch(node.elt)
        for i in node.generators:
            self._write_code(' ')
            self._dispatch(i)
        self._write_code(')')

    def _comprehension(self, node):
        """
        :type node: ast.comprehension
        """
        self._write_code('for ')
        self._dispatch(node.target)
        self._write_code(' in ')
        self._dispatch(node.iter)
        for i in node.ifs:
            self._write_code(' if ')
            self._dispatch(i)

    def _str(self, node):
        """
        :type node: ast.Str
        """
        self._write_code(repr(node.s))
        # co = _repr(node.s)
        # if co[0] == 'b' or co[0] == 'u':
        #     co = co[1:]
        # if isinstance(co, bytes):
        #     self._write_code('b', co)
        # else:
        #     self._write_code('u', co)

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

    def _lambda(self, node):
        """
        :type node: ast.Lambda
        """
        self._write_code('lambda ')
        end_id = len(node.args.args) - 1
        id_ = 0
        if node.args.vararg is not None:
            end_id += 1
        if node.args.kwarg is not None:
            end_id += 1

        args = node.args.args[:len(node.args.args) - len(node.args.defaults)]
        def_args = node.args.args[len(node.args.args) - len(node.args.defaults):]
        for i in args:
            self._dispatch(i)
            if id_ != end_id:
                self._write_code(', ')
            id_ += 1
        for i, v in zip(def_args, node.args.defaults):
            self._dispatch(i)
            self._write_code('=')
            self._dispatch(v)
            if id_ != end_id:
                self._write_code(', ')
            id_ += 1
        if node.args.vararg is not None:
            self._write_code('*', node.args.vararg)
            if id_ != end_id:
                self._write_code(', ')
            id_ += 1
        if node.args.kwarg is not None:
            self._write_code('**', node.args.kwarg)
            if id_ != end_id:
                self._write_code(', ')
            id_ += 1
        self._write_code(':')

        self._dispatch(node.body)


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
