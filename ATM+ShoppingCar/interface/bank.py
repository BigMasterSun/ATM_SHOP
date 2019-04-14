# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/4/14 13:31
from db import db_hander
from lib import common
logger = common.get_logger('bank')


# 查看余额接口
def check_balance_interface(name):
    user_dic = db_hander.select(name)
    logger.info('用户[%s]进行了余额查询操作' % name)
    return user_dic['balance']


# 提现接口
def withdraw_interface(name, money):
    user_dic = db_hander.select(name)
    money2 = money * 1.05
    money3 = money * 0.05
    if user_dic['balance'] >= money2:
        user_dic['balance'] -= money2
        info = '用户[%s]提现[%s]￥,手续费：%s￥'%(name,money,money3)
        logger.info(info)
        user_dic['flow'].append(info)
        db_hander.save(user_dic)
        return True,info
    else:
        return False,'余额不足'


# 转账接口
def transfer_interface(from_user, to_user, money):
    from_user_dic = db_hander.select(from_user)
    to_user_dic = db_hander.select(to_user)
    if not to_user_dic:
        return False,'对方账户不存在'
    if from_user_dic['balance'] >= money:
        from_user_dic['balance'] -= money
        to_user_dic['balance'] += money
        from_user_dic['flow'].append('给用户[%s]转账[%s￥]成功'%(to_user, money))
        to_user_dic['flow'].append('收到用户[%s]转账[%s￥]'%(from_user,money))
        logger.info('用户[%s]给用户[%s]转账[%s￥]成功'%(from_user, to_user, money))
        db_hander.save(from_user_dic)
        db_hander.save(to_user_dic)
        return True,'转账成功！'
    else:
        logger.warning('用户[%s]给用户[%s]转账[%s￥]失败'%(from_user, to_user, money))
        return False,'余额不足，转账失败'


# 还款接口
def repay_interface(name, money):
    user_dic = db_hander.select(name)
    user_dic['balance'] += money
    user_dic['flow'].append('还款[%s￥]成功！' % money)
    logger.info('用户[%s]还款[%s￥]成功！' % (name, money))
    db_hander.save(user_dic)
    return '还款成功'


# 查看流水接口
def check_flow_interface(name):
    user_dic = db_hander.select(name)
    return user_dic['flow']


# 支付接口
def pay(name, money):
    user_dic = db_hander.select(name)
    if user_dic['balance'] >= money:
        user_dic['balance'] -= money
        user_dic['flow'].append('用户[%s]购物支出[%s￥]'%(name,money))
        logger.info('用户[%s]购物支出[%s￥]'%(name,money))
        db_hander.save(user_dic)
        return True,'购物成功'


# 购物车支付接口
def pay_shoppingcar_interface(name):
    user_dic = db_hander.select(name)
    price_map = {
        '凤爪': 50,
        'T-shirt': 150,
        'macbook': 21800,
        'iphoneX': 7000
    }
    # 商品价格：
    cost = 0
    for i in user_dic['shopping_car']:
        cost += price_map[i] * user_dic['shopping_car'][i]
    if user_dic['balance'] >= cost:
        user_dic['balance'] -= cost
        user_dic['flow'].append('支付[%s￥]成功'%cost)
        logger.info('用户[%s]支付[%s￥]成功'%(name,cost))
        user_dic['shopping_car'] = {}
        db_hander.save(user_dic)
        return True,'支付[%s￥]成功'%cost
    else:
        logger.warning('余额不足，支付失败')
        return False,'余额不足，支付失败'