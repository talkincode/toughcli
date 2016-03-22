#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, click
from toughguy.trshell import shell
from toughguy import __version__
from toughguy import mysqlfunc
from toughguy import docker
from toughguy import toughradius
from toughguy import trbfunc
from toughguy import toughwlan
from toughguy import txportal

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(click.style("toughguy {0}".format(__version__),fg='cyan'))
    ctx.exit()

@click.group()
@click.option('--version', is_flag=True, callback=print_version,expose_value=False, is_eager=True)
def cli():
    pass

@click.command()
@click.option('--docker-install', is_flag=True)
@click.option('--docker', is_flag=True)
def mysql(docker_install):
    if docker_install:
        rundir = click.prompt('Please enter mysql rundir [/home/toughrun]', default='/home/toughrun')
        instance = click.prompt('Please enter mysql instance [mydb]', default='mydb')
        username = click.prompt('Please enter mysql user [mydb]', default='mydb')
        password = click.prompt('Please enter mysql password [mypwd]', default='mypwd')
        root_password = click.prompt('Please enter mysql root password [none]', default='')
        dbname = click.prompt('Please enter mysql database [mydb]', default='mydb')
        max_mem = click.prompt('Please enter mysql max_mem [none]', default='', 
            type=click.Choice(['', '512M','1G','4G']))
        mysqlfunc.docker_install(rundir,instance,username,password,root_password,dbname,max_mem)


cli.add_command(mysql)

if __name__ == '__main__':
    cli()















