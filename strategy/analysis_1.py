# -- coding:utf-8 --
from pymongo import MongoClient
import os
import time
import pdb, traceback
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
    profit = 0
    league_name = '德甲'
    league_name_arr = ['德甲', '英超', '法甲', '法乙', '俄超', '比甲', '德乙', '乌超', '丹超', '英甲', '西甲', '丹甲', '捷甲', '意乙', '西乙', '波甲', '芬超', '奥乙', '奥甲',
                                '土超', 'K1联赛', '挪超', '荷甲', 'K2联赛', 'J1联赛', '澳超', 'J2联赛', '瑞典超', '俄甲', '苏超', '瑞士超', '瑞士甲', '荷乙', '冰岛超',
                                '葡超', '巴西甲', '墨超', '巴西乙', '葡甲', '阿甲']
    limit_odd = 2.5
    max_odd = 3.8
    expected_result = 1
    low_limit = 1.3
    high_limit = 1.4
    select_1 = True
    home_odd_arr = []
    draw_odd_arr = []
    away_odd_arr = []
    home_value_arr = []
    draw_value_arr = []
    away_value_arr = []
    year = 2017
    show_pic = False

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # 设置标题
    ax1.set_title('Scatter Plot')

    for ratio in range(0, 40, 1):
        ratio_min = ratio * 0.1
        ratio_max = ratio * 0.1 + 0.1
        for expected_result in [3, 1, 0]:
            # for item in coll.find({'$and':[{'league_name': {'$in':league_name_arr}}]}):
            # for item in coll.find({'$and':[{'league_name': league_name}]}):
            for item in coll.find():
                cur_time = item['match_time']
                need_value_time = transform_time(cur_time)
                if int(need_value_time.split('-')[0]) < year:
                    continue
                # 特殊处理
                year_month_key = need_value_time.split('-')[0] + '_' + need_value_time.split('-')[1]

                cur_id = item['match_id']
                try:
                    cur_ratio = item['value_ratio']
                except Exception as err:
                    print('%s 错误！' % item['league_name'])
                if cur_ratio == '':
                    continue
                match_result = item['match_result']
                home_odd = float(item['home_odd'])
                draw_odd = float(item['draw_odd'])
                away_odd = float(item['away_odd'])
                if expected_result == 3:
                    cur_odd = draw_odd
                elif expected_result == 1:
                    cur_odd = draw_odd
                else:
                    cur_odd = draw_odd
                if is_between(cur_ratio, ratio_min, ratio_max):
                    cur_max_odd = max_odd
                    if cur_odd >= limit_odd and cur_odd <= cur_max_odd:
                        total += 1
                        if match_result == 3:
                            home_odd_arr.append(cur_odd)
                            home_value_arr.append(cur_ratio)
                        elif match_result == 1:
                            draw_odd_arr.append(cur_odd)
                            draw_value_arr.append(cur_ratio)
                        else:
                            away_odd_arr.append(cur_odd)
                            away_value_arr.append(cur_ratio)
                        if select_1:
                            if match_result == 1:
                                shot += 1
                                profit += draw_odd - 1
                            else:
                                profit -= 1
                        else:
                            if match_result != 1:
                                shot += 1
                                profit += (home_odd + away_odd)/4 - 1
                            else:
                                profit -= 1

        shot = shot/3
        total = total/3
        profit = profit/3
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
        # 显示利润
        print('比例范围：%s-%s, 总数：%s, 命中率：%s, 利润：%s, 利润率：%s' % (ratio_min, ratio_max, total, round(shot/total, 3), round(profit, 3), round((profit)/total, 3)))
        # 显示所画的图
        if show_pic:
            plt.show()


except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))