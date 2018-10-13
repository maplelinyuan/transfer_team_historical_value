# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import lisanRatelItem
from scrapy_splash import SplashRequest
from transfer_crawl.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time, datetime

# scrapy crawl lisan_rate
# class lisanRateSpider(scrapy.Spider):
class lisanRateSpider(RedisSpider):
    name = 'lisan_rate'
    allowed_domains = ['http://live.500.com']
    start_urls = []
    redis_key = 'lisan_rate:start_urls'
    if_open_local_crawl = True

    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'market_value'
    db = mongo_client[db_name]  # 获得数据库的句柄
    open_limit_danchang_matchs = True   # 是否限制为单场比赛


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        danchang_col_name = 'new_realtime_matchs'
        danchang_col = self.db[danchang_col_name]  # 获得collection的句柄
        qi_shu = danchang_col.find().sort([('qi_shu', -1)])[0]['qi_shu']
        danchang_league_name_arr = []
        for danchang_single in danchang_col.find({'qi_shu': qi_shu}):
            danchang_single_name = danchang_single['league_name']
            if danchang_single_name not in danchang_league_name_arr:
                danchang_league_name_arr.append(danchang_single_name)

        trs = response.xpath('//div[@class="right"]/table/tr')
        after_match_date = ''   # 后面比赛的日期 e: 2018-10-09
        for tr in trs:
            if len(tr.xpath('td')) == 1:    # 当前是日期行
                after_match_date = tr.xpath('td')[0].xpath('text()').extract()[0].split('(')[0]
            if len(tr.xpath('td')) < 13:
                continue
            tds = tr.xpath('td')
            match_id = tds[-1].xpath('a')[0].xpath('@href').extract()[0].split('-')[-1].split('.')[0]
            league_name = tds[1].xpath('a/font/text()').extract()[0]
            league_name_dict = {
                '巴乙': '巴西乙',
                '巴甲': '巴西甲',
                '美职联': '美职',
                '苏冠': '苏甲',
            }
            if league_name in league_name_dict.keys():
                league_name = league_name_dict[league_name]
            # 限制为单场比赛跳过其余
            if self.open_limit_danchang_matchs:
                if league_name not in danchang_league_name_arr:
                    continue

            tr_time = tds[0].xpath('text()').extract()[0].strip()
            match_time = after_match_date + ' ' + tr_time

            match_time_stamp = time.mktime(time.strptime(match_time, "%Y-%m-%d %H:%M"))
            time_now = int(time.time())
            time_interval = time_now - match_time_stamp

            # 如果开启局部爬取，就只爬取未开赛半个小时内和开赛后2小时内的比赛
            if self.if_open_local_crawl and (time_interval > 7200 or time_interval < -1800):
                continue

            home_name = tds[2].xpath('a/text()').extract()[0].strip()
            home_id = tds[2].xpath('a/@href').extract()[0].split('/')[-2]
            away_name = tds[3].xpath('a/text()').extract()[0].strip()
            away_id = tds[3].xpath('a/@href').extract()[0].split('/')[-2]
            pinnacle_home_odd = float(tds[4].xpath('text()').extract()[0])
            pinnacle_draw_odd = float(tds[5].xpath('text()').extract()[0])
            pinnacle_away_odd = float(tds[6].xpath('text()').extract()[0])

            current_info = dict(league_name=league_name, match_id=match_id, match_time=match_time, home_id=home_id, away_id=away_id, home_name=home_name, away_name=away_name,
            pinnacle_home_odd=pinnacle_home_odd, pinnacle_draw_odd=pinnacle_draw_odd, pinnacle_away_odd=pinnacle_away_odd)

            match_detail_href = 'http://odds.500.com/fenxi/ouzhi-%s.shtml' % match_id
            yield scrapy.Request(match_detail_href, self.detail_info_parse, meta=current_info, dont_filter=True)


    def detail_info_parse(self, response):
        league_name = response.meta['league_name']
        match_id = response.meta['match_id']
        match_time = response.meta['match_time']
        home_name = response.meta['home_name']
        away_name = response.meta['away_name']
        home_id = response.meta['home_id']
        away_id = response.meta['away_id']
        pinnacle_home_odd = response.meta['pinnacle_home_odd']
        pinnacle_draw_odd = response.meta['pinnacle_draw_odd']
        pinnacle_away_odd = response.meta['pinnacle_away_odd']
        # 获取得分
        score = response.xpath('//div[@class="odds_header"]/div/table/tbody/tr/td')[2].xpath('div/p')[1].xpath('strong/text()').extract()[0]
        if score == 'VS':
            home_goal = ''
            away_goal = ''
        else:
            home_goal = int(score.split(':')[0])
            away_goal = int(score.split(':')[1])

        total_table = response.xpath('//div[@id="table_btm"]')

        home_origin_lisan = float(total_table[0].xpath('table/tr')[3].xpath('td')[1].xpath('table')[0].xpath('tbody/tr')[0].xpath('td')[0].xpath('text()').extract()[0])
        draw_origin_lisan = float(total_table[0].xpath('table/tr')[3].xpath('td')[1].xpath('table')[0].xpath('tbody/tr')[0].xpath('td')[1].xpath('text()').extract()[0])
        away_origin_lisan = float(total_table[0].xpath('table/tr')[3].xpath('td')[1].xpath('table')[0].xpath('tbody/tr')[0].xpath('td')[2].xpath('text()').extract()[0])
        home_lisan = float(total_table[0].xpath('table/tr')[3].xpath('td')[1].xpath('table')[0].xpath('tbody/tr')[1].xpath('td')[0].xpath('text()').extract()[0])
        draw_lisan = float(total_table[0].xpath('table/tr')[3].xpath('td')[1].xpath('table')[0].xpath('tbody/tr')[1].xpath('td')[1].xpath('text()').extract()[0])
        away_lisan = float(total_table[0].xpath('table/tr')[3].xpath('td')[1].xpath('table')[0].xpath('tbody/tr')[1].xpath('td')[2].xpath('text()').extract()[0])

        single_item = lisanRatelItem()
        single_item['match_id'] = match_id
        single_item['league_name'] = league_name
        single_item['match_time'] = match_time
        single_item['home_id'] = home_id
        single_item['away_id'] = away_id
        single_item['home_name'] = home_name
        single_item['away_name'] = away_name
        single_item['home_goal'] = home_goal
        single_item['away_goal'] = away_goal
        single_item['pinnacle_home_odd'] = pinnacle_home_odd
        single_item['pinnacle_draw_odd'] = pinnacle_draw_odd
        single_item['pinnacle_away_odd'] = pinnacle_away_odd
        single_item['home_origin_lisan'] = home_origin_lisan
        single_item['draw_origin_lisan'] = draw_origin_lisan
        single_item['away_origin_lisan'] = away_origin_lisan
        single_item['home_lisan'] = home_lisan
        single_item['draw_lisan'] = draw_lisan
        single_item['away_lisan'] = away_lisan
        yield single_item
