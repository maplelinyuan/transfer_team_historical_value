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

# 被限制，无法使用

# use_proxy = False    # splash 是否使用代理 d: proxy_tool

# scrapy crawl dongqiudi_player
# class DongqiudiPlayerSpider(scrapy.Spider):
class DongqiudiPlayerSpider(RedisSpider):
    name = 'dongqiudi_player'
    allowed_domains = ['http://dongqiudi.com/']
    start_urls = []
    redis_key = 'realtime_matchs:dongqiudi_player'

    # global splashurl
    # splashurl = "http://192.168.99.100:8050/render.html"

    # 此处是重父类方法，并使把url传给splash解析
    # def make_requests_from_url(self, url):
    #     global splashurl
    #     url = splashurl + "?url=" + url
    #     # 使用代理访问
    #     proxy = MyTools.get_proxy()
    #     LUA_SCRIPT = """
    #                                 function main(splash)
    #                                     splash:on_request(function(request)
    #                                         request:set_proxy{
    #                                             host = "%(host)s",
    #                                             port = %(port)s,
    #                                             username = '', password = '', type = "HTTPS",
    #                                         }
    #                                         request:set_header('X-Forwarded-For', %(proxy_ip)s)
    #                                     end)
    #                                     assert(splash:go(args.url))
    #                                     assert(splash:wait(1))
    #                                     return {
    #                                         html = splash:html(),
    #                                     }
    #                                 end
    #                                 """
    #     try:
    #         if use_proxy:
    #             proxy_host = proxy.strip().split(':')[0]
    #             proxy_port = int(proxy.strip().split(':')[-1])
    #             LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
    #             print('make_requests代理为：', "http://{}".format(proxy))
    #             return SplashRequest(url, self.parse,
    #                                  args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
    #                                  dont_filter=True)
    #         else:
    #             LUA_SCRIPT = """
    #                                                 function main(splash)
    #                                                     assert(splash:go(args.url))
    #                                                     assert(splash:wait(1))
    #                                                     return {
    #                                                         html = splash:html(),
    #                                                     }
    #                                                 end
    #                                                 """
    #             return SplashRequest(url, self.parse,
    #                                  args={'wait': 0.5, 'images': 0, 'timeout': 30,  'lua_source': LUA_SCRIPT},
    #                                  dont_filter=True)
    #     except Exception as err:
    #         MyTools.delete_proxy(proxy)
    #         print('%s\n%s' % (err, traceback.format_exc()))
    #
    # def start_requests(self):
    #     for url in self.start_urls:
    #         proxy = MyTools.get_proxy()
    #
    #         LUA_SCRIPT = """
    #                                     function main(splash)
    #                                         splash:on_request(function(request)
    #                                             request:set_proxy{
    #                                                 host = "%(host)s",
    #                                                 port = %(port)s,
    #                                                 username = '', password = '', type = "HTTPS",
    #                                             }
    #                                             request:set_header('X-Forwarded-For', %(proxy_ip)s)
    #                                         end)
    #                                         assert(splash:go(args.url))
    #                                         assert(splash:wait(1))
    #                                         return {
    #                                             html = splash:html(),
    #                                         }
    #                                     end
    #                                     """
    #         if use_proxy:
    #             proxy_host = proxy.strip().split(':')[0]
    #             proxy_port = int(proxy.strip().split(':')[-1])
    #             LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
    #             try:
    #                 yield SplashRequest(url, self.parse,
    #                                     args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
    #                                     dont_filter=True)
    #             except Exception as err:
    #                 print('%s\n%s' % (err, traceback.format_exc()))
    #         else:
    #             LUA_SCRIPT = """
    #                                                                 function main(splash)
    #                                                                     assert(splash:go(args.url))
    #                                                                     assert(splash:wait(1))
    #                                                                     return {
    #                                                                         html = splash:html(),
    #                                                                     }
    #                                                                 end
    #                                                                 """
    #             yield SplashRequest(url, self.parse,
    #                                 args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
    #                                 dont_filter=True)
    #
    # '''
    #     redis中存储的为set类型的公司名称，使用SplashRequest去请求网页。
    #     注意：不能在make_request_from_data方法中直接使用SplashRequest（其他第三方的也不支持）,会导致方法无法执行，也不抛出异常
    #     但是同时重写make_request_from_data和make_requests_from_url方法则可以执行
    # '''
    #
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        trs = response.xpath('//div[@id="match_info"]/table/tbody/tr')
        for tr in trs:
            tds = tr.xpath('td')
            if len(tds) < 6:
                continue
            state = tds[0].xpath('text()').extract()[0].strip()
            if len(tds[0].xpath('p')) > 0:
                is_playing = 1  # 比赛正在进行
                continue
            else:
                is_playing = 0
            match_id = tr.xpath('[@rel]').extract()[0].strip()
            league_name = tds[1].xpath('text()').extract()[0].strip()
            home_name = tds[2].xpath('a/text()').extract()[0].strip()
            score = tds[2].xpath('text()').extract()[0].strip()
            away_name = tds[4].xpath('a/text()').extract()[0].strip()
            if state == '完场':
                cur_state = 0
                single_item = realTimeMktlItem()
                single_item['cur_state'] = cur_state
                single_item['match_id'] = match_id
                single_item['league_name'] = league_name
                single_item['home_name'] = home_name
                single_item['away_name'] = away_name
                single_item['score'] = score
                yield single_item
            else:
                cur_state = 1
                current_info_home = dict(cur_team=0, cur_state=cur_state, match_id=match_id, league_name=league_name, home_name=home_name,
                                    away_name=away_name, score=score
                                    )
                current_info_away = dict(cur_team=1, cur_state=cur_state, match_id=match_id, league_name=league_name,
                                         home_name=home_name,
                                         away_name=away_name, score=score
                                         )
                home_team_detail_href = 'http://dongqiudi.com%s' % tds[2].xpath('a/[@href]').extract()[0].strip()
                away_team_detail_href = 'http://dongqiudi.com%s' % tds[4].xpath('a/[@href]').extract()[0].strip()
                yield scrapy.Request(home_team_detail_href, self.detail_info_parse, meta=current_info_home, dont_filter=True)
                yield scrapy.Request(away_team_detail_href, self.detail_info_parse, meta=current_info_away, dont_filter=True)
    def detail_info_parse(self, response):
        cur_team = response.meta['cur_team']
        cur_state = response.meta['cur_state']
        match_id = response.meta['match_id']
        league_name = response.meta['league_name']
        home_name = response.meta['home_name']
        away_name = response.meta['away_name']
        score = response.meta['score']
        try:
            total_goal = 0
            inc = 0
            arr = []
            trs = response.xpath('//table[@class="teammates_list"]/tbody/tr')
            for tr in trs:
                tds = tr.xpath('td')
                if len(tds) > 5:
                    goal = tds[4].xpath('text()').extract()[0].strip()
                    if goal == '' or goal == '0' or goal == '-':
                        continue
                    goal = int(goal)
                    arr.append(goal)
                    total_goal += goal
                    inc += 1
            avg_goal = round(total_goal / inc, 3)
            unbiased_variance = 0
            for single in arr:
                unbiased_variance += pow(single - avg_goal, 2)
            if inc > 1:
                unbiased_variance = round((unbiased_variance / (inc - 1)), 2)
                # print('总进球：%s' % total_goal)
                # print('平均进球：%s' % round((total_goal / inc), 2)
                # print('进球方差：%s' % unbiased_variance)
            else:
                # print('人数不足！')
                unbiased_variance = -1

            single_item = realTimeMktlItem()
            single_item['cur_team'] = cur_team
            single_item['cur_state'] = cur_state
            single_item['match_id'] = match_id
            single_item['league_name'] = league_name
            single_item['home_name'] = home_name
            single_item['away_name'] = away_name
            single_item['score'] = score
            single_item['total_goal'] = total_goal
            single_item['unbiased_variance'] = unbiased_variance
            yield single_item
        except Exception as err:
            print(err)
            return False