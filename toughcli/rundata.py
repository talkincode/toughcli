#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import os
import click

class RunData(object):

    def __init__(self):
        self.rundir=os.environ.get("HOME",'~/')
        self.datas = {"mysql":{},'redis':{}}
        self.load()

    def add_mysql(self,instance,host,port,user,pwd,dbname):
        if not all([instance,host,port,user,pwd,dbname]):
            return
        self.datas['mysql'][instance] = dict(host=host,port=port,user=user,pwd=pwd,dbname=dbname)

    def add_redis(self,instance,host,port,pwd,mem='256m',dbid=0):
        if not all([instance,host,port,pwd]):
            return
        self.datas['redis'][instance] = dict(host=host,port=port,pwd=pwd,mem=mem,dbid=dbid)

    def list_mysqls():
        for instance, _mysql in self.datas['mysql'].items():
            click.echo(click.style("instance:%s"%instance),fg='cyan')
            click.echo(click.style(repr(_mysql)),fg='cyan')

    def list_redis():
        for instance, _redis in self.datas['redis'].items():
            click.echo(click.style("instance:%s"%instance),fg='cyan')
            click.echo(click.style(repr(_redis)),fg='cyan')

    def save(self):
        with open('{0}/toughcli.pickle'.format(self.rundir), 'wb') as f:
            pickle.dump(self.datas, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        if not os.path.exists('{0}/toughcli.pickle'.format(self.rundir)):
            return
        with open('{0}/toughcli.pickle'.format(self.rundir), 'rb') as f:
            try:
                self.datas = pickle.load(f)
            except:
                click.echo(click.style("load data error"),fg='red')

rundata = RunData()
