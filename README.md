# pyeal

新的 Python 打包编译工具

包名称是python seal的意思

## 目录

- [快速开始](#快速开始)
- [功能介绍](#功能介绍)
- [版权说明](#版权说明)

### 快速开始
注意下方的python是你的Python, 正常情况下可以直接通过python调用,
而Maya的python一般是C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe
#### 安装

```commandline
python -m pip install pyeal
```

#### 初始化

```commandline
mkdir test_pyeal
cd test_pyeal
python -m pyeal init
```

### 编译

```commandline
python -m pyeal go
```

### 功能介绍

目前大部分操作都通过命令行调用， 依赖于config.json配置功能。

#### 配置
```json
{
  "type": "MayaPlugin",
  "source": "src",
  "target": "build",
  "name": "dg_editor_0_1_0",
  "exec_script": "import main;main.main()",
  "log": "log.ico",
  "annotation": "这是这个插件的注释~"
}
```
##### 配置的各项参数
* type: 你要封装的类型目前仅支持MayaPlugin
* source： 源目录
* target： 目标目录
* name： 你要封装的名称，一般作为名称空间或者名称前缀
* exec_script： 启动脚本， 一般是导入某一个模块，然后执行启动函数
* log： log文件名
* annotation： 注释


### 版权说明

该项目签署了Apache-2.0 授权许可，详情请参阅 LICENSE