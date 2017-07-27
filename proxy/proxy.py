# coding:utf-8
"""
    从数据库中获取可用的代理IP
"""
import requests
from logger import logger
from lxml import etree
import time
import db_helper
import random
import sys
from utils import isproxy
reload(sys)
sys.setdefaultencoding('utf-8')

proxies_list = None


def init_proxies_list():
    global proxies_list

    if proxies_list is None or len(proxies_list) == 0:
        sql = "select id,ip, port, protocol,100 as count from ip where proxy is true and open is true  and anonymous='高匿名' order by update_time desc;"
        proxies_list = list(db_helper.query_all(sql))
    else:
        proxies_list = sorted(proxies_list,key=lambda x:x['count'],reverse=True)
        if proxies_list[0]['count'] == 0:
            proxies_list = None
            init_proxies_list()

def update(proxies):
    sql = "update ip set proxy=false where id={id}".format(**proxies)
    db_helper.execute(sql)


def get_proxies():
    while True:
        init_proxies_list()
        if proxies_list is None or len(proxies_list) == 0:
            raise Exception('proxy error')
        proxies = proxies_list[0]
        if isproxy(proxies['ip'],proxies['port'],proxies['protocol'].lower()) is False:
            update(proxies)
            proxies_list.remove(proxies)
        else:
            proxies['count'] -= 1
            return proxies


if __name__ == '__main__':
    print  get_proxies()

















