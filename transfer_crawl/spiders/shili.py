# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import shiliItem
from scrapy_splash import SplashRequest
from transfer_crawl.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time, datetime

# scrapy crawl shili
# class ShiliSpider(scrapy.Spider):
class ShiliSpider(RedisSpider):
    name = 'shili'
    allowed_domains = ['http://live.500.com']
    start_urls = []
    redis_key = 'shili:start_urls'

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
            home_id = tds[5].xpath('a/@href').extract()[0].split('/')[-2]
            if len(tds[6].xpath('div/a/text()').extract()) == 3:
                home_goal = tds[6].xpath('div/a/text()').extract()[0].strip()
                away_goal = tds[6].xpath('div/a/text()').extract()[2].strip()
                if home_goal.isdigit():
                    home_goal = int(home_goal)
                else:
                    home_goal = ''
                if away_goal.isdigit():
                    away_goal = int(away_goal)
                else:
                    away_goal = ''
            else:
                home_goal = ''
                away_goal = ''
            away_name = tds[7].xpath('a/text()').extract()[0].strip()
            away_id = tds[7].xpath('a/@href').extract()[0].split('/')[-2]
            if league_name == '乌克兰超':
                league_name = '乌超'
            if league_name == '波兰甲':
                league_name = '波甲'
            if league_name == '捷克甲':
                league_name = '捷甲'

            current_info = dict(league_name=league_name, qi_shu=qi_shu, match_id=match_id, match_time=match_time, home_id=home_id, away_id=away_id, home_name=home_name, away_name=away_name, home_goal=home_goal, away_goal=away_goal)

            match_detail_href = 'http://odds.500.com/fenxi/shuju-%s.shtml' % match_id.split('a')[1]
            yield scrapy.Request(match_detail_href, self.detail_info_parse, meta=current_info, dont_filter=True)


    def detail_info_parse(self, response):
        qi_shu = response.meta['qi_shu']
        league_name = response.meta['league_name']
        match_id = response.meta['match_id']
        match_time = response.meta['match_time']
        home_name = response.meta['home_name']
        away_name = response.meta['away_name']
        home_id = response.meta['home_id']
        away_id = response.meta['away_id']
        home_goal = response.meta['home_goal']
        away_goal = response.meta['away_goal']

        # 特殊情况
        if len(response.xpath('//div[@id="team_jiaozhan"]/div/span/span')) == 0:
            return False
        if len(response.xpath('//form[@id="zhanji_01"]').xpath('div[@class="M_content"]')[0].xpath('table/tbody/tr')[2].xpath('td')[-2].xpath('span/text()')) == 0:
            return False
        if len(response.xpath('//form[@id="zhanji_00"]').xpath('div[@class="M_content"]')[0].xpath('table/tbody/tr')[2].xpath('td')[-2].xpath('span/text()')) == 0:
            return False
        try:
            jiaozhan_em = response.xpath('//div[@id="team_jiaozhan"]/div/span/span')[1].xpath('em')
            win_number = int(jiaozhan_em[0].xpath('text()').extract()[0].split('胜')[0])
            draw_number = int(jiaozhan_em[1].xpath('text()').extract()[0].split('平')[0])
            away_number = int(jiaozhan_em[2].xpath('text()').extract()[0].split('负')[0])
            home_panlu = response.xpath('//form[@id="zhanji_01"]').xpath('div[@class="M_content"]')[0].xpath('table/tbody/tr')[2].xpath('td')[-2].xpath('span/text()').extract()[0]   # str 无为'-', 否则为输或赢
            away_panlu = response.xpath('//form[@id="zhanji_00"]').xpath('div[@class="M_content"]')[0].xpath('table/tbody/tr')[2].xpath('td')[-2].xpath('span/text()').extract()[0]   # str 无为'-', 否则为输或赢
            support_direction = judge_result(win_number, draw_number, away_number, home_panlu, away_panlu)

        except Exception as err:
            print(err)
            pdb.set_trace()


        single_item = shiliItem()
        single_item['qi_shu'] = qi_shu
        single_item['match_id'] = match_id
        single_item['league_name'] = league_name
        single_item['match_time'] = match_time
        single_item['home_id'] = home_id
        single_item['away_id'] = away_id
        single_item['home_name'] = home_name
        single_item['away_name'] = away_name
        single_item['home_goal'] = home_goal
        single_item['away_goal'] = away_goal
        single_item['support_direction'] = support_direction
        yield single_item

def sum_arr(lishi_arr):
    sum = 0
    for ele in lishi_arr:
        sum += ele
    return sum

def sure_index_str(index):
    if index < 0:
        index = 0
    elif index > 2:
        index = 2

    index_arr = ['胜', '平', '负']
    return index_arr[index]

def panlu_str2num(str):
    if str == '赢':
        return 3
    elif str == '走':
        return 1
    else:
        return 0


def judge_result(win_number, draw_number, away_number, home_panlu, away_panlu):
    if home_panlu == '-' or away_panlu == '-' or (win_number == 0 and draw_number == 0 and away_number == 0):
        return ''

    home_panlu = panlu_str2num(home_panlu)
    away_panlu = panlu_str2num(away_panlu)

    support_result = ''

    lishi_arr = [0, 0, 0]
    if win_number > 0:
        lishi_arr[0] = 1
    if draw_number == win_number and lishi_arr[0] == 1:
        lishi_arr[1] = 1
    if draw_number > win_number:
        lishi_arr[0] = 0
        lishi_arr[1] = 1
    if away_number == win_number and lishi_arr[0] == 1:
        lishi_arr[2] = 1
    if away_number == draw_number and lishi_arr[1] == 1:
        lishi_arr[2] = 1
    if away_number > win_number:
        lishi_arr[0] = 0
        lishi_arr[2] = 1
    if away_number > draw_number:
        lishi_arr[1] = 0
        lishi_arr[2] = 1


    if home_panlu == away_panlu:
        if sum_arr(lishi_arr) == 1:
            lishi_index = lishi_arr.index(1)
            support_direction = sure_index_str(lishi_index)
        else:
            return ''
    elif home_panlu > away_panlu:
        lishi_index = lishi_arr.index(1)
        support_direction = sure_index_str(lishi_index-1)
    else:
        lishi_index = lishi_arr.index(1)
        support_direction = sure_index_str(lishi_index + 1)

    return support_direction
