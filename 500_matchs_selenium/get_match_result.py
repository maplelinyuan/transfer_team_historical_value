# -*- coding:utf-8 -*-
from selenium import webdriver
# from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image, ImageEnhance
import pytesseract
import pdb, traceback
from pymongo import MongoClient
import os
import time
import redis
import json

def get_auth_code(driver, codeEelement):
    '''获取验证码'''
    driver.save_screenshot('login/login.png')  # 截取登录页面
    imgSize = codeEelement.size  # 获取验证码图片的大小
    imgLocation = codeEelement.location  # 获取验证码元素坐标
    rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
              int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
    login = Image.open("login/login.png")
    frame4 = login.crop(rangle)  # 截取验证码图片
    frame4.save('login/authcode.png')
    authcodeImg = Image.open('login/authcode.png')
    authCodeText = pytesseract.image_to_string(authcodeImg).strip()
    return authCodeText


# 需要修改的url链接
# give_me_url = 'http://liansai.500.com/zuqiu-4843/'
url_arr = [
    'http://liansai.500.com/zuqiu-4897/',
]

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'market_value'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'match_results'
    coll = db[col_name]  # 获得collection的句柄

    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--dick-cache=yes')
    service_args.append('--ignore-ssl-errors=true')
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    dcap = dict(DesiredCapabilities.PHANTOMJS)

    for give_me_url in url_arr:
        driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=dcap, service_args=service_args)
        driver.implicitly_wait(20)
        driver.set_page_load_timeout(30)
        # driver.set_window_size(1024, 768)  # 分辨率 1024*768
        driver.get(give_me_url)

        league_name = driver.find_elements_by_xpath('//ul[@class="lpage_race_nav clearfix"]')[0].find_elements_by_xpath('li')[0].find_elements_by_xpath('a')[0].text.split('首页')[0]  # 联赛名称

        # 悬停
        season_div = driver.find_elements_by_xpath('//div[@id="seaon_list_div"]/div')
        chain = ActionChains(driver)
        chain.click_and_hold(season_div[0]).perform()
        time.sleep(2)
        season_list_len = len(season_div[1].find_elements_by_xpath('div/ul/li'))

        if league_name == '澳超':
            need_season_arr = ['2010/2011', '2011/2012', '2012/2013', '2013/2014']
        elif league_name == '葡甲':
            need_season_arr = ['2010/2011', '2011/2012', '2012/2013', '2013/2014']
        else:
            need_season_arr = ['2010/2011', '2011/2012', '2012/2013', '2013/2014', '2014/2015', '2015/2016', '2016/2017', '2017/2018']
        for season_index in range(season_list_len):
            time.sleep(2)
            season_div = driver.find_elements_by_xpath('//div[@id="seaon_list_div"]/div')
            season_list = season_div[1].find_elements_by_xpath('div/ul/li')

            season_a = season_list[season_index].find_elements_by_xpath('a')[0]
            season = season_a.text.split('赛季')[0]
            if not season in need_season_arr:
                continue
            season_a.click()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            click_complete_matchs = driver.find_element_by_id('season_match_round').find_elements_by_xpath('div')[0].find_elements_by_xpath('a')[0]
            click_complete_matchs.click()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])

            match_day_list = driver.find_elements_by_xpath('//ul[@id="match_group"]/li')
            match_day_total = len(match_day_list)
            for match_day_index in reversed(range(match_day_total)):
                time.sleep(2)
                # if(match_day_index != 0 and match_day_index in [46, 38, 31, 25,18,12, 5]):
                if(match_day_index != 0 and (match_day_total-match_day_index)%6==0):
                    # 点击左侧箭头
                    driver.find_elements_by_xpath('//div[@class="lsaiguo_round clearfix"]')[0].find_elements_by_xpath('a')[0].click()
                    time.sleep(2)
                match_day_list[match_day_index].click()
                time.sleep(3)
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                trs_len = len(driver.find_elements_by_xpath('//tbody[@id="match_list_tbody"]/tr'))
                for tr_index in range(trs_len):
                    current_tr = driver.find_elements_by_xpath('//tbody[@id="match_list_tbody"]/tr')[tr_index]
                    match_id = current_tr.get_attribute('data-fid')
                    match_time = current_tr.get_attribute('data-time')
                    try:
                        home_name = current_tr.find_elements_by_xpath('td')[2].find_elements_by_xpath('a')[0].get_attribute('title')
                        away_name = current_tr.find_elements_by_xpath('td')[4].find_elements_by_xpath('a')[0].get_attribute('title')
                        score_td = current_tr.find_elements_by_xpath('td')[3]
                        if len(current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')) < 3 or len(score_td.find_elements_by_xpath('span')) < 2:
                            continue
                        if len(current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')) < 3:
                            continue
                        home_odd = current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')[0].text
                        draw_odd = current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')[1].text
                        away_odd = current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')[2].text
                    except Exception as msg:
                        print("查找元素异常 %s" % msg)
                        print("重新查找元素")
                        current_tr = driver.find_elements_by_xpath('//tbody[@id="match_list_tbody"]/tr')[tr_index]
                        home_name = current_tr.find_elements_by_xpath('td')[2].find_elements_by_xpath('a')[0].get_attribute('title')
                        away_name = current_tr.find_elements_by_xpath('td')[4].find_elements_by_xpath('a')[0].get_attribute('title')
                        score_td = current_tr.find_elements_by_xpath('td')[3]
                        home_odd = current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')[0].text
                        draw_odd = current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')[1].text
                        away_odd = current_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('span')[2].text
                    if score_td.find_elements_by_xpath('span')[0].text == 'null':
                        continue
                    home_goal = int(score_td.find_elements_by_xpath('span')[0].text)
                    away_goal = int(score_td.find_elements_by_xpath('span')[1].text)
                    if home_goal > away_goal:
                        match_result = 3
                    elif home_goal == away_goal:
                        match_result = 1
                    else:
                        match_result = 0

                    insertItem = dict(
                        match_id=match_id,
                        match_time=match_time,
                        league_name=league_name,
                        home_name=home_name,
                        away_name=away_name,
                        home_goal=home_goal,
                        away_goal=away_goal,
                        match_result=match_result,
                        home_odd=home_odd,
                        draw_odd=draw_odd,
                        away_odd=away_odd,
                    )
                    if coll.find({'match_id': match_id}).count() == 0:
                        coll.insert(insertItem)

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.close()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.close()
            windows = driver.window_handles
            driver.switch_to.window(windows[0])

        # 关闭窗口
        driver.quit()

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()



