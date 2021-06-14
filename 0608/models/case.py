# !/usr/bin/env python
# -*- coding: utf-8 -*-

from models.basic import Basic


class Case(Basic):
    def __init__(self):
        super(Case, self).__init__()
        self.count = 30

    def fetch_case1_list(self, page):
        sql = "select * from pcase order " \
              "by id desc limit %s, %s" % ((page - 1) * self.count, self.count)
        return self.g_mysql.query(sql)

    def count_case1_num(self):
        sql = "select count(id) from pcase"
        ret = self.g_mysql.query(sql)
        return ret

    def fetch_case2_list(self, page):
        sql = "select * from ccase order " \
              "by id desc limit %s, %s" % ((page - 1) * self.count, self.count)
        return self.g_mysql.query(sql)

    def count_case2_num(self):
        sql = "select count(id) from ccase"
        ret = self.g_mysql.query(sql)
        return ret

    def fetch_case3_list(self, page):
        # sql = "select top %s * from ncase where id not in (select top %s id from ncase) order by id" % (
        # self.count, ((int(page) - 1) * self.count))
        sql = "select * from ncase where id not in (select m.id from (select id from ncase limit 0,%s) as m) order by id limit 0, %s" % (
            ((int(page) - 1) * self.count), self.count)
        print(sql)
        return self.g_mysql.query(sql)

    def count_case3_num(self):
        sql = "select count(*) from ncase"
        ret = self.g_mysql.query(sql)
        return ret[0]["count(*)"]

    def search_case3_info_by_p(self, p):
        sql = "select * from ncase where province" \
              " like '%%%%%s%%%%' " % p
        print(sql)
        return self.g_mysql.query(sql)

    def insert_case3_data(self, data_list):
        sql = "insert into ncase (province, year, date, confirm, dead, heal, newconfirm, newheal, newdead, desp) " \
              "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % data_list
        # print(sql)
        self.g_mysql.operate(sql)

    def del_case3_data_by_id(self, id):
        sql = "delete from ncase where id = '%s'" % id
        self.g_mysql.operate(sql)

    def search_case3_info_by_id(self, id):
        sql = "select * from ncase where id = '%s'" % id
        # print(sql)
        return self.g_mysql.query(sql)

    def update_case3_by_id(self, id, data):
        data = tuple(list(data) + [id])
        sql = "update ncase set province='%s', confirm= '%s', dead='%s', heal='%s', newconfirm='%s', newheal='%s', newdead='%s', desp='%s' where id='%s'" % data
        self.g_mysql.operate(sql)
