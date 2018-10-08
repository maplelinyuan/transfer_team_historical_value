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
    home_id = scrapy.Field()
    away_id = scrapy.Field()
    home_name = scrapy.Field()
    away_name = scrapy.Field()
    home_odd = scrapy.Field()
    draw_odd = scrapy.Field()
    away_odd = scrapy.Field()
    home_goal = scrapy.Field()
    away_goal = scrapy.Field()
    home_origin_lisan = scrapy.Field()
    draw_origin_lisan = scrapy.Field()
    away_origin_lisan = scrapy.Field()
    home_lisan = scrapy.Field()
    draw_lisan = scrapy.Field()
    away_lisan = scrapy.Field()

# shili
class shiliItem(scrapy.Item):
    # define the fields for your item here like:
    qi_shu = scrapy.Field()
    match_id = scrapy.Field()
    league_name = scrapy.Field()
    match_time = scrapy.Field()
    home_id = scrapy.Field()
    away_id = scrapy.Field()
    home_name = scrapy.Field()
    away_name = scrapy.Field()
    home_goal = scrapy.Field()
    away_goal = scrapy.Field()
    support_direction = scrapy.Field()

# shot_rate
class shotRateItem(scrapy.Item):
    # define the fields for your item here like:
    danchang_code = scrapy.Field()
    zhu_ke_index = scrapy.Field()
    match_id = scrapy.Field()
    league_name = scrapy.Field()
    match_time = scrapy.Field()
    home_id = scrapy.Field()
    away_id = scrapy.Field()
    home_name = scrapy.Field()
    away_name = scrapy.Field()
    cur_score = scrapy.Field()
    cur_lose_score = scrapy.Field()
    total_shot = scrapy.Field()
    total_was_shoted = scrapy.Field()

# ID对应英文名
class idMapEnglish(scrapy.Item):
    # define the fields for your item here like:
    team_id = scrapy.Field()
    english_name = scrapy.Field()

