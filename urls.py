# coding:utf-8

import os

from handlers.BaseHandler import StaticFileBaseHandler as StaticFileHandler
from handlers import Handler

urls = [
    (r"/api/tj", Handler.TjHandler),
    (r"/api/ss/(?P<tiaojian>.+)/(?P<page>\d*)", Handler.SsHandler),
    (r"/api/list/(?P<tiaojian>.+)/(?P<page>\d*)", Handler.ListHandler),
    (r"/(.*)", StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="1.html"))
]
