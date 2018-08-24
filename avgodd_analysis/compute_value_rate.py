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
    col_name = 'avgodd_match_results'
    coll = db[col_name]  # 获得collection的句柄
    value_coll = db['english_version']

    for item in coll.find():
        cur_id = item['match_id']
        cur_time = item['match_time']
        need_value_time = transform_time(cur_time)
        try:
            home_name = item['home_name']
            english_home_name = c_2_e.get(home_name)
            away_name = item['away_name']
            english_away_name = c_2_e.get(away_name)
        except Exception as err:
            updateItem = dict(value_ratio='')
            coll.update({"match_id": cur_id},
                        {'$set': updateItem})
            print('%s\n%s' % (err, traceback.format_exc()))
            continue
        # 特殊处理
        if need_value_time.split('-')[0] == '2014' and 5 < int(need_value_time.split('-')[1]) < 11:
            updateItem = dict(value_ratio='')
            coll.update({"match_id": cur_id},
                        {'$set': updateItem})
            continue
        if need_value_time.split('-')[0] == '2010' and int(need_value_time.split('-')[1]) < 11:
            updateItem = dict(value_ratio='')
            coll.update({"match_id": cur_id},
                        {'$set': updateItem})
            continue
        find_home_value = value_coll.find({'$and': [{'name': english_home_name}, {"current_time": need_value_time}]})
        find_away_value = value_coll.find({'$and': [{'name': english_away_name}, {"current_time": need_value_time}]})
        if find_home_value.count() == 0 or find_away_value.count() == 0:
            updateItem = dict(value_ratio='')
            coll.update({"match_id": cur_id},
                        {'$set': updateItem})
            continue
        home_value = find_home_value[0]['value']
        away_value = find_away_value[0]['value']
        value_ratio = round(home_value / away_value, 2)  # 主客身价比
        updateItem = dict(value_ratio=value_ratio)
        coll.update({"match_id": cur_id},
                                     {'$set': updateItem})

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))

finally:
    mongo_client.close()
