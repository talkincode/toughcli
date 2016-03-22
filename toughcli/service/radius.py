#!/usr/bin/env python
#coding:utf-8
import os, sys, click
from toughcli.toughshell import shell
from toughcli.rundata import rundata
import shutil


docker_compose_fmt = '''redis:
    image: "index.alauda.cn/tutum/redis"
    expose:
        - "6379"
    environment:
        - REDIS_MAXMEMORY=512mb
        - REDIS_PASS=tredis
    restart: always   
radius:
    container_name: radius_{instance}
    command: pypy /opt/toughradius/toughctl --run -f {worker_num}
    image: "index.alauda.cn/toughstruct/toughradius:{release}"
    net: "hosts"
    links:
        - redis:redis
    ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000
    environment:
        - REDIS_URL=redis
        - REDIS_PORT=6379
        - REDIS_PWD=tredis
        - DB_TYPE=mysql
        - DB_URL=mysql://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8
    restart: always
    volumes:
        - {rundir}/{instance}:/var/toughradius
'''.format


docker_compose_fmt2 = '''redis:
    image: "index.alauda.cn/tutum/redis"
    expose:
        - "6379"
    environment:
        - REDIS_MAXMEMORY=512mb
        - REDIS_PASS=tredis
    restart: always   
radius:
    container_name: radius_{instance}
    command: pypy /opt/toughradius/toughctl --run -f {worker_num}
    image: "index.alauda.cn/toughstruct/toughradius:{release}"
    net: "hosts"
    links:
        - redis:redis
    environment:
        - REDIS_URL=redis
        - REDIS_PORT=6379
        - REDIS_PWD=tredis
    restart: always
    volumes:
        - {rundir}/{instance}:/var/toughradius
'''.format


def docker_install(rundir,instance,work_num,release):
    yaml_cfg = docker_compose_fmt
    mysql_instances = rundata.datas['mysql'].keys()
    mysql_instances = [''] + mysql_instances
    params_cfg = {}
    mysql_ins = click.prompt('Please select mysql instance [defaule sqlite]', 
        default='',type=click.Choice(mysql_instances))
    if mysql_ins:
        _mysql = rundata.datas['mysql'].get(mysql_ins)
        params_cfg.update(mysql_user=_mysql['user'],mysql_pwd=_mysql['ped'],
            mysql_host=_mysql['host'],mysql_port=_mysql['port'],mysql_db=_mysql['dbname'])

    if params_cfg:
        click.echo(click.style("mysql config:  %s".format(params_cfg),fg='green'))
    else:
        yaml_cfg = docker_compose_fmt2

    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    params = dict(
        rundir=rundir,
        instance=instance,
        worker_num=work_num,
        release=release,
    )
    params_cfg.update(params)
    with open("{0}/docker-compose.yaml".format(target_dir),'wb') as dcfile:
        dcfile.write(yaml_cfg(**params_cfg))

    shell.run('cd {0} && docker-compose up -d && docker-compose ps'.format(target_dir))


def docker_op(rundir,instance,op):
    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        click.echo(click.style("instance {0} not exist".format(instance),fg='red'))
    if op in ('logs','start','stop','restart','kill','rm'):
        shell.run('cd {0} && docker-compose {1} radius'.format(target_dir,op))

        if op == 'rm' and click.confirm('Do you want to remove radius data ({0})?'.format(target_dir)):
            shutil.rmtree(target_dir)
    else:
        click.echo(click.style("unsupported operation {0}".format(op),fg='red'))









