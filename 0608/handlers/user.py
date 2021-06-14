#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .basic import BasicHandler


class SignHandler(BasicHandler):
    def get(self):
        self.render('sign.html')

    def post(self):
        username = self.get_argument("username", "")
        email = self.get_argument("mail", '')
        tel = self.get_argument('telnum', '')
        pwd1 = self.get_argument("password", None)
        pwd2 = self.get_argument("password1", None)

        if not username:
            return self.write("用户名不能为空!!!")
        if pwd1 != pwd2:
            return self.write("两次输入的密码不相同!!!")

        self.user_ins.new_user(username, pwd1, tel, email)
        self.redirect("/login")
