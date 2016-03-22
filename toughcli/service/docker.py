#!/usr/bin/env python
#coding:utf-8
import platform
from toughcli.toughshell import shell

def daocloud_install():
    shell.run("sudo curl -sSL https://get.daocloud.io/docker | sh")
    shell.run("sudo curl -L https://get.daocloud.io/docker/compose/releases/download"
              "/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose")
    shell.run("sudo service docker start")

def centos6_install():
    shell.run("sudo yum install epel-release")
    shell.run("sudo yum install docker-io")
    shell.run("sudo chkconfig docker on")
    shell.run("sudo service docker start")

def centos7_install():
    shell.run("sudo yum install epel-release")
    shell.run("sudo yum install docker")
    shell.run("sudo systemctl enable docker")
    shell.run("sudo service docker start")


def ubuntu_install():
    shell.run("sudo apt-get update")
    shell.run("sudo apt-get install docker.io")
    shell.run("sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker")
    shell.run("sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io")


def auto_install():
    name,ver,_ = platform.dist()
    if name == 'centos' and ver.startswith("7"):
        centos7_install()
    elif name == 'centos' and ver.startswith("6"):
        centos6_install()
    elif name in ('ubuntu','debian'):
        ubuntu_install()
    else:
        daocloud_install()




