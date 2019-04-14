# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/4/14 13:31

import json
import os
from conf import settings


# 存储数据
def save(user_dic):
    user_path = '%s/%s.json'%(settings.DB_PATH, user_dic['name'])
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic,f)


# 查询数据
def select(name):
    user_path = '%s/%s.json' % (settings.DB_PATH, name)
    # 判断查询的数据是否存在
    if not os.path.exists(user_path):
        return
    with open(user_path, 'r', encoding='utf-8') as f:
        user_dic = json.load(f)
        return user_dic