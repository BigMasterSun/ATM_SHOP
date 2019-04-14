# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/4/14 13:31
from db import db_hander
from lib import common
logger = common.get_logger('user')


# 用户注销接口
def logout_interface():
    from core import src
    src.user_info['name'] = None
    return '注销成功'


# 查询用户是否存在接口
def check_user_interface(name):
    user_dic = db_hander.select(name)
    if user_dic:
        logger.warning('用户[%s]已存在，注册失败'%name)
        return False
    else:
        return True


# 注册接口
def register_interface(name, pwd, balance=15000):
    # 密码加密存储
    md5_pwd = common.get_md5(pwd)
    user_dic = {
        'name': name,
        'pwd': md5_pwd,
        'balance': balance,
        'flow': [],
        'shopping_car': {}
    }
    db_hander.save(user_dic)
    logger.info("用户%s注册成功"%name)
    return True,"用户[%s]注册成功"%name


# 登录接口
def login_interface(name, pwd):
    user_dic = db_hander.select(name)
    if not user_dic:
        return False,'用户不存在'
    md5_pwd = common.get_md5(pwd)
    if md5_pwd == user_dic['pwd']:
        logger.info('用户[%s]登录成功'%name)
        return True,'登录成功'
    else:
        return False,'密码错误'
