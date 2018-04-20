# -*- coding: UTF-8 -*-
from urllib import request
import re
import json
import datetime
import jieba
import web
import news
import time

db = web.database(dbn="mysql", user="root", pw="password", db="stu_manage")

while(True):
    list1 = news.searchin()
    list2 = news.searchout()
    for i in list1:
        furl = i['url']
        ftitle = i['title']
        ftime = datetime.datetime.today()
        db.insert('news',urls = furl, title = ftitle, dtime = ftime,type = "school")
    for i in list2:
        furl = i['url']
        ftitle = i['title']
        ftime = datetime.datetime.today()
        db.insert('news',urls = furl, title = ftitle, dtime = ftime, type = "paper")
    time.sleep(86400)
