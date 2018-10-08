# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import shotRateItem
from scrapy_splash import SplashRequest
from transfer_crawl.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time, datetime

# scrapy crawl shot_rate
# class ShotRateSpider(scrapy.Spider):
class ShotRateSpider(RedisSpider):
    name = 'shot_rate'
    allowed_domains = ['https://live.dszuqiu.com']
    start_urls = []
    redis_key = 'shot_rate:start_urls'
    splashurl = "http://192.168.99.100:8050/render.html"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        trs = response.xpath('//table[@class="live-list-table MBBlock"]/tbody/tr')
        for tr in trs:
            if len(tr.xpath('td')) < 15:
                continue
            tds = tr.xpath('td')
            danchang_code = tds[1].xpath('text()').extract()[0].split('单场')[-1]
            match_id = tds[-2].xpath('a')[0].xpath('@href').extract()[0].split('/')[-1]
            match_time = '20' + tds[2].xpath('text()').extract()[0]
            league_name = tds[0].xpath('text()').extract()[0]
            home_name = tds[3].xpath('a/text()').extract()[0].strip()
            home_id = tds[3].xpath('a/@href').extract()[0].split('/')[-1]
            away_name = tds[5].xpath('a/text()').extract()[0].strip()
            away_id = tds[5].xpath('a/@href').extract()[0].split('/')[-1]

            current_info = dict(zhu_ke_index=0, danchang_code=danchang_code, league_name=league_name, match_id=match_id, match_time=match_time, home_id=home_id, away_id=away_id, home_name=home_name, away_name=away_name)

            zhu_ke_index = 0
            for cur_id in [home_id, away_id]:
                current_info['zhu_ke_index'] = zhu_ke_index
                match_detail_href = 'https://www.dszuqiu.com/team/%s' % cur_id
                yield scrapy.Request(match_detail_href, self.detail_info_parse, meta=current_info, dont_filter=True)
                zhu_ke_index += 1


    def detail_info_parse(self, response):
        pdb.set_trace()
        danchang_code = response.meta['danchang_code']
        zhu_ke_index = response.meta['zhu_ke_index']
        league_name = response.meta['league_name']
        match_id = response.meta['match_id']
        match_time = response.meta['match_time']
        home_name = response.meta['home_name']
        away_name = response.meta['away_name']
        home_id = response.meta['home_id']
        away_id = response.meta['away_id']

        ended_matchs = response.xpath('//section[@id="ended"]/table/tbody/tr')
        for tr in ended_matchs:
            tds = tr.xpath('td')
            cur_zhuke_index = 0     # 当前主客
            cur_score = 0  # 当前球队进球
            cur_lose_score = 0  # 当前球队失球
            cur_home_name = tds[3].xpath('a/text()').extract()[0].strip()
            cur_away_name = tds[5].xpath('a/text()').extract()[0].strip()
            home_score = int(tds[4].xpath('text()').extract()[0].split(':')[0].strip())
            away_score = int(tds[4].xpath('text()').extract()[0].split(':')[-1].strip())
            if zhu_ke_index == 0:
                if cur_home_name == home_name:
                    cur_zhuke_index = 0
                    cur_score = home_score
                    cur_lose_score = away_score
                else:
                    cur_zhuke_index = 1
                    cur_score = away_score
                    cur_lose_score = home_score
            else:
                if cur_away_name == away_name:
                    cur_zhuke_index = 1
                    cur_score = away_score
                    cur_lose_score = home_score
                else:
                    cur_zhuke_index = 0
                    cur_score = home_score
                    cur_lose_score = away_score
            cur_match_id = tds[-2].xpath('a/@href').extract()[0].split('/')[-1]
            current_info = dict(danchang_code=danchang_code, league_name=league_name, match_id=match_id,
                                zhu_ke_index=zhu_ke_index, match_time=match_time, home_id=home_id, away_id=away_id, home_name=home_name,away_name=away_name,
                                cur_zhuke_index=cur_zhuke_index, cur_score=cur_score, cur_lose_score=cur_lose_score)
            match_detail_href = 'https://www.dszuqiu.com/race_xc/%s' % cur_match_id
            yield scrapy.Request(match_detail_href, self.detail_match_parse, meta=current_info, dont_filter=True)

    def detail_match_parse(self, response):
        danchang_code = response.meta['danchang_code']
        zhu_ke_index = response.meta['zhu_ke_index']
        league_name = response.meta['league_name']
        match_id = response.meta['match_id']
        match_time = response.meta['match_time']
        home_name = response.meta['home_name']
        away_name = response.meta['away_name']
        home_id = response.meta['home_id']
        away_id = response.meta['away_id']
        cur_zhuke_index = response.meta['cur_zhuke_index']
        cur_score = response.meta['cur_score']
        cur_lose_score = response.meta['cur_lose_score']

        gongfang_div = response.xpath('//div[@id="race_data_pct"]/div[@class="panel-body"]/div')
        if cur_zhuke_index == 0:
            total_shot = int(gongfang_div[0].xpath('div').xpath('div')[0].xpath('text()').extract()[0]) + int(gongfang_div[1].xpath('div').xpath('div')[0].xpath('text()').extract()[0])
            total_was_shoted = int(gongfang_div[0].xpath('div').xpath('div')[2].xpath('text()').extract()[0]) + int(gongfang_div[1].xpath('div').xpath('div')[2].xpath('text()').extract()[0])
        else:
            total_shot = int(gongfang_div[0].xpath('div').xpath('div')[2].xpath('text()').extract()[0]) + int(gongfang_div[1].xpath('div').xpath('div')[2].xpath('text()').extract()[0])
            total_was_shoted = int(gongfang_div[0].xpath('div').xpath('div')[0].xpath('text()').extract()[0]) + int(gongfang_div[1].xpath('div').xpath('div')[0].xpath('text()').extract()[0])

        single_item = shotRateItem()
        single_item['danchang_code'] = danchang_code
        single_item['zhu_ke_index'] = zhu_ke_index
        single_item['match_id'] = match_id
        single_item['league_name'] = league_name
        single_item['match_time'] = match_time
        single_item['home_id'] = home_id
        single_item['away_id'] = away_id
        single_item['home_name'] = home_name
        single_item['away_name'] = away_name
        single_item['cur_score'] = cur_score
        single_item['cur_lose_score'] = cur_lose_score
        single_item['total_shot'] = total_shot
        single_item['total_was_shoted'] = total_was_shoted
        yield single_item


