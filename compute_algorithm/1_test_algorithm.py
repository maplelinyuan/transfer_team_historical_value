# -- coding:utf-8 --
from pymongo import MongoClient
import os
import time
import pdb, traceback
from chinese_2_english import Chinese_2_english
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)

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

index_arr = [0, 0.1, 0.2, 0.3, 0.4 ,0.5 ,0.6 ,0.7, 0.8, 0.9, 1, 1.1, 1.25, 1.43, 1.67, 2, 2.5, 3.33, 5, 10]
result_arr = [0] * 20
profit_ratio_arr = []

# 参数
league_name = '葡甲'
buy_result = 3

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'market_value'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'match_results'
    coll = db[col_name]  # 获得collection的句柄
    print('购买%s利润' % buy_result)
    for cur_index in range(len(index_arr)):
        total = 0
        revenue = 0
        for single_match in coll.find({'league_name': league_name}):
            home_name = single_match['home_name']
            english_home_name = c_2_e.get(home_name)
            away_name = single_match['away_name']
            english_away_name = c_2_e.get(away_name)
            match_time = single_match['match_time']
            match_result = single_match['match_result']
            home_odd = float(single_match['home_odd'])
            draw_odd = float(single_match['draw_odd'])
            away_odd = float(single_match['away_odd'])
            # 获取身价
            value_col_name = 'english_version'
            value_coll = db[value_col_name]  # 获得collection的句柄
            need_value_time = transform_time(match_time)

            # 特殊处理
            if need_value_time.split('-')[0] == '2014' and 5 < int(need_value_time.split('-')[1]) < 11:
                continue
            if need_value_time.split('-')[0] == '2010' and int(need_value_time.split('-')[1]) < 11:
                continue
            # 特殊处理结束

            # 获取主客身价
            try:
                find_home_value = value_coll.find({'$and': [{'name': english_home_name}, {"current_time": need_value_time}]})
                find_away_value = value_coll.find({'$and': [{'name': english_away_name}, {"current_time": need_value_time}]})
                if find_home_value.count() == 0 or find_away_value.count() == 0:
                    continue
                home_value = find_home_value[0]['value']
                away_value = find_away_value[0]['value']
            except Exception as err:
                pdb.set_trace()
            value_ratio = round(home_value/away_value, 2)   # 主客身价比
            # 统计不同比下的赛果数量
            # if match_result == 1:
            #     if value_ratio >= 10:
            #         result_arr[19] += 1
            #     elif value_ratio >= 5:
            #         result_arr[18] += 1
            #     elif value_ratio >= 3.33:
            #         result_arr[17] += 1
            #     elif value_ratio >= 2.5:
            #         result_arr[16] += 1
            #     elif value_ratio >= 2:
            #         result_arr[15] += 1
            #     elif value_ratio >= 1.67:
            #         result_arr[14] += 1
            #     elif value_ratio >= 1.43:
            #         result_arr[13] += 1
            #     elif value_ratio >= 1.25:
            #         result_arr[12] += 1
            #     elif value_ratio >= 1.1:
            #         result_arr[11] += 1
            #     elif value_ratio >= 1:
            #         result_arr[10] += 1
            #     elif value_ratio >= 0.9:
            #         result_arr[9] += 1
            #     elif value_ratio >= 0.8:
            #         result_arr[8] += 1
            #     elif value_ratio >= 0.7:
            #         result_arr[7] += 1
            #     elif value_ratio >= 0.6:
            #         result_arr[6] += 1
            #     elif value_ratio >= 0.5:
            #         result_arr[5] += 1
            #     elif value_ratio >= 0.4:
            #         result_arr[4] += 1
            #     elif value_ratio >= 0.3:
            #         result_arr[3] += 1
            #     elif value_ratio >= 0.2:
            #         result_arr[2] += 1
            #     elif value_ratio >= 0.1:
            #         result_arr[1] += 1
            #     elif value_ratio >= 0:
            #         result_arr[0] += 1
            # index_arr = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.25, 1.43, 1.67, 2, 2.5, 3.33, 5,10]
            # 计算利润
            if cur_index == len(index_arr) - 1:
                if index_arr[cur_index] <= value_ratio:
                    total += 1
                    if match_result == buy_result:
                        if buy_result == 3:
                            revenue += home_odd
                        elif buy_result == 1:
                            revenue += draw_odd
                        else:
                            revenue += away_odd
            else:
                if index_arr[cur_index] <= value_ratio and value_ratio < index_arr[cur_index+1]:
                    total += 1
                    if match_result == buy_result:
                        if buy_result == 3:
                            revenue += home_odd
                        elif buy_result == 1:
                            revenue += draw_odd
                        else:
                            revenue += away_odd
        if total != 0:
            print('当前比例：%s, 投注总数：%s, 总收入：%s, 利润率：%s' % (index_arr[cur_index], total, revenue, round((revenue - total)/total, 2)))
            profit_ratio = round((revenue - total) / total, 2)
        else:
            profit_ratio = 0
        profit_ratio_arr.append(profit_ratio)

    # 画图
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(u'%s value ratio_for_%s' % (league_name, buy_result), fontproperties=font_set)
    plt.plot(index_arr, profit_ratio_arr)
    plt.show()


except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()