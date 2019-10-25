# coding:utf-8

import json

from tornado.web import RequestHandler, StaticFileHandler


class BaseHandler(RequestHandler):
    """自定义基类"""
    #@property
    #def db(self):
        #return self.application.db


    def prepare(self):
        """预解析json数据"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}




class StaticFileBaseHandler(StaticFileHandler):
    """自定义静态文件处理类, 在用户获取html页面的时候设置_xsrf的cookie"""
    def __init__(self, *args, **kwargs):
        super(StaticFileBaseHandler, self).__init__(*args, **kwargs)
        #self.xsrf_token























