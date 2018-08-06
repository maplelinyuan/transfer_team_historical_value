#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 获取历史身价信息
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6381)
r = redis.Redis(connection_pool=pool)

year_start = 2010
url_arr = [
    'https://www.transfermarkt.com/liga-1/marktwerteverein/wettbewerb/RO1/plus/?stichtag=',
    'https://www.transfermarkt.com/liga-2/marktwerteverein/wettbewerb/RO2/plus/?stichtag=',
    'https://www.transfermarkt.com/1-hnl/marktwerteverein/wettbewerb/KR1/plus/?stichtag=',
    'https://www.transfermarkt.com/2-hnl/marktwerteverein/wettbewerb/KR2/plus/?stichtag=',
    'https://www.transfermarkt.com/superliga/marktwerteverein/wettbewerb/SER1/plus/?stichtag=',
    'https://www.transfermarkt.com/prva-liga/marktwerteverein/wettbewerb/SER2/plus/?stichtag=',
    'https://www.transfermarkt.com/ligat-haal/marktwerteverein/wettbewerb/ISR1/plus/?stichtag=',
    'https://www.transfermarkt.com/liga-leumit/marktwerteverein/wettbewerb/ISR2/plus/?stichtag=',
    'https://www.transfermarkt.com/parva-liga/marktwerteverein/wettbewerb/BU1/plus/?stichtag=',
    'https://www.transfermarkt.com/vtora-liga/marktwerteverein/wettbewerb/BU2/plus/?stichtag=',
    'https://www.transfermarkt.com/primera-division/marktwerteverein/wettbewerb/AR1N/plus/?stichtag=',
    'https://www.transfermarkt.com/primera-b-nacional/marktwerteverein/wettbewerb/ARG2/plus/?stichtag=',
    'https://www.transfermarkt.com/liga-mx-apertura/marktwerteverein/wettbewerb/MEXA/plus/?stichtag=',
    'https://www.transfermarkt.com/ascenso-mx-apertura/marktwerteverein/wettbewerb/MEXB/plus/?stichtag=',
    'https://www.transfermarkt.com/campeonato-brasileiro-serie-a/marktwerteverein/wettbewerb/BRA1/plus/?stichtag=',
    'https://www.transfermarkt.com/campeonato-brasileiro-serie-b/marktwerteverein/wettbewerb/BRA2/plus/?stichtag=',
    'https://www.transfermarkt.com/major-league-soccer/marktwerteverein/wettbewerb/MLS1/plus/?stichtag=',
    'https://www.transfermarkt.com/united-soccer-league/marktwerteverein/wettbewerb/USL/plus/?stichtag=',

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

