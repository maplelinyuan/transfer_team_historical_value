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
                    support_direction = get_direction.get(league_name, value_ratio, home_odd, draw_odd, away_odd, home_value, away_value)
                else:
                    support_direction = ''
                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'match_id': match_id}).count() > 0:
                    insertItem = dict(qi_shu=qi_shu, match_id=match_id, league_name=league_name, match_time=match_time,
                                      home_name=home_name, away_name=away_name, home_value=home_value, away_value=away_value,
                                      home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd, home_lisan=home_lisan, draw_lisan=draw_lisan, away_lisan=away_lisan,
                                      home_goal=home_goal, away_goal=away_goal,
                                      value_ratio=value_ratio, support_direction=support_direction)
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(league_name=league_name, home_value=home_value, away_value=away_value, home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd,
                                      home_lisan=home_lisan, draw_lisan=draw_lisan, away_lisan=away_lisan,
                                      home_goal=home_goal, away_goal=away_goal, value_ratio=value_ratio, support_direction=support_direction)
                    self.coll.update({"match_id": match_id},
                                     {'$set': updateItem})

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
        finally:
            self.mongo_client.close()
        return item
