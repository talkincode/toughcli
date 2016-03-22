#!/usr/bin/env python
#coding:utf-8

import sys,os
from toughguy.trshell import shell

docker_compose_fmt = '''redis:
    container_name: redis_{instance}
    image: "index.alauda.cn/tutum/redis"
    expose:
        - "6379"
    environment:
        - REDIS_MAXMEMORY=256mb
        - REDIS_PASS=guyredis
    restart: always   
'''