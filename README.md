# toughcli

toughcli 是一个基于toughradius以及相关软件的工具包。

## 运行环境

    - Linux/Mac OSX/BSD
    - Python 2.7/PyPy
    - Click

## 安装

    easy_install toughcli 或者 pip install toughcli

## 使用说明

查看帮助：

    toughcli --help

    Usage: toughcli [OPTIONS] COMMAND [ARGS]...

    Options:
      --version
      --help     Show this message and exit.

    Commands:
      docker
      mysql
      radius
      redis
      upgrade

查看服务器信息：

    $ toughcli --info
    Linux distribution: CentOS Linux,7.2.1511,Core
    Cli version toughcli: 0.0.7
    Env_home: /root
    Env_path: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/usr/local/bin
    Server platform: Linux-3.10.0-327.4.5.el7.x86_64-x86_64-with-centos-7.2.1511-Core,x86_64
    Python version: CPython,2.7.5
    Docker version 1.8.2-el7.centos, build a01dc02/1.8.2
    docker-compose version 1.5.2, build 7240ff3

