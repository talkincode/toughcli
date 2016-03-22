#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, click
from toughcli.toughshell import shell
from toughcli import __version__
from toughcli.service import mysql as mysql_serv
from toughcli.service import docker as docker_serv
from toughcli.service import redis as redis_serv
from toughcli.service import radius as radius_serv
from toughcli.rundata import rundata

RUNDIR = '/home/toughrun'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(click.style("toughcli {0}".format(__version__),fg='cyan'))
    ctx.exit()

@click.group()
@click.option('--version', is_flag=True, callback=print_version,expose_value=False, is_eager=True)
def cli():
    pass

@click.command()
@click.option('--pypi', is_flag=True,help="from pypi")
@click.option('--github', is_flag=True,help="from github")
def upgrade(pypi,github):
    if github:
        shell.run("sudo pip install --upgrade https://github.com/talkincode/toughcli/archive/master.zip")
    elif pypi:
        shell.run("sudo pip install --upgrade toughcli")


@click.command()
@click.option('--install', is_flag=True,help="install docker & docker-compose")
@click.option('--from-daocloud', is_flag=True)
def docker(install,from_daocloud):
    if install and from_daocloud:
        docker_serv.daocloud_install()
    elif from_daocloud:
        docker_serv.auto_install()


@click.command()
@click.option('--docker-install', is_flag=True,help="install docker-mysql instance")
@click.option('--docker-op', default='',
    type=click.Choice(['','logs','start','stop','restart','kill','rm','backup']),
    help="docker instance operate")
@click.option('--rundir', default=RUNDIR,help="default:%s"%RUNDIR)
@click.option('--instance', default='mydb',help="mysql instance, default:mydb")
def mysql(docker_install,docker_op,rundir,instance):
    if docker_install:
        mysql_serv.docker_install(rundir,instance)
    elif docker_op:
        mysql_serv.docker_op(rundir,instance,docker_op)


@click.command()
@click.option('--docker-install', is_flag=True,help="install docker-redis instance")
@click.option('--docker-op', default='',
    type=click.Choice(['','logs','start','stop','restart','kill','rm']),
    help="docker instance operate")
@click.option('--rundir', default=RUNDIR,help="default:%s"%RUNDIR)
@click.option('--instance', default='myredis',help="redis instance, default:myredis")
def redis(docker_install,docker_op,rundir,instance):
    if docker_install:
        redis_serv.docker_install(rundir,instance)
    elif docker_op:
        redis_serv.docker_op(rundir,instance,docker_op)



@click.command()
@click.option('--docker-install', is_flag=True)
@click.option('--docker-op', default='',
    type=click.Choice(['','logs','start','stop','restart','kill','rm','sh',"ps"]))
@click.option('--rundir', default=RUNDIR, help="default:%s"%RUNDIR)
@click.option('--instance', default='myradius')
@click.option('--worker-num', default=2,type=click.INT)
@click.option('--release', default='stable',type=click.Choice(['dev','stable']),)
def radius(docker_install,docker_op,rundir,instance,worker_num,release):
    if docker_install:
        radius_serv.docker_install(rundir,instance,worker_num,release)
    elif docker_op:
        radius_serv.docker_op(rundir,instance,docker_op)


cli.add_command(upgrade)
cli.add_command(docker)
cli.add_command(mysql)
cli.add_command(redis)
cli.add_command(radius)

if __name__ == '__main__':
    cli()















