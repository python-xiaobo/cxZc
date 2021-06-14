#!/usr/bin/env python
# -*- coding: utf-8 -*-


from models.basic import Basic


class Users(Basic):
    def __init__(self):
        super(Users, self).__init__()

    def checkout_user_login(self, nickname, pwd):
        sql = "select id, password from users where nickname='%s'" % nickname
        ret = self.g_mysql.get(sql)
        if not ret:
            return False
        if pwd != ret['password']:
            return False
        return True

    def fetch_user_info_by_nickname(self, nickname):
        sql = "select id, nickname, password, email from users " \
              "where nickname='%s'" % nickname
        return self.g_mysql.get(sql)

    def new_user(self, nickname, pwd, tel, email):
        sql = "insert into users (nickname, password, tel, email) values ('%s', %s, %s, '%s')" % (nickname, pwd, tel, email)
        print(sql)
        self.g_mysql.operate(sql)

