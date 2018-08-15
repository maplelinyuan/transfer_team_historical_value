# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 历史身价
class TransferCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    current_time = scrapy.Field()
    name = scrapy.Field()
    value = scrapy.Field()

# 实时身价
class realTimeMktlItem(scrapy.Item):
    # define the fields for your item here like:
    update_time = scrapy.Field()
    name = scrapy.Field()
    value = scrapy.Field()

# 实时比赛
class realTimeMatchlItem(scrapy.Item):
    # define the fields for your item here like:
    qi_shu = scrapy.Field()
    match_id = scrapy.Field()
    league_name = scrapy.Field()
    match_time = scrapy.Field()
    home_name = scrapy.Field()
    away_name = scrapy.Field()
    home_odd = scrapy.Field()
    draw_odd = scrapy.Field()
    away_odd = scrapy.Field()
    home_goal = scrapy.Field()
    away_goal = scrapy.Field()

