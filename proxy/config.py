#coding:utf-8

mysql_config = {
    'host':'localhost',
    'port':3306,
    'user':'root',
    'passwd':'',
    'db':'proxy',
    'charset':'utf8'
}

redis_config = {
    'host':'localhost',
    'db':2
}


log_name = 'crawler'
log_path = 'crawler.log'
log_formatter = '%(asctime)s %(levelname)-10s: %(message)s'