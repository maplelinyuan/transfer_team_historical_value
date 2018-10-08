# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import datetime, time
import pdb
import traceback
import requests
from compute_algorithm.chinese_2_english import Chinese_2_english
from compute_algorithm.my_strategy import My_strategy

class TransferCrawlPipeline(object):
    def __init__(self):
        # 链接数据库
        self.mongo_client = MongoClient(host='localhost', port=27019)
        # self.mongo_client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])     #如果有账户密码

    def process_item(self, item, spider):
        try:
            if spider.name == 'transfermkt':
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'english_version'
                self.coll = self.db[col_name]  # 获得collection的句柄
                current_time = item['current_time']
                name = item['name']
                value = item['value']
                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'current_time': current_time, 'name': name}).count() > 0:
                    insertItem = dict(current_time=current_time, name=name, value=value)
                    self.coll.insert(insertItem)
            elif spider.name == 'realtime_mkt':
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'realtime_mkt'
                self.coll = self.db[col_name]  # 获得collection的句柄
                update_time = item['update_time']
                name = item['name']
                value = item['value']
                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'name': name}).count() > 0:
                    insertItem = dict(update_time=update_time, name=name, value=value)
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(update_time=update_time, value=value)
                    self.coll.update({"name": name},
                                     {'$set': updateItem})
            elif spider.name == 'china2code':
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'id_map_english'
                self.coll = self.db[col_name]  # 获得collection的句柄
                team_id = item['team_id']
                english_name = item['english_name']
                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'team_id': team_id}).count() > 0:
                    insertItem = dict(team_id=team_id, english_name=english_name)
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict( english_name=english_name)
                    self.coll.update({"team_id": team_id},
                                     {'$set': updateItem})
            elif spider.name == 'shili':
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'shili_realtime_matchs'
                self.coll = self.db[col_name]  # 获得collection的句柄
                qi_shu = item['qi_shu']
                match_id = item['match_id']
                league_name = item['league_name']
                match_time = item['match_time']
                home_name = item['home_name']
                away_name = item['away_name']
                home_goal = item['home_goal']
                away_goal = item['away_goal']
                support_direction = item['support_direction']
                sub_col = self.db['new_realtime_matchs']
                home_odd = sub_col.find_one({'match_id': match_id})['home_odd']
                draw_odd = sub_col.find_one({'match_id': match_id})['draw_odd']
                away_odd = sub_col.find_one({'match_id': match_id})['away_odd']

                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'match_id': match_id}).count() > 0:
                    insertItem = dict(qi_shu=qi_shu, match_id=match_id, league_name=league_name, match_time=match_time,
                                      home_name=home_name, away_name=away_name,
                                      home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd,
                                      home_goal=home_goal, away_goal=away_goal,
                                      support_direction=support_direction)
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(league_name=league_name,
                                      home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd,
                                      home_goal=home_goal, away_goal=away_goal,
                                      support_direction=support_direction)
                    self.coll.update({"match_id": match_id},
                                     {'$set': updateItem})
            elif spider.name == 'shot_rate':
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'shot_rate_realtime_matchs'
                self.coll = self.db[col_name]  # 获得collection的句柄
                danchang_code = item['danchang_code']
                zhu_ke_index = item['zhu_ke_index']
                match_id = item['match_id']
                league_name = item['league_name']
                match_time = item['match_time']
                home_name = item['home_name']
                away_name = item['away_name']
                cur_score = item['cur_score']
                cur_lose_score = item['cur_lose_score']
                total_shot = item['total_shot']
                total_was_shoted = item['total_was_shoted']

                # 根据zhu_ke_index 确定该场比赛主或者客进球数
                if zhu_ke_index == 0:
                    home_score = cur_score
                    home_lose_score = cur_lose_score
                    home_total_shot = total_shot
                    home_total_was_shoted = total_was_shoted
                    away_score = 0
                    away_lose_score = 0
                    away_total_shot = 0
                    away_total_was_shoted = 0
                else:
                    away_score = cur_score
                    away_lose_score = cur_lose_score
                    away_total_shot = total_shot
                    away_total_was_shoted = total_was_shoted
                    home_score = 0
                    home_lose_score = 0
                    home_total_shot = 0
                    home_total_was_shoted = 0

                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'match_id': match_id}).count() > 0:
                    insertItem = dict(danchang_code=danchang_code, match_id=match_id, league_name=league_name, match_time=match_time,
                                      home_name=home_name, away_name=away_name,
                                      home_score=home_score, home_lose_score=home_lose_score, home_total_shot=home_total_shot, home_total_was_shoted=home_total_was_shoted,
                                      away_score=away_score, away_lose_score=away_lose_score, away_total_shot=away_total_shot, away_total_was_shoted=away_total_was_shoted,
                                      )
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(
                        home_score=home_score, home_lose_score=home_lose_score, home_total_shot=home_total_shot, home_total_was_shoted=home_total_was_shoted,
                        away_score=away_score, away_lose_score=away_lose_score, away_total_shot=away_total_shot,away_total_was_shoted=away_total_was_shoted,
                    )
                    self.coll.update({"match_id": match_id},
                                     {'$inc': updateItem})
            else:
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'new_realtime_matchs'
                self.coll = self.db[col_name]  # 获得collection的句柄
                self.id_coll = self.db['id_map_english']
                qi_shu = item['qi_shu']
                match_id = item['match_id']
                league_name = item['league_name']
                match_time = item['match_time']
                home_id = item['home_id']
                away_id = item['away_id']
                home_name = item['home_name']
                away_name = item['away_name']
                home_odd = item['home_odd']
                draw_odd = item['draw_odd']
                away_odd = item['away_odd']
                home_goal = item['home_goal']
                away_goal = item['away_goal']
                home_origin_lisan = item['home_origin_lisan']
                draw_origin_lisan = item['draw_origin_lisan']
                away_origin_lisan = item['away_origin_lisan']
                home_lisan = item['home_lisan']
                draw_lisan = item['draw_lisan']
                away_lisan = item['away_lisan']
                sub_col = self.db['realtime_mkt']
                home_value = ''
                away_value = ''
                value_ratio = ''
                # if home_name == '哈特贝格':
                #     pdb.set_trace()
                try:
                    english_home_name = self.id_coll.find_one({'team_id': home_id})['english_name']
                    english_away_name = self.id_coll.find_one({'team_id': away_id})['english_name']
                except Exception as err:
                    print('转化名称出错')
                    return
                if sub_col.find({'name': english_home_name}).count() > 0:
                    home_value = sub_col.find_one({'name': english_home_name})['value']
                if sub_col.find({'name': english_away_name}).count() > 0:
                    away_value = sub_col.find_one({'name': english_away_name})['value']
                if home_value and away_value:
                    value_ratio = round(home_value/away_value, 2)

                if value_ratio != '':
                    get_direction = My_strategy()
                    support_direction = get_direction.get(league_name, value_ratio, home_odd, draw_odd, away_odd, home_value, away_value, home_lisan, draw_lisan, away_lisan)
                else:
                    support_direction = ''

                home_lisan_rate = round(home_lisan/home_origin_lisan, 2)
                draw_lisan_rate = round(draw_lisan/draw_origin_lisan, 2)
                away_lisan_rate = round(away_lisan/away_origin_lisan, 2)
                lisan_rate_arr = [home_lisan_rate, draw_lisan_rate, away_lisan_rate]
                lisan_support_index = lisan_rate_arr.index(min(lisan_rate_arr))
                max_odd_value = 5
                lisan_support = ''
                cur_profit = 0
                max_lisan_rate = 0.7        # 关键参数
                if not (lisan_rate_arr[lisan_support_index] < max_lisan_rate):
                    if lisan_support_index == 0 and home_odd <= max_odd_value:
                        lisan_support = 3
                        if not (home_goal == '' or away_goal == ''):
                            if home_goal > away_goal:
                                cur_profit = round(home_odd - 1, 2)
                            else:
                                cur_profit = -1
                    elif lisan_support_index == 1 and draw_odd <= max_odd_value:
                        lisan_support = 1
                        if not (home_goal == '' or away_goal == ''):
                            if home_goal == away_goal:
                                cur_profit = round(draw_odd - 1, 2)
                            else:
                                cur_profit = -1
                    elif lisan_support_index == 2 and away_odd <= max_odd_value:
                        lisan_support = 0
                        if not (home_goal == '' or away_goal == ''):
                            if home_goal < away_goal:
                                cur_profit = round(away_odd - 1, 2)
                            else:
                                cur_profit = -1
                    else:
                        lisan_support = ''

                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'match_id': match_id}).count() > 0:
                    insertItem = dict(qi_shu=qi_shu, match_id=match_id, league_name=league_name, match_time=match_time,
                                      home_name=home_name, away_name=away_name, home_value=home_value, away_value=away_value,
                                      home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd,
                                      home_origin_lisan=home_origin_lisan, draw_origin_lisan=draw_origin_lisan, away_origin_lisan=away_origin_lisan,
                                      home_lisan=home_lisan, draw_lisan=draw_lisan, away_lisan=away_lisan,
                                      home_lisan_rate=home_lisan_rate, draw_lisan_rate=draw_lisan_rate, away_lisan_rate=away_lisan_rate,
                                      lisan_support=lisan_support,
                                      home_goal=home_goal, away_goal=away_goal,
                                      cur_profit=cur_profit,
                                      value_ratio=value_ratio, support_direction=support_direction)
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(league_name=league_name, home_value=home_value, away_value=away_value, home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd,
                                      home_origin_lisan=home_origin_lisan, draw_origin_lisan=draw_origin_lisan, away_origin_lisan=away_origin_lisan,
                                      home_lisan=home_lisan, draw_lisan=draw_lisan, away_lisan=away_lisan,
                                      home_lisan_rate=home_lisan_rate, draw_lisan_rate=draw_lisan_rate, away_lisan_rate=away_lisan_rate,
                                      lisan_support=lisan_support,
                                      home_goal=home_goal, away_goal=away_goal,
                                      cur_profit=cur_profit,
                                      value_ratio=value_ratio, support_direction=support_direction)
                    self.coll.update({"match_id": match_id},
                                     {'$set': updateItem})

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
        finally:
            self.mongo_client.close()
        return item
