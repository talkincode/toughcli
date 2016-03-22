#!/usr/bin/env python
#coding:utf-8

from toughguy.trshell import shell

def daocloud_install():
    rcode1,rcode2 = 1,1
    rcode1,_,_ = shell.run("curl -sSL https://get.daocloud.io/docker | sh")
    if rcode1 == 0:
        rcode2,_,_ = shell.run("curl -L https://get.daocloud.io/docker/compose/releases/download"
                              "/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose")
    if rcode2 == 0:
        shell.run("ln -s /usr/local/bin/docker-compose /usr/local/bin/docp")

    if (rcode1,rcode2) == (0,0):
        shell.run("service docker start")

def centos6_install():
    shell.run("epel-release")
    shell.run("yum install docker-io")
    shell.run("chkconfig docker on")
    shell.run("service docker start")

def centos7_install():
    shell.run("epel-release")
    shell.run("yum install docker")
    shell.run("systemctl enable docker")
    shell.run("service docker start")


def ubuntu_install():
    shell.run("sudo apt-get update")
    shell.run("sudo apt-get install docker.io")
    shell.run("sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker")
    shell.run("sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io")



