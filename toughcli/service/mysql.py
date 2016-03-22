#!/usr/bin/env python
#coding:utf-8

import os, sys, click
from toughcli.toughshell import shell
import shutil

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

def docker_install(rundir,instance):
    username = click.prompt('Please enter mysql user [mydb]', default='mydb')
    password = click.prompt('Please enter mysql password [mypwd]', default='mypwd')
    root_password = click.prompt('Please enter mysql root password [none]', default='')
    dbname = click.prompt('Please enter mysql database [mydb]', default='mydb')
    max_mem = click.prompt('Please enter mysql max_mem [none]', default='', 
        type=click.Choice(['', '512M','1G','4G']))

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


def docker_op(rundir,instance,op):
    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        click.echo(click.style("instance {0} not exist".format(instance),fg='red'))
    if op in ('logs','start','stop','restart','kill','rm','backup'):
        if op == 'backup':
            shell.run('docker exec -it mysql_{0} sh -c "dbutils backup" '.format(instance))
        else:
            shell.run('cd {0} && docker-compose {1} dbmysql'.format(target_dir,op))

        if op == 'rm' and click.confirm('Do you want to remove mysql data ({0})?'.format(target_dir)):
            shutil.rmtree(target_dir)
    else:
        click.echo(click.style("unsupported operation {0}".format(op),fg='red'))

    
    


















