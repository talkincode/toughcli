#!/usr/bin/env python
#coding:utf-8
import os, sys, click
import shutil
from toughcli.settings import *

docker_compose_fmt = '''redis:
    image: "index.alauda.cn/tutum/redis"
    expose:
        - "6379"
    environment:
        - REDIS_MAXMEMORY=512mb
        - REDIS_PASS=wlanredis
    restart: always 
wlanpd:
    command: /usr/local/bin/toughrun portald
    image: "index.alauda.cn/toughstruct/toughwlan"
    ports:
        - "{portal_listen_port}:50100/udp"
    links:
        - redis:redis
    environment:
        - REDIS_URL=redis
        - REDIS_PORT=6379
        - REDIS_PWD=wlanredis
        - DB_TYPE=mysql
        - DB_URL=mysql://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8
    restart: always
    volumes:
        - /home/toughrun/{instance}:/var/toughwlan
wlan:
    command: /usr/local/bin/toughrun httpd
    image: "index.alauda.cn/toughstruct/toughwlan"
    privileged: true
    expose:
        - "1810"
    links:
        - redis:redis
    environment:
        - REDIS_URL=redis
        - REDIS_PORT=6379
        - REDIS_PWD=wlanredis
        - EXCLUDE_PORTS=50100
        - DB_TYPE=mysql
        - DB_URL=mysql://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8
    restart: always
    ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000    
    volumes:
        - /home/toughrun/{instance}:/var/toughwlan
haproxy:
    image: "index.alauda.cn/tutum/haproxy"
    privileged: true
    ports:
        - "{web_port}:80"
    links:
        - wlan:wlan
    restart: always
    environment:
        - MAXCONN=40000
    ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000    
'''.format


docker_compose_fmt2 = '''redis:
    image: "index.alauda.cn/tutum/redis"
    expose:
        - "6379"
    environment:
        - REDIS_MAXMEMORY=256mb
        - REDIS_PASS=wlanredis
    restart: always         
wlan:
    container_name: wlan_{instance}
    command: /usr/local/bin/toughrun standalone
    image: "index.alauda.cn/toughstruct/toughwlan"
    privileged: true
    ports:
        - "{web_port}:1810"
        - "{portal_listen_port}:50100"
    links:
        - redis:redis
    environment:
        - REDIS_URL=redis
        - REDIS_PORT=6379
        - REDIS_PWD=wlanredis
    restart: always  
    volumes:
        - {rundir}/{instance}:/var/toughwlan
'''.format

def docker_install(rundir,instance,work_num):
    yaml_cfg = docker_compose_fmt
    params_cfg = dict(
        rundir=rundir,
        instance=instance,
        portal_listen_port = click.prompt('Please enter portal listen port', default='50100'),
        web_port = click.prompt('Please enter web port', default='1818')
    )
    dbtype = click.prompt('database type [sqlite,mysql]', default='sqlite', type=click.Choice(['sqlite','mysql']))
    if dbtype == 'sqlite':
        yaml_cfg = docker_compose_fmt2
    else:
        params_cfg.update(
            mysql_port = click.prompt('Please enter mysql port', default='3306'),
            mysql_host = click.prompt('Please enter mysql host', default='localhost'),
            mysql_user = click.prompt('Please enter mysql user', default='myuser'),
            mysql_pwd = click.prompt('Please enter mysql password', default='mypwd'),
            mysql_db = click.prompt('Please enter mysql database', default='mydb'),
        )

    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    click.echo(click.style("\nToughwlan config:\n",fg='cyan'))
    for k,v in params_cfg.iteritems():
        click.echo(click.style("{0}: {1}".format(k,v),fg='green'))

    click.echo(click.style("\nToughwlan docker-compose.yml:\n",fg='cyan'))
    with open("{0}/docker-compose.yml".format(target_dir),'wb') as dcfile:
        yml_content = yaml_cfg(**params_cfg)
        dcfile.write(yml_content)
        click.echo(click.style(yml_content,fg='green'))

    os.system('cd {0} && docker-compose up -d'.format(target_dir))
    os.system('cd {0} && docker-compose ps'.format(target_dir))


def docker_op(rundir,instance,op):
    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        click.echo(click.style("instance {0} not exist".format(instance),fg='red'))
    if op in DOCKER_OPS:
        os.system('cd {0} && docker-compose {1}'.format(target_dir,op))
        if op == 'rm' and click.confirm('Do you want to remove toughwlan data ({0})?'.format(target_dir)):
            shutil.rmtree(target_dir)
    else:
        click.echo(click.style("unsupported operation {0}".format(op),fg='red'))

def docker_scale(rundir,instance,num):
    target_dir = "{0}/{1}".format(rundir,instance)
    os.system('cd {0} && docker-compose scale wlan={0}'.format(target_dir,num))
    os.system('cd {0} && docker-compose kill down'.format(target_dir))
    os.system('cd {0} && docker-compose up -d haproxy'.format(target_dir))
    

