# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/4/14 13:32

import logging.config
import hashlib
from conf import settings

# 用户认证装饰器
def user_status(fn):
    from core import src
    def inner(*args, **kwargs):
        if src.user_info['name']:
            res = fn(*args, **kwargs)
            return res
        else:
            src.login()
    return inner


# 密码加密
def get_md5(pwd):
    # 加字符串进去防止密码被破译
    string = '自是人生长恨水长东'
    # 生成md5仓库
    md5 = hashlib.md5()
    # 加工
    md5.update(string.encode('utf-8'))
    md5.update(pwd.encode('utf-8'))
    return md5.hexdigest()


# 日志处理
def get_logger(name):
    logging.config.dictConfig(settings.LOGGING_DIC)
    # 创建log实例
    logger = logging.getLogger(name)
    return logger
