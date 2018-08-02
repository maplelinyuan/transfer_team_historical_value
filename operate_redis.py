#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 获取历史身价信息
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6381)
r = redis.Redis(connection_pool=pool)

year_start = 2010
url_arr = [
    'https://www.transfermarkt.com/national-league/marktwerteverein/wettbewerb/CNAT/plus/?stichtag=',
    'https://www.transfermarkt.com/segunda-division-b-grupo-i/marktwerteverein/wettbewerb/ES3A/plus/?stichtag=',
    'https://www.transfermarkt.com/segunda-division-b-grupo-ii/marktwerteverein/wettbewerb/ES3B/plus/?stichtag=',
    'https://www.transfermarkt.com/segunda-division-b-grupo-iii/marktwerteverein/wettbewerb/ES3C/plus/?stichtag=',
    'https://www.transfermarkt.com/segunda-division-b-grupo-iv/marktwerteverein/wettbewerb/ES3D/plus/?stichtag=',
    'https://www.transfermarkt.com/championnat-national/marktwerteverein/wettbewerb/FR3/plus/?stichtag=',
    'https://www.transfermarkt.com/3-liga/marktwerteverein/wettbewerb/L3/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-c-girone-a/marktwerteverein/wettbewerb/IT3A/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-c-girone-b/marktwerteverein/wettbewerb/IT3B/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-c-girone-c/marktwerteverein/wettbewerb/IT3C/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-d-girone-a/marktwerteverein/wettbewerb/IT4A/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-d-girone-d/marktwerteverein/wettbewerb/IT4D/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-d-girone-g/marktwerteverein/wettbewerb/IT4G/plus/?stichtag=',
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

