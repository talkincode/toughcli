#!/usr/bin/env python
import sys,os,time,datetime
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughcli import __version__

env.user = 'root'
env.hosts = ['121.201.63.77']

def pub():
    try:
        local("git add . && git ci -am '%s' && git push origin master"%raw_input("commit"))
    except:
        pass
    with cd("/opt/toughcli"):
        run("git pull origin master")
        run("make upload")