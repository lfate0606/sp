# coding:utf-8
from celery import Celery
from  redis import StrictRedis
import socket
import sys
import db_helper
from utils import *
broker = 'redis://127.0.0.1:6379/5'
backend = 'redis://127.0.0.1:6379/6'
app = Celery('tasks', broker=broker,backend=backend)

redis = StrictRedis(db=15)



@app.task
def do_alive(proxies):
    if alive(proxies['ip']) is False:
        sql = "update ip set alive=false, open=false," \
              " proxy=false ,update_time=now() where ip='%s';" % proxies['ip']
    else:
        sql = "update ip set alive=true,update_time=now() where ip = '%s' " % proxies['ip']
    db_helper.execute(sql)

@app.task
def do_open(proxies):
    if isopen(proxies['ip'],proxies['port']) is False:
        sql = "update ip set open=false," \
              " proxy=false, update_time=now() "" \
              ""where ip = '%s' and port=%s " % (proxies['ip'],proxies['port'])
    else:
        sql = "update ip set open=true,update_time=now() where ip = '%s' "" \
        "" and port=%s " % (proxies['ip'],proxies['port'])
    db_helper.execute(sql)

@app.task
def do_proxy(proxies):
    if isproxy(proxies['ip'],proxies['port'],proxies['protocol']) is False:
        sql = "update ip set proxy=false," \
              " update_time=now() "" \
              ""where ip = '%s' and port=%s " % (proxies['ip'],proxies['port'])
    else:
        sql = "update ip set proxy=true,update_time=now() where ip = '%s' "" \
        "" and port=%s " % (proxies['ip'],proxies['port'])
    db_helper.execute(sql)







