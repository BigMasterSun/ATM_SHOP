# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/4/14 13:31
from lib import common
from db import db_hander
logger = common.get_logger('shop')


# 查看购物车接口
def check_shop_interface(name):
    user_dic = db_hander.select(name)
    if user_dic:
        return True,user_dic['shopping_car']
    else:
        return False, '购物车已清空'


# 添加购物车接口
def add_shopping_car_interface(name,shopping_car):
    user_dic = db_hander.select(name)
    user_dic['shopping_car'] = shopping_car
    logger.info('用户[%s]添加商品至购物车成功')
    db_hander.save(user_dic)
    return True, '添加购物车成功'