# coding:utf-8
import logging

import sys

from config import log_name,log_path,log_formatter

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(log_name)
logger.setLevel(logging.INFO)
# 日志保存路径
file_handler = logging.FileHandler(log_path)
# 日志存储格式
formatter = logging.Formatter(log_formatter)
# 屏幕打印
console_handler = logging.StreamHandler(sys.stdout)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.WARN)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

   