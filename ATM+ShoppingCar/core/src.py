# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/4/14 13:31
from interface import bank, shop, user
from lib import common

user_info = {
    'name': None
}


# 注销
def logout():
    if not user_info['name']:
        print('当前没有用户登录，不需注销！')
        return
    else:
        msg = user.logout_interface()
        print(msg)


# 注册
def register():
    print('注册界面'.center(20, '-'))
    while True:
        name = input("请设置用户名：")
        info = user.check_user_interface(name)
        # info接收到False，if为真则退出，否则继续注册
        if not info:
            break
        pwd = input("请设置密码：")
        conf_pwd = input("请再次确认密码：")
        if pwd == conf_pwd:
            flag, msg = user.register_interface(name, pwd)
            if flag:
                print(msg)
                break
        else:
            print('两次密码不一致，请确认！')


# 登录
def login():
    print('登录界面'.center(20, '-'))
    while True:
        name = input("请输入账户名：")
        pwd = input("请输入密码：")
        flag, msg = user.login_interface(name, pwd)
        if flag:
            print(msg)
            user_info['name'] = name
            break
        else:
            print(msg)


# 查看余额
@common.user_status
def check_balance():
    print('查看余额界面'.center(20, '-'))
    msg = bank.check_balance_interface(user_info['name'])
    print('用户[%s]当前余额为[%s￥]' % (user_info['name'], msg))


# 提现
@common.user_status
def withdraw():
    print('提现界面'.center(20, '-'))
    while True:
        money = input("请输入您要提现的金额：")
        if money.isdigit():
            money = int(money)
            flag, msg = bank.withdraw_interface(user_info['name'], money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print("请输入纯数字！")


# 转账
@common.user_status
def transfer():
    print('转账界面'.center(20, '-'))
    while True:
        to_user = input("请输入对方账户名：")
        money = input("请输入转账金额：")
        if money.isdigit():
            money = int(money)
            flag, msg = bank.transfer_interface(user_info['name'], to_user, money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print("请输入纯数字！")


# 还款
@common.user_status
def repay():
    print('还款界面'.center(20, '-'))
    money = input("请输入还款金额：")
    if money.isdigit():
        money = int(money)
        msg = bank.repay_interface(user_info['name'], money)
        print(msg)


# 查看流水
@common.user_status
def check_flow():
    print('查看流水界面'.center(20, '-'))
    msg = bank.check_flow_interface(user_info['name'])
    for i in msg:
        print(i)


# 购物车
@common.user_status
def shopping():
    print('购物界面'.center(20, '-'))
    goods_list = [
        ['凤爪', 50],
        ['T-shirt', 150],
        ['macbook', 21800],
        ['iphoneX', 7000]
    ]
    shopping_car = {}
    while True:
        for index, goods in enumerate(goods_list):
            print("编号：%s  商品：%s" % (index, goods))
        choice = input("请输入商品编号（按q退出）：")
        if choice.isdigit():
            choice = int(choice)
            if choice >= 0 and choice < len(goods_list):
                goods_name, goods_price = goods_list[choice]
                choose = input("请选择：\n1、直接购买\n2、加入购物车")
                if choose == '1':
                    flag, msg = bank.pay(user_info['name'], goods_price)
                    if flag:
                        print(msg)
                        break
                elif choose == '2':
                    shopping_car.setdefault(goods_name, 0)
                    shopping_car[goods_name] += 1
                    flag, msg1 = shop.add_shopping_car_interface(user_info['name'], shopping_car)
                    if flag:
                        print(msg1)
                        for i in shopping_car:
                            print("商品：%s  数量：%s" % (i, shopping_car[i]))
                else:
                    print("输入的商品编号不存在！！！")
        elif choice == 'q':
            print('退出购买')
            break
        else:
            print("非法输入！！！")


# 查看购物车
@common.user_status
def check_shop():
    print('查看购物车界面'.center(20, '-'))
    flag, msg = shop.check_shop_interface(user_info['name'])
    if flag:
        for i in msg:
            print("商品：%s  数量：%s"%(i,msg[i]))
        if msg:
            choice = input("是否要支付？(y/n)")
            if choice == 'y':
                flag1,msg1 = bank.pay_shoppingcar_interface(user_info['name'])
                if flag1:
                    print(msg1)
                else:
                    print(msg1)
            elif choice == 'n':
                print("您已选择退出！")
    else:
        print(msg)


method_map = {
    '0': logout,
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': transfer,
    '6': repay,
    '7': check_flow,
    '8': shopping,
    '9': check_shop,
}


def run():
    while True:
        print('''
        0  注销
        1  注册
        2  登录
        3  查看余额
        4  提现
        5  转账
        6  还款
        7  查看流水
        8  购物车
        9  查看购物车
        q  退出
        ''')
        choice = input("请选择操作编号：")
        if choice == 'q':
            break
        elif choice in method_map:
            method_map[choice]()
        else:
            print("非法输入！")
