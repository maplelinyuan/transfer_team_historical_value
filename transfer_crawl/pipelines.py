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
        db_name = 'market_value'
        self.db = self.mongo_client[db_name]  # 获得数据库的句柄
        col_name = 'english_version'
        self.coll = self.db[col_name]  # 获得collection的句柄
        current_time = item['current_time']
        name = item['name']
        value = item['value']
        try:
            # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
            if not self.coll.find({'current_time': current_time, 'name': name}).count() > 0:
                insertItem = dict(current_time=current_time, name=name, value=value)
                self.coll.insert(insertItem)

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
        finally:
            self.mongo_client.close()
        return item
