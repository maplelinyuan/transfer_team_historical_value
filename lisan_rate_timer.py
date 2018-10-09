#! /usr/bin/env python
# coding=utf-8
# 500网单场实时比赛爬取
import time, os, sched
from threading import Timer

# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# 第二个参数以某种人为的方式衡量时间
schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    print('开始执行：%s, 时间：%s' % (cmd, time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))))
    os.system(cmd)


def timming_exe(cmd, inc=60):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()


crawl_commend_1 = 'python run_lisan_matchs.py'
Timer(6, timming_exe, (crawl_commend_1, 40)).start()
print('保存实时爬虫任务：', crawl_commend_1)



