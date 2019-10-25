# coding:utf-8

import os

# Application配置参数
settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    cookie_secret="FhLXI+BRRomtuaG47hoXEg3JCdi0BUi8vrpWmoxaoyI=",
    #xsrf_cookies=True,
    debug=True
)


# 数据库配置参数
mysql_options = dict(
    host="127.0.0.1",
    database="nbufiles",
    user="root",
    password="123456"
)


# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"

