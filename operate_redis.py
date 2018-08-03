#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 获取历史身价信息
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6381)
r = redis.Redis(connection_pool=pool)

year_start = 2010
url_arr = [
    'https://www.transfermarkt.com/lotto-ekstraklasa/marktwerteverein/wettbewerb/PL1/plus/?stichtag=',
    'https://www.transfermarkt.com/fortuna-1-liga/marktwerteverein/wettbewerb/PL2/plus/?stichtag=',
    'https://www.transfermarkt.com/2-liga/marktwerteverein/wettbewerb/PL2L/plus/?stichtag=',
    'https://www.transfermarkt.com/het-liga/marktwerteverein/wettbewerb/TS1/plus/?stichtag=',
    'https://www.transfermarkt.com/fotbalova-narodni-liga/marktwerteverein/wettbewerb/TS2/plus/?stichtag=',
]
year_end = 2018
current_day = ''
for year in range(year_start, year_end+1):
    for month in range(1, 13):
        if year == 2010 and month < 11:
            continue
        if year == year_end and month > 7:
            continue
        for day in ['01', '15']:
            current_day = str(year) + '-' + str(month) + '-' + day
            for url_first in url_arr:
                url = url_first + current_day
                r.rpush("transfermkt:start_urls", url)

