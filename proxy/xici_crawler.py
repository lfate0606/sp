# coding:utf-8
"""
    从快代理获取历史代理IP地址
"""
import requests
from logger import logger
from lxml import etree
import time
import db_helper
import random
from proxy import get_proxies
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def crawl(session, url, retry=3):
    """
    获取内容 默认失败重试三次
    :param session:
    :param url:
    :param retry:
    :return: 网页内容
    """
    logger.info("url:%s---retry:%s" % (url,retry))
    try:
        proxies = get_proxies()
        resp = session.get(url, timeout=3,proxies={'http':'{protocol}://{ip}:{port}'.format(**proxies)})
    except Exception as e:
        logger.error(e)
        if retry > 0:
            # time.sleep(random.uniform(0.1, 10))
            return crawl(session,url, retry - 1)
        else:
            raise e
    if resp.status_code == 200:
        return resp.content
    elif retry > 0:
        # time.sleep(random.uniform(0.1, 10))
        return crawl(session, url, retry - 1)
    else:
        raise Exception('获取数据失败')


def parse(list_xpath, text_xpath, content):
    """
    解析内容
    :param xpath_list:
    :param content:
    :return:
    """
    print content
    html = etree.HTML(content)
    ele_list = html.xpath(list_xpath)
    element_list = []
    for ele in ele_list:
        element = ele.xpath(text_xpath)
        element_list.append(element)
    return element_list


def save(element_list):
    ip_sql = "insert into ip(ip,port,location,anonymous,protocol,create_time,update_time)" \
             " values('{ip}',{port},'{location}','{anonymous}','{protocol}',now(),now()) " \
             "on duplicate key update update_time=now(),anonymous='{anonymous}',protocol='{protocol}'"
    for ele in element_list[1:]:
        if ele[5] =='高匿' or ele[5] ==u'高匿':
            ele[5] = u'高匿名'
        else:
            continue
        db_helper.execute(ip_sql.format(ip=ele[0].strip('\n \t'),port=ele[1].strip('\n \t'),anonymous=ele[5].strip('\n \t'),location=ele[3].strip('\n \t'),protocol=ele[6].strip('\n \t')))



def run():
    base_urls = [
        {'url':'http://www.xicidaili.com/nn/',
        'total':10,
        'list_xpath':'//*[@id="ip_list"]/tr',
        'text_xpath':'td/text()|td/a/text()',
        },
        {'url': 'http://www.xicidaili.com/nt/',
         'total': 10,
         'list_xpath': '//*[@id="ip_list"]/tr',
         'text_xpath': 'td/text()|td/a/text()',
         },
        {'url':'http://www.xicidaili.com/wn/',
        'total':10,
        'list_xpath':'//*[@id="ip_list"]/tr',
        'text_xpath':'td/text()|td/a/text()',
        }
        ,
        {'url': 'http://www.xicidaili.com/wt/',
         'total': 10,
         'list_xpath': '//*[@id="ip_list"]/tr',
         'text_xpath': 'td/text()|td/a/text()',
         }
    ]
    session = requests.Session()
    session.headers.update({"Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            "Cache-Control": "max-age=0",
                            "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWEyMzA5NjUwNDY5ZmNjNzEyMzYyOGJkMGYyYWI4ZjIxBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUVCRVB3cFJ2ZnIyTWNQNElSekRFcFdwNTZVTXYrM2ViNnhZbkI4NXZwc3c9BjsARg%3D%3D--600ed2905773cde5c641d42baa06bd99cde15446; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1500975206; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1500975698",
                            "Connection": "keep-alive"})
    for base_url in base_urls:
        url = base_url['url']
        total = base_url['total']
        list_xpath = base_url['list_xpath']
        text_xpath = base_url['text_xpath']
        for page in xrange(1,total+1):
            # time.sleep(random.uniform(0.1,10))
            page = total + 1 - page
            try:
                if page == 1:
                    _url = url
                else:
                    _url = "%s%s" % (url, page)
                content = crawl(session,_url)
                element_list = parse(list_xpath, text_xpath, content)
                save(element_list)
            except Exception as e:
                logger.error("%s-%s" % (url,e))

if __name__ == '__main__':
    run()





