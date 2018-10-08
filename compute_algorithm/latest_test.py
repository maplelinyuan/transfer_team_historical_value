# -- coding:utf-8 --
from pymongo import MongoClient
import os
import time
import pdb, traceback
from chinese_2_english import Chinese_2_english
import matplotlib.pyplot as plt

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

c_2_e = Chinese_2_english()


total = 0
revenue = 0
total_expected_result = 0
watch_direction = 0

# Specific parameters
limit_year = 2015
least_ratio = 0.02
max_ratio = 0.1
min_odd = 2.2
max_odd = 3.8

# picture
home_odd_arr = []
draw_odd_arr = []
away_odd_arr = []
home_value_arr = []
draw_value_arr = []
away_value_arr = []
show_pic = True
fig = plt.figure()
ax1 = fig.add_subplot(111)
# 设置标题
ax1.set_title('Scatter Plot')

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'market_value'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'match_results'
    coll = db[col_name]  # 获得collection的句柄

    for single_match in coll.find():
        home_odd = float(single_match['home_odd'])
        draw_odd = float(single_match['draw_odd'])
        away_odd = float(single_match['away_odd'])
        value_ratio = single_match['value_ratio']
        cur_time = single_match['match_time']
        need_value_time = transform_time(cur_time)
        if int(need_value_time.split('-')[0]) < limit_year:
            continue
        match_result = single_match['match_result']
        if value_ratio != '' and value_ratio >= least_ratio and value_ratio <= max_ratio:
            if total_expected_result == 3:
                revenue_odd = home_odd
            elif total_expected_result == 1:
                revenue_odd = draw_odd
            else:
                revenue_odd = away_odd

            if watch_direction == 3:
                cur_odd = home_odd
            elif watch_direction == 1:
                cur_odd = draw_odd
            else:
                cur_odd = away_odd

            if cur_odd >= min_odd and cur_odd <= max_odd:
                total += 1
                if match_result == 3:
                    home_odd_arr.append(cur_odd)
                    home_value_arr.append(value_ratio)
                elif match_result == 1:
                    draw_odd_arr.append(cur_odd)
                    draw_value_arr.append(value_ratio)
                else:
                    away_odd_arr.append(cur_odd)
                    away_value_arr.append(value_ratio)
                if match_result == total_expected_result:
                    revenue += revenue_odd

    if total != 0:
        print('最小身价比: %s, 最大身价比: %s, 投注总数：%s, 总利润：%s, 利润率：%s' % (
        least_ratio, max_ratio, total, round(revenue - total, 2), round((revenue - total) / total, 2)))
        profit_ratio = round((revenue - total) / total, 2)
    # 设置X轴标签
    plt.xlabel('value_ratio')
    # 设置Y轴标签
    plt.ylabel('odd')
    # 画散点图
    ax1.scatter(home_value_arr, home_odd_arr, c='r', marker='o')
    ax1.scatter(draw_value_arr, draw_odd_arr, c='g', marker='o')
    ax1.scatter(away_value_arr, away_odd_arr, c='b', marker='o')
    # 设置图标
    plt.legend(['home', 'draw', 'away'])
    if show_pic:
        plt.show()

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))

finally:
    mongo_client.close()
