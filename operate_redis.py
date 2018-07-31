#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6381)
r = redis.Redis(connection_pool=pool)

year_start = 2010
url_arr = [
    'https://www.transfermarkt.com/championship/marktwerteverein/wettbewerb/GB2/plus/?stichtag=',
    'https://www.transfermarkt.com/league-one/marktwerteverein/wettbewerb/GB3/plus/?stichtag=',
    'https://www.transfermarkt.com/league-two/marktwerteverein/wettbewerb/GB4/plus/?stichtag=',
    'https://www.transfermarkt.com/laliga/marktwerteverein/wettbewerb/ES1/plus/?stichtag=',
    'https://www.transfermarkt.com/laliga2/marktwerteverein/wettbewerb/ES2/plus/?stichtag=',
    'https://www.transfermarkt.com/ligue-1/marktwerteverein/wettbewerb/FR1/plus/?stichtag=',
    'https://www.transfermarkt.com/ligue-2/marktwerteverein/wettbewerb/FR2/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-a/marktwerteverein/wettbewerb/IT1/plus/?stichtag=',
    'https://www.transfermarkt.com/serie-b/marktwerteverein/wettbewerb/IT2/plus/?stichtag=',
    'https://www.transfermarkt.com/1-bundesliga/marktwerteverein/wettbewerb/L1/plus/?stichtag=',
    'https://www.transfermarkt.com/2-bundesliga/marktwerteverein/wettbewerb/L2/plus/?stichtag=',
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

