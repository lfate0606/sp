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
        resp = session.get(url, timeout=3)
    except Exception as e:
        logger.error(e)
        if retry > 0:
            time.sleep(random.uniform(0.1, 5))
            return crawl(session,url, retry - 1)
        else:
            raise e
    if resp.status_code == 200:
        return resp.content
    elif retry > 0:
        time.sleep(random.uniform(0.1, 5))
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
    html = etree.HTML(content)
    ele_list = html.xpath(list_xpath)
    element_list = []
    for ele in ele_list:
        element = ele.xpath(text_xpath)
        element_list.append(element)
    return element_list


def save(element_list):
    ip_sql = "insert into ip(ip,port,location,anonymous,create_time,update_time)" \
             " values('{ip}',{port},'{location}','{anonymous}',now(),now()) " \
             "on duplicate key update update_time=now()"
    for ele in element_list:
        db_helper.execute(ip_sql.format(ip=ele[0],port=ele[1],anonymous=ele[2],location=ele[4]))



def run():
    base_urls = [
        {'url':'http://www.kuaidaili.com/free/inha/',
        'total':10,
        'list_xpath':'//*[@id="list"]/table/tbody/tr',
        'text_xpath':'td/text()',
        },
        {'url': 'http://www.kuaidaili.com/free/intr/',
         'total': 10,
         'list_xpath': '//*[@id="list"]/table/tbody/tr',
         'text_xpath': 'td/text()',
         },
        {'url':'http://www.kuaidaili.com/ops/proxylist/',
        'total':10,
        'list_xpath':'//*[@id="freelist"]/table/tbody/tr',
        'text_xpath':'td/text()',
        }
    ]
    session = requests.Session()
    session.headers.update({"Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            "Cache-Control": "max-age=0",
                            "Cookie": "channelid=0; sid=1500791148039455; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1500773376; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1500793506; _ga=GA1.2.1800942703.1500773376; _gid=GA1.2.438274450.1500773376",
                            "Connection": "keep-alive"})
    for base_url in base_urls:
        url = base_url['url']
        total = base_url['total']
        list_xpath = base_url['list_xpath']
        text_xpath = base_url['text_xpath']
        for page in xrange(1,total+1):
            time.sleep(random.uniform(0.1,5))
            try:
                if page == 1:
                    _url = url
                else:
                    _url = "%s%s/" % (url, page)
                content = crawl(session,_url)
                element_list = parse(list_xpath, text_xpath, content)
                save(element_list)
            except Exception as e:
                logger.error("%s-%s" % (url,e))

if __name__ == '__main__':
    run()





