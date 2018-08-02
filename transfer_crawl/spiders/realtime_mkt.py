# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import realTimeMktlItem
from scrapy_splash import SplashRequest
from transfer_crawl.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time

# scrapy crawl realtime_mkt
# class RealtimeMktSpider(scrapy.Spider):
class RealtimeMktSpider(RedisSpider):
    name = 'realtime_mkt'
    allowed_domains = ['www.transfermarkt.com']
    start_urls = []
    redis_key = 'realtime_mkt:start_urls'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        # 获取当前时间
        time_now = int(time.time())
        # 转换成localtime
        time_local = time.localtime(time_now)
        # 转换成新的时间格式(2016-05-09 18:59:20)
        update_time = time.strftime("%Y-%m-%d %H:%M", time_local)
        trs = response.xpath('//div[@id="yw1"]/table/tbody/tr')
        for tr in trs:
            name = tr.xpath('td')[1].xpath('a/text()').extract()[0]
            market_value = tr.xpath('td')[6].xpath('a/text()').extract()[0]
            if market_value == '-':
                continue
            value_unit = market_value.split(' ')[1].split('.')[0]
            if value_unit == 'Bill':
                value = int(market_value.split(' ')[0].replace(',', '')) * 10000000
            elif value_unit == 'Mill':
                value = int(market_value.split(' ')[0].replace(',', '')) * 10000
            else:
                value = int(market_value.split(' ')[0].replace(',', '')) * 1000
            single_item = realTimeMktlItem()
            single_item['update_time'] = update_time
            single_item['name'] = name
            single_item['value'] = value
            yield single_item
