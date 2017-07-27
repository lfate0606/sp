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

def create(alive=False):
    ip_sql = "select ip from ip group by ip having count(1) < 20"
    port_sql = "select port,count(1) from ip group by port order by count(1) desc limit 20"
    ip_list =  db_helper.query_all(ip_sql)
    port_list = db_helper.query_all(port_sql)
    for ip in ip_list:
        data = list()
        for port in port_list:
            data.append((ip['ip'],port['port']))
        sql = "insert into ip(ip, port, anonymous,alive) values(%s,%s,'高匿名',true) on duplicate key update update_time=now() "
        db_helper.executemany(sql,data=data)

if __name__ == '__main__':
    create(alive=True)
