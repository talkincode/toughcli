#!/usr/bin/env python
#coding:utf-8
import os

def auto_install():
    os.system("curl -sSL https://get.daocloud.io/docker | sh")
    os.system("curl -L https://get.daocloud.io/docker/compose/releases/download"
              "/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose")
    os.system("ln -s /usr/local/bin/docker-compose //usr/bin/docker-compose")
    os.system("service docker start")




