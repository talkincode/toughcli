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
    net: "host"
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
    net: "host"
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
    params_cfg = {}
    dbtype = click.prompt('database type [sqlite,mysql]', default='sqlite', type=click.Choice(['sqlite','mysql']))
    if dbtype == 'sqlite':
        yaml_cfg = docker_compose_fmt2
    else:
        params_cfg.update(
            mysql_user = click.prompt('Please enter mysql user [mydb]', default='mydb'),
            mysql_pwd = click.prompt('Please enter mysql password [mypwd]', default='mypwd'),
            mysql_host = click.prompt('Please enter mysql host [localhost]', default='localhost'),
            mysql_db = click.prompt('Please enter mysql database [mydb]', default='mydb'),
            mysql_port = click.prompt('Please enter mysql port [3306]', default='3306'),
        )

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

    click.echo(click.style("\nRadius config:\n",fg='cyan'))
    for k,v in params_cfg.iteritems():
        click.echo(click.style("{0}: {1}".format(k,v),fg='green'))

    click.echo(click.style("\nRadius docker-compose.yml:\n",fg='cyan'))
    with open("{0}/docker-compose.yml".format(target_dir),'wb') as dcfile:
        yml_content = yaml_cfg(**params_cfg)
        dcfile.write(yml_content)
        click.echo(click.style(yml_content,fg='green'))

    shell.run('cd {0} && docker-compose up -d'.format(target_dir))
    shell.run('cd {0} && docker-compose ps'.format(target_dir))


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









