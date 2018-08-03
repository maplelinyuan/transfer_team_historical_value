# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import realTimeMatchlItem
from scrapy_splash import SplashRequest
from transfer_crawl.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time, datetime

# scrapy crawl realtime_matchs
# class RealtimeMatchsSpider(scrapy.Spider):
class RealtimeMatchsSpider(RedisSpider):
    name = 'realtime_matchs'
    allowed_domains = ['http://live.500.com']
    start_urls = []
    redis_key = 'realtime_matchs:start_urls'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        has_december = False    # 是否包含了12月
        qi_shu = int(response.xpath('//select[@id="sel_expect"]/option/text()').extract()[0])
        trs = response.xpath('//table[@id="table_match"]/tbody/tr')
        for tr in trs:
            if len(tr.xpath('td')) < 13:
                continue
            tds = tr.xpath('td')
            match_id = tr.xpath('@id').extract()[0]
            league_name = tds[1].xpath('a/text()').extract()[0]
            tr_date = tds[3].xpath('text()').extract()[0]
            tr_month = int(tr_date.split('-')[0].replace('0', ''))
            if tr_month == 12:
                has_december = True
            tr_day = int(tr_date.split(' ')[0].split('-')[1].replace('0', ''))
            # 如果是1月1号的话，需要查看之前的比赛是否包含了12月份，如果是则year+1
            if tr_month == 1 and tr_day == 1 and has_december:
                match_time = str(datetime.datetime.now().year + 1) + '-' + tr_date
            else:
                match_time = str(datetime.datetime.now().year) + '-' + tr_date
            home_name = tds[5].xpath('a/text()').extract()[0].strip()
            away_name = tds[7].xpath('a/text()').extract()[0].strip()
            single_item = realTimeMatchlItem()
            single_item['qi_shu'] = qi_shu
            single_item['match_id'] = match_id
            single_item['league_name'] = league_name
            single_item['match_time'] = match_time
            single_item['home_name'] = home_name
            single_item['away_name'] = away_name
            yield single_item
