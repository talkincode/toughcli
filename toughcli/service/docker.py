#!/usr/bin/env python
#coding:utf-8
import platform,os

def daocloud_install():
    os.system("sudo curl -sSL https://get.daocloud.io/docker | sh")
    os.system("sudo curl -L https://get.daocloud.io/docker/compose/releases/download"
              "/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose")
    os.system("sudo service docker start")

def centos6_install():
    os.system("sudo yum install epel-release")
    os.system("sudo yum install docker-io")
    os.system("sudo chkconfig docker on")
    os.system("sudo service docker start")

def centos7_install():
    os.system("sudo yum install epel-release")
    os.system("sudo yum install docker")
    os.system("sudo systemctl enable docker")
    os.system("sudo service docker start")


def ubuntu_install():
    os.system("sudo apt-get update")
    os.system("sudo apt-get install docker.io")
    os.system("sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker")
    os.system("sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io")


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




