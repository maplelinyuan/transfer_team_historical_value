# -*- coding: utf-8 -*-
import scrapy
import pdb
from transfer_crawl.items import TransferCrawlItem
from scrapy_splash import SplashRequest
from transfer_crawl.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time
import redis

# scrapy crawl transfermkt
# class TransfermktSpider(scrapy.Spider):
class TransfermktSpider(RedisSpider):
    name = 'transfermkt'
    allowed_domains = ['http://www.transfermarkt.com/']
    start_urls = []
    redis_key = 'transfermkt:start_urls'
    # global splashurl
    # splashurl = "http://192.168.99.100:8050/render.html"
    #
    # # 此处是重父类方法，并使把url传给splash解析
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
    #         proxy_host = proxy.strip().split(':')[0]
    #         proxy_port = int(proxy.strip().split(':')[-1])
    #         LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
    #         print('make_requests代理为：', "http://{}".format(proxy))
    #         return SplashRequest(url, self.parse,
    #                              args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
    #                              dont_filter=True)
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
    #         proxy_host = proxy.strip().split(':')[0]
    #         proxy_port = int(proxy.strip().split(':')[-1])
    #         LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
    #         try:
    #             yield SplashRequest(url, self.parse,
    #                                 args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
    #                                 dont_filter=True)
    #         except Exception as err:
    #             print('%s\n%s' % (err, traceback.format_exc()))

    #
    # '''
    #     redis中存储的为set类型的公司名称，使用SplashRequest去请求网页。
    #     注意：不能在make_request_from_data方法中直接使用SplashRequest（其他第三方的也不支持）,会导致方法无法执行，也不抛出异常
    #     但是同时重写make_request_from_data和make_requests_from_url方法则可以执行
    # '''

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        current_time = response.url.split('=')[-1]
        trs = response.xpath('//div[@id="yw1"]/table/tbody/tr')
        for tr in trs:
            name = tr.xpath('td')[2].xpath('a/text()').extract()[0].strip()
            market_value = tr.xpath('td')[4].xpath('a/text()').extract()[0]
            if market_value == '-':
                continue
            value_unit = market_value.split(' ')[1].split('.')[0]
            if value_unit == 'Bill':
                value = int(market_value.split(' ')[0].replace(',', '')) * 10000000
            elif value_unit == 'Mill':
                value = int(market_value.split(' ')[0].replace(',', '')) * 10000
            else:
                value = int(market_value.split(' ')[0].replace(',', '')) * 1000
            single_item = TransferCrawlItem()
            single_item['current_time'] = current_time
            single_item['name'] = name
            single_item['value'] = value
            yield single_item