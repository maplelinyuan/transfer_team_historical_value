# -- coding:utf-8 --
from pymongo import MongoClient
import os
import time
import pdb, traceback

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
def is_between(value, low, up=float('inf')):
    if value >= low and value < up:
        return True
    else:
        return False

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'market_value'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'match_results'
    coll = db[col_name]  # 获得collection的句柄

    total = 0
    shot = 0
    gain = 0
    league_name = '乌超'
    limit_odd = 0
    max_odd = 3.2
    expected_result = 1
    low_limit = 0.8
    high_limit = 0.9
    match_dict = {}

    for item in coll.find({'league_name': league_name}):
        cur_time = item['match_time']
        need_value_time = transform_time(cur_time)
        if int(need_value_time.split('-')[0]) < 2013:
            continue
        # 特殊处理
        year_month_key = need_value_time.split('-')[0] + '_' + need_value_time.split('-')[1]
        if not year_month_key in match_dict.keys():
            match_dict[year_month_key] = 0

        cur_id = item['match_id']
        cur_ratio = item['value_ratio']
        if cur_ratio == '':
            continue
        match_result = item['match_result']
        home_odd = float(item['home_odd'])
        draw_odd = float(item['draw_odd'])
        away_odd = float(item['away_odd'])
        if expected_result == 3:
            cur_odd = home_odd
        elif expected_result == 1:
            cur_odd = draw_odd
        else:
            cur_odd = away_odd
        if is_between(cur_ratio, low_limit, high_limit):
            if cur_odd >= limit_odd and cur_odd <= max_odd:
                total += 1
                if match_result == expected_result:
                    shot += 1
                    gain += cur_odd
                    cur_profit = round(cur_odd - 1, 3)
                    match_dict[year_month_key] += cur_profit
                else:
                    match_dict[year_month_key] -= 1
    for key, value in match_dict.items():
        print('{key}:{value}'.format(key=key, value=value))
    profit = gain - total
    print('总数：%s, 命中率：%s, 利润：%s, 利润率：%s' % (total, round(shot/total, 3), round(profit, 3), round((profit)/total, 3)))


except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))