#coding:utf-8
import requests
from logger import logger
from lxml import etree
import time
import db_helper
import random
import sys
from tasks import do_open,do_alive,do_proxy
reload(sys)
sys.setdefaultencoding('utf-8')

def get_ip_list():
    sql = "select * from ip order by update_time desc"
    return db_helper.query_all(sql)

def check_open(open=False):
    sql = "select ip, port from ip where alive is true and open is %s order by update_time desc" % open
    proxies_list =  db_helper.query_all(sql)
    for proxies in proxies_list:
        do_open.delay(proxies)

def check_proxy(proxy=False):
    sql = "select ip,port,protocol from ip where open is true and proxy is %s order by update_time desc" % proxy
    proxies_list =  db_helper.query_all(sql)
    for proxies in proxies_list:
        do_proxy.delay(proxies)

def check_alive(alive=False):
    sql = "select distinct ip as ip from ip where alive is %s  and update_time=create_time" % alive
    proxies_list =  db_helper.query_all(sql)
    for proxies in proxies_list:
        do_alive.delay(proxies)


if __name__ == '__main__':
    check_value = sys.argv[1]
    method_dict = {
        "alive":check_alive,
        "open":check_open,
        "proxy":check_proxy,
    }
    if check_value in method_dict.keys():
        method_dict[check_value](sys.argv[2])

