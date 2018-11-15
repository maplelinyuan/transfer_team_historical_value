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
    'http://dongqiudi.com/match?tab=64',
]

class dongqiudi_player:
    def __init__(self):
        try:
            self.mongo_client = MongoClient(host='localhost', port=27019)
            db_name = 'player_analysis'
            db = self.mongo_client[db_name]  # 获得数据库的句柄
            col_name = 'dongqiudi_player'
            self.coll = db[col_name]  # 获得collection的句柄

            self.service_args = []
            self.service_args.append('--load-images=no')
            self.service_args.append('--dick-cache=yes')
            self.service_args.append('--ignore-ssl-errors=true')
            self.chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            self.dcap = dict(DesiredCapabilities.PHANTOMJS)

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))

    def for_match_list(self, driver, match_list):
        for match in match_list:
            tds = match.find_elements_by_xpath('td')
            if len(tds) > 5:
                cur_location = match.location
                driver.execute_script("window.scrollTo(0,%s)" % str(cur_location['y'] - 180))  # 持续滚动
                state = tds[0].text
                if state == '完场' or '':
                    continue
                match_id = match.get_attribute('rel').strip()
                league_name = tds[1].text.strip()
                home_name = tds[2].text.strip()
                score = tds[3].text.strip()
                away_name = tds[4].text.strip()
                home_detail_href = tds[2].find_elements_by_xpath('a')[0].get_attribute('href')
                away_detail_href = tds[4].find_elements_by_xpath('a')[0].get_attribute('href')
                newwindow = 'window.open("%s");' % home_detail_href
                driver.execute_script(newwindow)
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 进球数据
                home_total_goal = 0
                home_inc = 0
                home_arr = []
                away_total_goal = 0
                away_inc = 0
                away_arr = []
                # 切换到主队详情页面
                sub_list = driver.find_elements_by_xpath('//table[@class="teammates_list"]/tbody/tr')
                for player in sub_list:
                    cur_player_location = player.location
                    driver.execute_script("window.scrollTo(0,%s)" % str(cur_player_location['y'] - 180))  # 持续滚动
                    sub_tds = player.find_elements_by_xpath('td')
                    if len(sub_tds) > 5:
                        goal = sub_tds[4].text.strip()
                        if goal == '' or goal == '0' or goal == '-':
                            continue
                        goal = int(goal)
                        home_arr.append(goal)
                        home_total_goal += goal
                        home_inc += 1
                if home_inc > 1:
                    home_avg_goal = round(home_total_goal / home_inc, 3)
                    home_unbiased_variance = 0
                    for single_goal in home_arr:
                        home_unbiased_variance += pow(single_goal - home_avg_goal, 2)
                    home_unbiased_variance = round((home_unbiased_variance / (home_inc - 1)), 2)
                    # print('总进球：%s' % total_goal)
                    # print('平均进球：%s' % round((total_goal / inc), 2)
                    # print('进球方差：%s' % unbiased_variance)
                else:
                    # print('人数不足！')
                    home_unbiased_variance = -1
                driver.close()  # 关闭主队详情页面
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                newwindow = 'window.open("%s");' % away_detail_href
                driver.execute_script(newwindow)
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 开启客队详情
                sub_list = driver.find_elements_by_xpath('//table[@class="teammates_list"]/tbody/tr')
                for player in sub_list:
                    cur_player_location = player.location
                    driver.execute_script("window.scrollTo(0,%s)" % str(cur_player_location['y'] - 180))  # 持续滚动
                    sub_tds = player.find_elements_by_xpath('td')
                    if len(sub_tds) > 5:
                        goal = sub_tds[4].text.strip()
                        if goal == '' or goal == '0' or goal == '-':
                            continue
                        goal = int(goal)
                        away_arr.append(goal)
                        away_total_goal += goal
                        away_inc += 1
                if away_inc > 1:
                    away_avg_goal = round(away_total_goal / away_inc, 3)
                    away_unbiased_variance = 0
                    for single_goal in away_arr:
                        away_unbiased_variance += pow(single_goal - away_avg_goal, 2)
                    away_unbiased_variance = round((away_unbiased_variance / (away_inc - 1)), 2)
                    # print('总进球：%s' % total_goal)
                    # print('平均进球：%s' % round((total_goal / inc), 2)
                    # print('进球方差：%s' % unbiased_variance)
                else:
                    # print('人数不足！')
                    away_unbiased_variance = -1
                # 关闭客队详情，切换到主页面进行下一次循环
                driver.close()
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 判断支持方向
                if home_unbiased_variance < 0 or away_unbiased_variance < 0:
                    support_direction = ''
                else:
                    if (away_total_goal >= home_total_goal) and (away_unbiased_variance < home_unbiased_variance):
                        support_direction = '0'
                    elif (home_total_goal >= away_total_goal) and (home_unbiased_variance < away_unbiased_variance):
                        support_direction = '3'
                    else:
                        support_direction = ''
                # 存储该场次数据
                if not self.coll.find({'match_id': match_id}).count() > 0:
                    insertItem = dict(match_id=match_id, league_name=league_name, home_name=home_name,
                                      away_name=away_name, score=score, state=state,
                                      home_total_goal=home_total_goal, home_unbiased_variance=home_unbiased_variance,
                                      away_total_goal=away_total_goal, away_unbiased_variance=away_unbiased_variance,
                                      support_direction=support_direction,
                                      )
                    self.coll.insert(insertItem)
                else:
                    updateItem = dict(score=score, state=state)
                    self.coll.update({"match_id": match_id},
                                     {'$set': updateItem})

    def run(self):
        try:
            for give_me_url in url_arr:
                driver = webdriver.Chrome(chrome_options=self.chrome_options, desired_capabilities=self.dcap,
                                          service_args=self.service_args)
                driver.implicitly_wait(20)
                driver.set_page_load_timeout(30)
                # driver.set_window_size(1024, 768)  # 分辨率 1024*768
                driver.get(give_me_url)

                # 悬停
                match_list = driver.find_elements_by_xpath('//div[@id="match_info"]/table/tbody/tr')
                self.for_match_list(driver, match_list)
                match_tables = driver.find_elements_by_xpath('//div[@id="match_info"]/table')
                if len(match_tables) > 1:
                    match_list = match_tables[1].find_elements_by_xpath('tbody/tr')
                self.for_match_list(driver, match_list)
                # 关闭窗口
                driver.quit()
        finally:
            self.mongo_client.close()

if __name__ == '__main__':
    app = dongqiudi_player()
    app.run()




