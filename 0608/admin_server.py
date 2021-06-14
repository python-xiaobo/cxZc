#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options
from logging.handlers import RotatingFileHandler

from handlers.user import SignHandler
from handlers.index import IndexHandler
from handlers.login import LoginHandler, LogoutHandler
from handlers.case import Case1Handler,Case1CreateHandler, SearchCase1Handler, DelCase1Handler, EditCase1Handler


formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()
if options.log_file_prefix:
    logger.handlers = []
    channel = logging.handlers.TimedRotatingFileHandler(
        filename=options.log_file_prefix,
        when='midnight',
        backupCount=options.log_file_num_backups
    )
    channel.setFormatter(formatter)
    logger.addHandler(channel)


define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/index", IndexHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/sign", SignHandler),
            (r"/case1", Case1Handler),
            (r"/case/append", Case1CreateHandler),
            (r"/search", SearchCase1Handler),
            (r"/case/del", DelCase1Handler),
            (r"/case/change", EditCase1Handler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "statics"),
            ui_modules=dict(
            ),
            cookie_secret='939d3d573f06c5fed9bf7',
            debug=True,
            gzip=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

