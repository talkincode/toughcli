#!/usr/bin/env python
#coding:utf-8

import sys,os
import shutil
import click
from toughcli.toughshell import shell

docker_compose_fmt = '''redis:
    container_name: redis_{instance}
    image: "index.alauda.cn/tutum/redis"
    net: "host"
    environment:
        - REDIS_MAXMEMORY={max_mem}
        - REDIS_PASS={redis_pass}
    restart: always
    ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000    
'''.format

def docker_install(rundir,instance):
    redis_pass = click.prompt('Please enter redis password [myredis]', default='myredis')
    max_mem = click.prompt('Please enter redis max_mem [256m]', default='256m', 
        type=click.Choice(['256m', '512m','1024m','2048m','4096m','8192m']))
    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    params = dict(
        rundir=rundir,
        instance=instance,
        redis_pass=redis_pass,
        max_mem=max_mem
    )
    with open("{0}/docker-compose.yaml".format(target_dir),'wb') as dcfile:
        dcfile.write(docker_compose_fmt(**params))

    shell.run('cd {0} && docker-compose up -d && docker-compose ps'.format(target_dir))


def docker_op(rundir,instance,op):
    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        click.echo(click.style("instance {0} not exist".format(instance),fg='red'))
    if op in ('logs','start','stop','restart','kill','rm'):
        shell.run('cd {0} && docker-compose {1} redis'.format(target_dir,op))
    else:
        click.echo(click.style("unsupported operation {0}".format(op),fg='red'))












