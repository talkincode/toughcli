#!/usr/bin/env python
# -*- coding: utf-8 -*-


RUNDIR = '/home/toughrun'
DOCKER_OPS = ['','ps','config','pull','logs','start','stop','restart','kill','rm','down','pause','unpause']
MYSQL_OPS = DOCKER_OPS + ['status','backup','showdbs']
REDIS_OPS = DOCKER_OPS + ['status']
RADIUS_OPS = DOCKER_OPS + ['status']
WLAN_OPS = DOCKER_OPS + ['status']