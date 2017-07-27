# encoding: utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB
from config import mysql_config
from MySQLdb.cursors import DictCursor
from logger import logger

# mysql  数据库连接池
pool = PooledDB(MySQLdb, **mysql_config)


def transaction(func,*args,**kwargs):
    """
        数据库处理事务
    """

    def _transaction(sql, _type='dict',*args,**kwargs):
        logger.info(sql)
        db = pool.connection()
        if _type == 'dict':
            cursor = db.cursor(DictCursor)
        else:
            cursor = db.cursor()
        try:
            data = func(cursor, sql, *args,**kwargs)
            db.commit()
            cursor.close
            return data
        except Exception as e:
            logger.info(e)
            db.rollback()
            raise e

    return _transaction


@transaction
def query_one(cursor, sql, _type='dict'):
    cursor.execute(sql)
    return cursor.fetchone()


@transaction
def query_all(cursor, sql, _type='dict'):
    cursor.execute(sql)
    return cursor.fetchall()


@transaction
def execute(cursor, sql):
    return cursor.execute(sql)

@transaction
def executemany(cursor, sql, data):
    return cursor.executemany(sql, data)
