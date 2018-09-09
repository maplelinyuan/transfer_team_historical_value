# -- coding:utf-8 --
from pymongo import MongoClient
import os
import time
import pdb, traceback
from chinese_2_english import Chinese_2_english

c_2_e = Chinese_2_english()

def transform_time(time_str):
    if time_str.split('-')[1][0] == '0':
        time_str = time_str.split('-')[0] + '-' + time_str.split('-')[1][1] + '-' + time_str.split('-')[2]
    if time_str.split('-')[2].split(' ')[0][0] == '0':
        day = int(time_str.split('-')[2].split(' ')[0][1])
    else:
        day = int(time_str.split('-')[2].split(' ')[0])
    # 根据当天日期判断使用1还是15作为查询日期
    if day >= 1 and day < 15:
        time_str = time_str.split('-')[0] + '-' + time_str.split('-')[1] + '-' + '01'
    else:
        time_str = time_str.split('-')[0] + '-' + time_str.split('-')[1] + '-' + '15'
    return time_str


try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'market_value'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'new_realtime_matchs'
    coll = db[col_name]  # 获得collection的句柄

    for item in coll.find():
        cur_id = item['match_id']
        home_odd = item['home_odd']
        value_ratio = item['value_ratio']
        if value_ratio == '':
            coll.update({"match_id": cur_id},
                        {'$set': dict(home_product=0)})
            continue
        home_product = round(value_ratio/(value_ratio + 1) * home_odd, 4)
        updateItem = dict(home_product=home_product)
        coll.update({"match_id": cur_id},
                    {'$set': updateItem})

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))

finally:
    mongo_client.close()
