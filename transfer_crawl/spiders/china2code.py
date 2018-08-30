# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import idMapEnglish
from scrapy_redis.spiders import RedisSpider
import traceback
import time, datetime
from compute_algorithm.chinese_2_english import Chinese_2_english

c_2_e = Chinese_2_english()
# scrapy crawl china2code
# class China2codeSpider(scrapy.Spider):
class China2codeSpider(RedisSpider):
    name = 'china2code'
    allowed_domains = ['http://liansai.500.com']
    start_urls = []
    redis_key = 'china2code:start_urls'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        trs = response.xpath('//table[@class="lstable1 ljifen_top_list_s jTrHover"]/tr')
        for tr in trs:
            if len(tr.xpath('td')) < 7:
                continue
            tds = tr.xpath('td')
            team_id = tds[1].xpath('a')[0].xpath('@href').extract()[0].split('/')[2]
            team_title = tds[1].xpath('a')[0].xpath('@title').extract()[0]
            english_name = c_2_e.get(team_title)
            single_item = idMapEnglish()
            single_item['team_id'] = team_id
            single_item['english_name'] = english_name
            yield single_item