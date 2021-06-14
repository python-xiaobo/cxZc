#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import re
# 数据库mysql的配置信息，例如主机ip、登录名、登录密码以及创建的数据库名称
mysqlInfo = {
    "host": 'localhost',    # 本地数据库的ip或者localhost
    "user": 'root',     # mysql用户名
    "passwd": '',   # 登录密码
    "db": 'cov',     # 现有项目要将爬取数据保存到的数据库名
    "port": 3306,  # mysql默认3306端口，修改请配置
}



class OPMysql(object):

    __using4conn = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.conn = OPMysql.getmysqlconn()
        self.cur = self.conn.cursor()

    @staticmethod
    def getmysqlconn():
        # 链接数据库，通过配置获取信息
        if OPMysql.__using4conn is None:
            __using4conn = pymysql.connect(mysqlInfo["host"], mysqlInfo["user"], mysqlInfo["passwd"], mysqlInfo["db"])
        return __using4conn

    def query(self, sql, *args):
        # 根据sql语句查询数据库表中的数据，将查取的数据返回
        # 当数据取完后即刻关闭连接，防止资源占用
        self.cur.execute(sql, args)
        res = self.cur.fetchall()
        self.dispose()
        return res

    def dispose(self):
        # 释放资源，游标链接关闭
        self.conn.close()
        self.cur.close()

    def table_exists(self, table_name):
        # 这个函数用来判断表是否存在
        sql = "show tables;"
        self.cur.execute(sql)
        tables = [self.cur.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name.lower() in table_list:
            return True
        else:
            return False

    def get_conn(self):
        # 建立连接
        conn = self.conn
        # c创建游标
        cursor = self.cur
        return conn, cursor
