#!/usr/bin/env python
#coding:utf-8

import sys,os
from toughguy.trshell import shell

docker_compose_fmt = '''dbmysql:
    container_name: mysql_{instance}
    image: "index.alauda.cn/toughstruct/mysql"
    privileged: true
    net: "host"
    environment:
        - MYSQL_MAX_MEM={max_mem}
        - MYSQL_USER={username}
        - MYSQL_PASSWORD={password}
        - MYSQL_DATABASE={dbname}
        - MYSQL_ROOT_PASSWORD={root_password}
    restart: always
    ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000    
    volumes:
        - {rundir}/{instance}/data:/var/lib/mysql
        - {rundir}/{instance}/backup:/var/backup
'''.format

def docker_install(rundir,instance='mydb',
        username=None,password=None,root_password=None,dbname=None,max_mem=None):

    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    params = dict(
        rundir=rundir,
        instance=instance,
        username=username,
        password=password,
        dbname=dbname,
        root_password=root_password,
        max_mem=max_mem
    )
    with open("{0}/docker-compose.yaml".format(target_dir),'wb') as dcfile:
        dcfile.write(docker_compose_fmt(**params))

    shell.run('cd {0} && docker-compose up -d && docker-compose ps'.format(target_dir))



