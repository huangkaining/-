# -*- coding: UTF-8 -*-
from urllib import request
import re
import json
import datetime
import jieba
import web

db = web.database(dbn="mysql", user="root", pw="password", db="stu_manage")

def words():
    list1 = list(db.query("SELECT title,num FROM newsrecord"))
    dict1 = {}
    for i in list1:
        cutre = list(jieba.cut(i['title']))
        for j in cutre:
            if j in dict1.keys():
                dict1[j]+= i['num']
            else:
                dict1[j]=i['num']
    dict2 = sorted(dict1.items(), key=lambda d: d[1], reverse=True)
    list2 = []
    cnt = 0
    for i in dict2:
        if cnt >9 :
            break
        p = {}
        p['word'] = i[0]
        p['cnt'] = i[1]
        list2.append(p)
        cnt = cnt + 1
    #data = json.dumps(list2)
    #return data
    return list2

def searchin():
    response = request.urlopen("http://jwc.ecust.edu.cn/main.htm")
    #print(response.getcode())
    #print(response.geturl())
    #print(response.info())
    html = response.read()
    html = html.decode("utf-8")
    #print(len(html))

    pat = "ico4.gif.*?<td align=.*?><a href='(.*?)' target='_blank' title='(.*?)'>.*?<div style=.white-space:nowrap.>(.*?)</div>"
    result=re.compile(pat,re.S).findall(str(html))
    a=sorted(result, key=lambda x:x[2],reverse=True)
    b=a[:10]
    list1 = []
    for i in range(8):
        list1.append({'url':"http://jwc.ecust.edu.cn"+b[i][0],'title':b[i][1],'date':b[i][2]})
    #data = json.dumps(list1)
    #return data
    return list1

def searchout():
    year=datetime.datetime.now().year
    yearstr=str(year)
    month=datetime.datetime.now().month
    if (month<10):
        monthstr="0"+str(month)
    day=datetime.datetime.now().day-1
    daystr=str(day)
    urlpre="http://paper.people.com.cn/rmrb/html/"+yearstr+"-"+monthstr+"/"+daystr+"/"
    url=urlpre+"nbs.D110000renmrb_01.htm"
    response = request.urlopen(url)
    #print(response.getcode())
    #print(response.geturl())
    #print(response.info())
    html = response.read()
    html = html.decode("utf-8",errors = 'ignore')
    #print(len(html))

    pat = '<li[ class="one"]*>[\s]*<a href=(.*?)><script>document.write.view."(.*?)[\s]*"..</script></a></li>'
    result=re.compile(pat,re.S).findall(str(html))
    list1 = []
    for i in result:
        list1.append({'url':urlpre+i[0],'title':i[1]})
    #data = json.dumps(list1)
    #return data
    return list1
