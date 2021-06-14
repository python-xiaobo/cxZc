#!/usr/bin/env python
# -*-coding:utf-8-*-

# import srvconf
# import torndb
#
# # mysql 数据库全局链接
# global_mysql = torndb.Connection(srvconf.MYSQL_HOST, srvconf.MYSQL_DB, srvconf.MYSQL_USER, srvconf.MYSQL_PASSWORD)

import srvconf
import pymysql


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
            __using4conn = pymysql.connect(host=srvconf.MYSQL_HOST, user=srvconf.MYSQL_USER, password=srvconf.MYSQL_PASSWORD,
                                           database=srvconf.MYSQL_DB, port=srvconf.MYSQL_POOT, charset='utf8')
        return __using4conn

    def operate(self, sql, *args):
        self.cur.execute(sql, args)
        self.conn.commit()
        # self.dispose()

    def query(self, sql, *args):
        select_pos, from_pos = sql.find("select"), sql.find("from")
        key4list = sql[select_pos + 7:from_pos - 1].replace(" ", '').split(",")
        if key4list == ["*"] or key4list == ["top30*"]:
            key4list = ["id", "province", "year", "date", "confirm", "dead", "heal", "newconfirm", "newheal", "newdead", "desp"]
        self.cur.execute(sql, args)
        res_ = self.cur.fetchall()
        res = []
        for i in range(len(res_)):
            swap = {}
            for j in range(len(key4list)):
                swap[key4list[j]] = res_[i][j]
            res.append(swap)
        # self.dispose()
        return res

    def get(self, sql, *args):
        res = {}
        select_pos, from_pos = sql.find("select"), sql.find("from")
        key4list = sql[select_pos+7:from_pos-1].replace(" ", '').split(",")
        self.cur.execute(sql, args)
        res_ = self.cur.fetchall()
        if res_:
            for i in range(len(key4list)):
                res[key4list[i]] = res_[0][i]
        else:
            res = None
        return res

    def dispose(self):
        # 释放资源，游标链接关闭
        self.conn.close()
        self.cur.close()

    def get_conn(self):
        # 建立连接
        conn = self.conn
        # c创建游标
        cursor = self.cur
        return conn, cursor


global_mysql = OPMysql()
