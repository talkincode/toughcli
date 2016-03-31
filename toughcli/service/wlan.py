#!/usr/bin/env python
#coding:utf-8
import os, sys, click
import shutil
import platform
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
    command: pypy /opt/toughwlan/toughctl  --portald
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
        - {rundir}/{instance}:/var/toughwlan
wlan:
    command: pypy /opt/toughwlan/toughctl  --httpd
    image: "index.alauda.cn/toughstruct/toughwlan"
    privileged: true
    expose:
        - "1818"
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
        - {rundir}/{instance}:/var/toughwlan
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
    command: pypy /opt/toughwlan/toughctl --standalone
    image: "index.alauda.cn/toughstruct/toughwlan"
    privileged: true
    ports:
        - "{web_port}:1818"
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
    if dbtype == 'mysql':
        docker_scale(rundir,instance,work_num)


def docker_op(rundir,instance,op):
    target_dir = "{0}/{1}".format(rundir,instance)
    if not os.path.exists(target_dir):
        click.echo(click.style("instance {0} not exist".format(instance),fg='red'))
    if op in DOCKER_OPS:
        os.system('cd {0} && docker-compose {1}'.format(target_dir,op))
        if op == 'rm' and click.confirm('Do you want to remove toughwlan data ({0})?'.format(target_dir)):
            shutil.rmtree(target_dir)
    elif op =='upgrade':
        os.system('cd {0} && docker-compose pull && docker-compose kill && \
            docker-compose rm && docker-compose up -d && docker-compose ps'.format(target_dir))
    else:
        click.echo(click.style("unsupported operation {0}".format(op),fg='red'))

def docker_scale(rundir,instance,num):
    target_dir = "{0}/{1}".format(rundir,instance)
    os.system('cd {0} && docker-compose scale wlan={1}'.format(target_dir,num))
    os.system('cd {0} && docker-compose kill haproxy'.format(target_dir))
    os.system('cd {0} && docker-compose rm haproxy'.format(target_dir))
    os.system('cd {0} && docker-compose up -d haproxy'.format(target_dir))
    



##################################################################################

def install_native_py_models():
    os.system("pip install supervisor")
    os.system("pip install wheel")
    os.system("pip install Mako")
    os.system("pip install Beaker")
    os.system("pip install MarkupSafe")
    os.system("pip install PyYAML")
    os.system("pip install Twisted")
    os.system("pip install treq")
    os.system("pip install tablib")
    os.system("pip install cyclone")
    os.system("pip install six")
    os.system("pip install autobahn")
    os.system("pip install pycrypto")
    os.system("pip install pyOpenSSL>=0.14")
    os.system("pip install service_identity")
    os.system("pip install MySQL-python")
    os.system("pip install SQLAlchemy")
    os.system("pip install pyzmq")
    os.system("pip install txzmq")
    os.system("pip install redis")
    os.system("pip install msgpack-python")
    os.system("pip install psutil")
    os.system("pip install IPy")
    os.system("pip install -U https://github.com/talkincode/toughlib/archive/master.zip --no-deps")
    os.system("pip install -U https://github.com/talkincode/txportal/archive/master.zip --no-deps")

def install_native_release(release):
    if os.path.exists("/opt/toughwlan"):
        native_upgrade(release)
    else:
        os.system("cd /opt && git clone -b release-%s https://github.com/talkincode/toughwlan.git /opt/toughwlan"%release)
    os.system("rm -f /etc/toughwlan.json")
    os.system("rm -f /etc/toughwlan.conf")
    os.system("rm -f /usr/lib/systemd/system/toughwlan.service")
    os.system("ln -s /opt/toughwlan/etc/toughwlan.json /etc/toughwlan.json")
    os.system("ln -s /opt/toughwlan/etc/toughwlan.conf /etc/toughwlan.conf")
    os.system("ln -s /opt/toughwlan/etc/toughwlan.service /usr/lib/systemd/system/toughwlan.service")
    os.system("chmod 754 /usr/lib/systemd/system/toughwlan.service")


def ubuntu_install(release):
    os.system("apt-get install -y  libffi-devel openssl openssl-devel git gcc python-devel python-setuptools")
    os.system("apt-get install -y  mysql-client libmysqlclient-dev libzmq-dev redis-server")
    install_native_py_models()
    if not os.path.exists("/usr/local/bin/supervisord"):
        os.system("ln -s /usr/bin/supervisord /usr/local/bin/supervisord")
        os.system("ln -s /usr/bin/supervisorctl /usr/local/bin/supervisorctl")
    install_native_release(release)
    strs = "install done, please edit /etc/toughwlan.json and start by 'service toughwlan start' "
    click.echo(click.style(strs,fg='green'))

def centos_install(release):
    os.system("yum install -y epel-release" )
    os.system("yum install -y  wget zip python-devel libffi-devel openssl openssl-devel gcc git czmq czmq-devel")
    os.system("yum install -y  mysql-devel MySQL-python redis")
    install_native_py_models()
    if not os.path.exists("/usr/local/bin/supervisord"):
        os.system("ln -s /usr/bin/supervisord /usr/local/bin/supervisord")
        os.system("ln -s /usr/bin/supervisorctl /usr/local/bin/supervisorctl")
    install_native_release(release)
    strs = "install done, please edit /etc/toughwlan.json and start by 'service toughwlan start' "
    click.echo(click.style(strs,fg='green'))

def native_initdb():
    os.system("python /opt/toughwlan/toughctl --initdb -f -c /etc/toughwlan.json")

def native_upgrade(release):
    os.system("cd /opt/toughwlan && git fetch origin release-%s && git reset --hard FETCH_HEAD && git clean -df"%release)

def native_install(release):
    if not os.path.exists("/var/toughwlan/data"):
        os.makedirs("/var/toughwlan/data")
    _linux = platform.dist()[0]
    if _linux  == 'centos':
        centos_install(release)
    elif _linux  == 'ubuntu':
        ubuntu_install(release)
    else:
        click.echo(click.style("setup not support",fg='green'))



