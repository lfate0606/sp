#coding:utf-8
import os
import socket
from logger import logger
import requests

def alive(ip):
    """
    验证 ip 是否可访问
    :param ip:
    :return:
    """
    ret = os.system('ping -c 1 -W 1 %s' % ip)
    if ret == 0:
        return True
    else:
        return False

def isopen(ip,port):
    """
    验证端口是否开放
    :param ip:
    :param port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, port))
        open = True
    except Exception as e:
        logger.error("%s-%s-%s" % (ip,port,e))
        open = False
    s.close()
    return open


def isproxy(ip,port,protocol):
    """
    验证端口是否为代理端口
    :param ip:
    :param port:
    :return:
    """
    test_url = 'http://lfate.com/check.html'
    logger.info('proxy:%s://%s:%s' % (protocol,ip,port))
    proxies = {
        'http':'%s://%s:%s' % (protocol,ip,port),
        'https':'%s://%s:%s' % (protocol,ip,port),
    }

    try:
        resp = requests.get(test_url, proxies=proxies,timeout=5)
        if resp.status_code == 200:
            if 'check' in resp.content:
                isproxy = True
            else:
                isproxy = False
        else:
            isproxy = False
    except Exception as e:
        logger.error("%s-%s-%s" % (ip, port, e))
        isproxy = False
    return  isproxy



def protocol(ip,port):
    """
    获取代理类型
    :param ip:
    :param port:
    :return:['http','https','socks4','socks5','all_http','all_socks','all']
    """
    return 'http'




def anonymous(ip,port):
    """
        验证高匿名  代理
        :param ip:
        :param port:
        :return:['高匿名','匿名','透明']
        """
    pass

def method(ip,port):
    """
        验证访问支持
        :param ip:
        :param port:
        :return:['GET','POST','ALL']
    """
    pass

def location(ip):
    """
    获取ip 地址
    :param ip:
    :return:
    """
    pass


