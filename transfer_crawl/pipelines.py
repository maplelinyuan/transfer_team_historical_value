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
                if not self.coll.find({'update_time': update_time, 'name': name}).count() > 0:
                    insertItem = dict(update_time=update_time, name=name, value=value)
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(update_time=update_time, value=value)
                    self.coll.update({"name": name},
                                     {'$set': updateItem})
            else:
                db_name = 'market_value'
                self.db = self.mongo_client[db_name]  # 获得数据库的句柄
                col_name = 'realtime_matchs'
                self.coll = self.db[col_name]  # 获得collection的句柄
                match_id = item['match_id']
                league_name = item['league_name']
                match_time = item['match_time']
                home_name = item['home_name']
                away_name = item['away_name']
                # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
                if not self.coll.find({'match_id': match_id}).count() > 0:
                    insertItem = dict(match_id=match_id, league_name=league_name, match_time=match_time, home_name=home_name, away_name=away_name)
                    self.coll.insert(insertItem)

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
        finally:
            self.mongo_client.close()
        return item
