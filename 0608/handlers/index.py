#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .basic import BasicHandler, login


class IndexHandler(BasicHandler):

    @login
    def get(self):
        extra_info = self.user_ins.fetch_user_info_by_nickname(self.current_user)
        self.render('index.html', extra_info=extra_info)

