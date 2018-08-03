# -- coding:utf-8 --
from pymongo import MongoClient
import os
import time
import pdb, traceback

mongo_client = MongoClient(host='localhost', port=27019)
db_name = 'market_value'
db = mongo_client[db_name]  # 获得数据库的句柄
col_name = 'english_version'
coll = db[col_name]  # 获得collection的句柄

for item in coll.find():
    cur_name = item['name']
    cur_time = item['current_time']
    if cur_name[0] == ' ' or cur_name[-1] == ' ':
        print('修改%s的名称' % cur_name)
        updateItem = dict(name=cur_name.strip())
        coll.update({'current_time': cur_time, 'name':cur_name}, updateItem)