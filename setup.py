#!/usr/bin/python
# -*-coding:utf-8 -*-
from __future__ import unicode_literals, print_function

import sys

import setuptools

lib_name = 'pyeal'

author = 'cpcgskill',
author_email = 'cpcgskill@outlook.com'

version = '0.5.1'

description = 'Python 打包编译工具'
with open("README.md", "rb") as f:
    long_description = f.read().decode(encoding='utf-8')

project_homepage = 'https://github.com/cpcgskill/pyeal'
project_urls = {
    'Bug Tracker': 'https://github.com/cpcgskill/pyeal/issues',
}
license = 'Apache Software License (Apache 2.0)'

python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*'
install_requires = [
    'astunparse==1.6.3',
]

console_scripts = [
    "pyeal=pyeal.cli:main",
]
# # 想按照不同版本启用不同入口的但是whl是静态打包好了的，并且不知道怎么指定。gz格式则不知道为什么单独打包会报错
# # error removing pyeal-0.5.0: [WinError 145] 目录不是空的。: 'pyeal-0.5.0\\src'
# # error removing pyeal-0.5.0: [WinError 145] 目录不是空的。: 'pyeal-0.5.0'
# # 明明whl和gz一起打包时是正常的，也找不到相关资料，所以暂时不实现这个功能了
# if sys.version_info.major < 3:
#     console_scripts = [
#         "pyeal=pyeal.cli:main",
#         "pyeal-py2=pyeal.cli:main",
#     ]
# else:
#     console_scripts = [
#         "pyeal=pyeal.cli:main",
#         "pyeal-py3=pyeal.cli:main",
#     ]

setuptools.setup(
    name=lib_name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=project_homepage,
    project_urls=project_urls,
    license=license,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    package_dir={"": "src"},
    # # 使用自动搜索
    # packages=setuptools.find_packages(where="src"),
    packages=['pyeal', 'pyeal.codekit'],
    python_requires=python_requires,
    # 指定依赖
    install_requires=install_requires,
    # 指定启用包数据如log.ico这样的文件
    include_package_data=True,
    entry_points={
        # 控制台脚本
        "console_scripts": console_scripts,
    },
)
