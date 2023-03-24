# pyeal

新的 Python 打包编译工具

包名称是python seal的意思

## 目录

- [快速开始](#快速开始)
- [功能介绍](#功能介绍)
- [版权说明](#版权说明)

### 快速开始

注意下方的python是你的Python, 正常情况下可以直接通过python调用, 而Maya的python一般是C:\Program
Files\Autodesk\Maya2018\bin\mayapy.exe

#### 安装

```commandline
python -m pip install pyeal
```

##### 如果你使用mayapy进行安装请注意以下几点:

1. 请确认pip给你安装的位置是否在python的搜索路径下, 
   如果不存在可以在“pip install”后加“-t 目标路径” 来解决这个问题.
2. 请确认pyeal.exe可以被命令行查找到, 它一般在pip给你安装的库的位置的../../Scripts下.
   如果无法被找到请将其所在的目录添加到环境变量中.
3. 如果出现第一次安装pyeal不会出现以上情况, 而第二次出现或者反过来.请按情况处理即可, 
   这只是python2、python3、maya、windows其中一个出现了未知的变化而已导致的更改而已.
4. 建议打开管理员进行安装否则会安装到
   “C:\Users\PC\AppData\Roaming\Python\Python27\site-packages”下, 
   这将导致库文件和普通的python2混合在一起.
5. 如果出现了不在上述情况中的错误请提issue

#### 初始化

```commandline
mkdir test_pyeal
cd test_pyeal
python -m pyeal init
```

### 编译

```commandline
python -m pyeal build
```

### 功能介绍

目前大部分操作都通过命令行调用, 依赖于pyeal.json配置功能.

#### 配置

```json
{
  "type": "package",
  "name": "your_name",
  "exec_script": ""
}
```

##### 配置的各项参数

* type[str]: 你要封装的类型目前仅支持package, maya-plugin.
* name[str]: 你要封装的名称, 一般作为名称空间或者名称前缀.
* imp_name[str]: 打包完成后的导入名称, 未填则为name的值.
* exec_script[str]: 启动脚本, 一般是导入某一个模块, 然后执行启动函数.
* annotation[str]: 注释字符串, 在构建类型为maya-plugin或其他可以添加注释的的编译类型的时候被使用.
* outer_lib[list(str)]: 额外的库目录.

#### 文件约定

* icon.ico logo文件, 在构建类型为maya-plugin或其他需要图标的编译类型的时候被使用的文件.
* pyeal.json 构建配置文件.
* index.py 在编写复杂的启动脚本时, 替代exec_script配置项的文件.
* src/ 源代码目录.
* lib/ 依赖库目录.
* build/ 输出目录.

### 版权说明

该项目签署了Apache-2.0 授权许可, 详情请参阅 LICENSE