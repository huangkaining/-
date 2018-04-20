#coding=utf-8


import web
import json
import xlwings as xw
import pythoncom
import sta
import datetime
import qrcode
import hashlib
from lxml import etree
import time
import memcache
import news


urls = (
    '/','Index',
    '/main','main',
    '/intr','intr',
    '/register','Register',
    '/modify','Modify',
    '/score','Score',
    '/inclass','InClass',
    '/ingrade','InGrade',
    '/fileimport','FileImport',
    '/cleanone','Cleanone',
    '/cleanclass','Cleanclass',
    '/cleanclassmore','Cleanclassmore',
    '/cleanall','Cleanall',
    '/cleanallmore','Cleanallmore',
    '/studyone','Studyone',
    '/studyclass','Studyclass',
    '/clubone','Clubone',
    '/clubmore','Clubmore',
    '/clubmanage','Clubmanage',
    '/clubenergy','Clubenergy',
    '/clubuser','Clubuser',
    '/clubnum','Clubnum',
    '/consumption','Consumption',
    '/mealconsumption','MealConsumption',
    '/mealoccupy','MealOccupy',
    '/poorstudent','PoorStudent',
    '/prizedeclare','PrizeDeclare',
    '/scorestu','ScoreStu',
    '/classconsumption','ClassConsumption',
    '/consumptionstu','ConsumptionStu',
    '/clubsign','ClubSign',
    '/clubpic','ClubPic',
    '/wechat','wechat'
)
render = web.template.render('templates')



web.config.debug = False
app = web.application(urls,locals())
db = web.database(dbn="mysql", user="root", pw="password", db="stu_manage")
store = web.session.DBStore(db, 'sessions')  
session = web.session.Session(app, store) 

class JsonExtendEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


class Index:
    def GET(self):
        return render.index('')

    def POST(self):
        i = web.input()
        userid = i.get('userid')
        password = i.get('password')
        results = list(db.query("SELECT * FROM user WHERE userid='%s'"%userid))
        if results:
            if userid == results[0]['userid'] and password == results[0]['password']:
                session.logged_in = True
                session.userid = userid
                session.username = results[0]['username']
                session.au = results[0]['role']
                session.id = userid
                web.setcookie('system_mangement', '', 60)
                raise web.seeother('/main')
            else:
                status = "用户名或密码错误"
        else:
            status = "用户名或密码错误"

        return render.index(status)

class intr:
    def GET(self):
        return render.intr(session.username)
    
class main:
    def GET(self):
        au = session.au
        username = session.username
        list1 = list(db.query("SELECT urls,title FROM news WHERE type='school' and date(dtime) = '2018-4-19'"))
        list2 = list(db.query("SELECT urls,title FROM news WHERE type='paper' and date(dtime) = '2018-4-19'"))

        #list1.append({"urls":"www.baidu.com","title":"百度"})

        str1 = json.dumps(list1)
        str2 = json.dumps(list2)
        return render.main(username,session.au,str1,str2)
    def POST(self):
        x = web.input()
        ftitle = x.get('title')
        list3 = list(db.query("SELECT title,num FROM newsrecord WHERE title='%s'"%ftitle))
        if list3:
            db.update('newsrecord', where="title='%s'"%ftitle , num=list3[0]['num']+1)
        else:
            db.insert('newsrecord',title = ftitle,num = 1)
        list1 = list(db.query("SELECT urls,title FROM news WHERE type='school' and date(dtime) = '2018-4-19'"))
        list2 = list(db.query("SELECT urls,title FROM news WHERE type='paper' and date(dtime) = '2018-4-19'"))

        #list1.append({"urls": "www.baidu.com", "title": "百度"})

        str1 = json.dumps(list1)
        str2 = json.dumps(list2)
        return render.main(session.username, session.au, str1,str2)

class Modify:
    def GET(self):
        status = " "
        return render.modify(session.username, status)

    def POST(self):
        i= web.input()
        userid=session.userid
        newpw1 = i.get('newpw1')
        newpw2 = i.get('newpw2')
        if newpw1==newpw2:
            sql = "UPDATE user SET password= '%s' where userid='%s'"%(newpw1,userid)
            db.query(sql)
            status="修改成功"
        else:
            status="两次输入不一致"
        return render.modify(session.username, status)


class Register:
    def GET(self):
        userid, password, status = "", "", ""
        return render.register(userid, password, status)

    def POST(self):
        i = web.input()
        iuserid = i.get('userid')
        ipasswd = i.get('password')
        cursor = db.cursor()
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        results = cursor.fetchall()
        value = 1
        print(results)
        for row in results:
            if iuserid == row[0]:
                status = "该用户名已被注册"
                value = 0
                break
        if value == 1:
            cursor.execute("insert into user(userid,password) values('%s','%s')" % (iuserid, ipasswd))
            db.commit()
            status = str(iuserid) + "注册成功"
            raise web.seeother('/main')
        db.close()
        userid = ""
        password = ""
        return render.register(userid, password, status)

class Score:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.score(username,au)

class PrizeDeclare:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.prizedeclare(username,au,'')
    def POST(self):
        x = web.input()
        pid = x.get('userid')
        pclass = x.get('userclass')
        pname = x.get('prizename')
        ptime = x.get('prizetime')
        plevel = x.get('prizelevel')
        db.insert('prize',userid = pid,userclass = pclass, prize_name = pname, prize_time = ptime, prize_level = plevel)
        username = session.username
        au = session.au
        return render.prizedeclare(username, au,'上传成功')

class InClass:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.inclass(username,au,'','')
    def POST(self):
        '''import sys
        reload(sys)
        sys.setdefaultencoding('utf8')'''
        i = web.input()
        sub = i.get("sub1")
        sub2 = i.get("sub2")
        classresult = list(db.query("SELECT userclass FROM user WHERE userid='%s'" %session.userid))
        idresult = list(db.query("SELECT userid FROM user WHERE userclass='%s'" %classresult[0]['userclass']))
        result1 = []
        username = session.username
        au = session.au
        if sub == u"必修" or sub == u"选修":
            for p in idresult :
                re = list(db.query("SELECT userid,subject,subject_score FROM score WHERE userid='%s' and subject='%s'" %(p['userid'],sub2)))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1':'学号'},{'n2':'科目'},{'n3':'成绩'}]
            datastr2 = json.dumps(result2)
            return render.scorestu01(session.username,session.au,datastr1,datastr2)
        if sub == u"获奖":
            for p in idresult :
                re = list(db.query("SELECT userid,prize_name,prize_level FROM prize WHERE userid='%s'" %p['userid']))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '奖项名称'}, {'n3': '奖项等级'}]
            datastr2 = json.dumps(result2)
            return render.scorestu1(session.username, session.au, datastr1, datastr2)
        if sub == u"处分":
            for p in idresult :
                re = list(db.query("SELECT userid,punish_level FROM punishment WHERE userid='%s'" %p['userid']))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '处分类型'}]
            datastr2 = json.dumps(result2)
            return render.scorestu2(session.username, session.au, datastr1, datastr2)

'''class InClass:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.inclass(username,au,'','')
    def POST(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        i = web.input()
        sub = i.get("sub1")
        sub2 = i.get("sub2")
        classresult = list(db.query("SELECT userclass FROM user WHERE userid='%s'" %session.userid))
        idresult = list(db.query("SELECT userid FROM user WHERE userclass='%s'" %classresult[0]['userclass']))
        result1 = []
        username = session.username
        au = session.au
        if sub == u"必修" :
            for p in idresult :
                re = list(db.query("SELECT userid,subject,subject_score FROM score WHERE userid='%s' and subject_type='必修'" %p['userid']))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1':'学号'},{'n2':'科目'},{'n3':'成绩'}]
            datastr2 = json.dumps(result2)
            return render.scorestu01(session.username,session.au,datastr1,datastr2)
        if sub == u"选修" :
            for p in idresult :
                re = list(db.query("SELECT userid,subject,subject_score FROM score WHERE userid='%s' and subject_type='选修'" %p['userid']))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '科目'}, {'n3': '成绩'}]
            datastr2 = json.dumps(result2)
            return render.scorestu02(session.username,session.au,datastr1,datastr2)
        if sub == u"获奖":
            for p in idresult :
                re = list(db.query("SELECT userid,prize_name,prize_level FROM prize WHERE userid='%s'" %p['userid']))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '奖项名称'}, {'n3': '奖项等级'}]
            datastr2 = json.dumps(result2)
            return render.scorestu1(session.username, session.au, datastr1, datastr2)
        if sub == u"处分":
            for p in idresult :
                re = list(db.query("SELECT userid,punish_level FROM punishment WHERE userid='%s'" %p['userid']))
                result1.extend(re)
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '处分类型'}]
            datastr2 = json.dumps(result2)
            return render.scorestu2(session.username, session.au, datastr1, datastr2)'''

class InGrade:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.ingrade(username,au,'')
    def POST(self):
        i = web.input()
        itemchoice = i.get('itemchoice')
        gradechoice = i.get('gradechoice')
        data = {}
        #必修挂科1，必修优秀2，体育挂科3，体育优秀4，获奖数量5，处分数量6
        if itemchoice == '1':
            con1 = 'userclass'
            con2 = 'score'
            con3 = "subject_score<60 and subject_type='必修'"
            data['picname'] = '必修挂科'
        if itemchoice == '2':
            con1 = 'userclass'
            con2 = 'score'
            con3 = "subject_score>90 and subject_type='必修'"
            data['picname'] = '必修优秀'
        if itemchoice == '3':
            con1 = 'userclass'
            con2 = 'score'
            con3 = "subject_score<60 and subject='体育'"
            data['picname'] = '体育挂科'
        if itemchoice == '4':
            con1 = 'userclass'
            con2 = 'score'
            con3 = "subject_score>90 and subject='体育'"
            data['picname'] = '体育优秀'
        if itemchoice == '5':
            con1 = 'userclass'
            con2 = 'prize'
            con3 = ""
            data['picname'] = '获奖'
        if itemchoice == '6':
            con1 = 'userclass'
            con2 = 'punishment'
            con3 = ""
            data['picname'] = '处分'
        if gradechoice == '15':
            if con3 :
                con3 = con3 + " and userid REGEXP '^1015'"
            else :
                con3 = "userid REGEXP '^1015'"
        elif gradechoice == '16':
            if con3 :
                con3 = con3 + " and userid REGEXP '^1016'"
            else :
                con3 = "userid REGEXP '^1016'"
        elif gradechoice == '17':
            if con3 :
                con3 = con3 + " and userid REGEXP '^1017'"
            else :
                con3 = "userid REGEXP '^1017'"
        elif gradechoice == '18':
            if con3 :
                con3 = con3 + " and userid REGEXP '^1018'"
            else :
                con3 = "userid REGEXP '^1018'"
        result = list(db.query("SELECT %s FROM %s WHERE %s" %(con1,con2,con3)))
        s = {}
        for i in result:
            if i['userclass'] in s :
                s[i['userclass']]+=1
            else :
                s[i['userclass']] = 0
        ss = []
        for i in s:
            tmp = {}
            tmp['name'] = i
            tmp['value'] = s[i]
            ss.append(tmp)
        data['list'] = ss
        datastr = json.dumps(data)
        return render.ingrade(session.username, session.au, datastr)

class ScoreStu:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        result1=[{'n1': '无'}]
        datastr1 = json.dumps(result1)
        result2=[{'n1': '结果'}]
        datastr2 = json.dumps(result2)
        return render.scorestu(username,au,datastr1,datastr2)
    def POST(self):
        '''import sys
        reload(sys)
        sys.setdefaultencoding('utf8')'''
        i = web.input()
        sub = i.get("sub1")
        sub2 = i.get("sub2")
        userid = session.userid
        username = session.username
        au = session.au
        if sub == u"必修" or sub == u"选修":
            result1 = list(db.query("SELECT subject,userid,subject_score FROM score WHERE userid='%s' and subject='%s' " % (userid,sub2)))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '科目'}, {'n3': '成绩'}]
            datastr2 = json.dumps(result2)
            return render.scorestu01(session.username, session.au, datastr1, datastr2)
        if sub == u"获奖":
            result1 = list(db.query("SELECT userid,prize_name,prize_level FROM prize WHERE userid='%s'" % userid))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '奖项名称'}, {'n3': '奖项等级'}]
            datastr2 = json.dumps(result2)
            return render.scorestu1(session.username, session.au, datastr1, datastr2)
        if sub == u"处分":
            result1 = list(db.query("SELECT userid,punish_level FROM punishment WHERE userid='%s'" % userid))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '处分类型'}]
            datastr2 = json.dumps(result2)
            return render.scorestu2(session.username, session.au, datastr1, datastr2)

'''class ScoreStu:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        result1=[{'n1': '无'}]
        datastr1 = json.dumps(result1)
        result2=[{'n1': '结果'}]
        datastr2 = json.dumps(result2)
        return render.scorestu(username,au,datastr1,datastr2)
    def POST(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        i = web.input()
        sub = i.get("sub1")
        userid = session.userid
        username = session.username
        au = session.au
        if sub == u"必修":
            result1 = list(db.query("SELECT subject,userid,subject_score FROM score WHERE userid='%s' and subject_type='必修' " % userid))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '科目'}, {'n3': '成绩'}]
            datastr2 = json.dumps(result2)
            return render.scorestu01(session.username, session.au, datastr1, datastr2)
        if sub == u"选修":
            sql1="SELECT userid,subject,subject_score FROM score WHERE userid='%s' and subject_type='选修'" % userid
            result1 = list(db.query(sql1))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '科目'}, {'n3': '成绩'}]
            datastr2 = json.dumps(result2)
            return render.scorestu02(session.username, session.au, datastr1, datastr2)
        if sub == u"获奖":
            result1 = list(db.query("SELECT userid,prize_name,prize_level FROM prize WHERE userid='%s'" % userid))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '奖项名称'}, {'n3': '奖项等级'}]
            datastr2 = json.dumps(result2)
            return render.scorestu1(session.username, session.au, datastr1, datastr2)
        if sub == u"处分":
            result1 = list(db.query("SELECT userid,punish_level FROM punishment WHERE userid='%s'" % userid))
            datastr1 = json.dumps(result1)
            result2 = [{'n1': '学号'}, {'n2': '处分类型'}]
            datastr2 = json.dumps(result2)
            return render.scorestu2(session.username, session.au, datastr1, datastr2)'''


class FileImport:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.fileimport(username,au,'')

    def POST(self):
        x = web.input(myfile={})
        ty = x.get('sub1')
        username = session.username
        au = session.au
        filedir = 'C:\计算机大赛\上传文件'
        if 'myfile' in x:
            filepath = x.myfile.filename.replace('\\', '/')
            filename = filepath.split('/')[-1]
            fout = open(filedir + '/' + filename, 'wb')
            fout.write(x.myfile.file.read())
            fout.close()
            pythoncom.CoInitialize()
            app2 = xw.App(visible=False)
            wb = app2.books.open(filedir + '/' +filename)
            try:
                if ty == "学生表":
                    rng = wb.sheets['Sheet1'].range('A2')
                    while rng.value:
                        rng2 = rng.offset(row_offset = 0, column_offset = 3)
                        list1 = wb.sheets['sheet1'].range('%s:%s' %(rng.address,rng2.address)).value
                        db.insert('user',userid = str(int(list1[0])),username = list1[1], password = '123456', userclass = list1[2], role = 1, dormitory = list1[3])
                        rng = rng.offset(row_offset = 1, column_offset = 0)
                    wb.close()
                if ty == "成绩表":
                    rng = wb.sheets['Sheet1'].range('A2')
                    while rng.value:
                        rng2 = rng.offset(row_offset = 0, column_offset = 4)
                        list1 = wb.sheets['sheet1'].range('%s:%s' %(rng.address,rng2.address)).value
                        db.insert('score',userid = str(int(list1[0])), userclass = list1[1], subject = list1[2],subject_score = list1[3],subject_type = list1[4])
                        rng = rng.offset(row_offset = 1, column_offset = 0)
                    wb.close()
                if ty == "卫生表":
                    rng = wb.sheets['Sheet1'].range('A2')
                    while rng.value:
                        rng2 = rng.offset(row_offset = 0, column_offset = 4)
                        list1 = wb.sheets['sheet1'].range('%s:%s' %(rng.address,rng2.address)).value
                        db.insert('clean_inspect',userid = str(int(list1[0])), userclass = list1[1], clean_grade = list1[2],dormitory = list1[3],inspect_time = list1[4])
                        rng = rng.offset(row_offset = 1, column_offset = 0)
                    wb.close()
                if ty == "集体自习签到":
                    rng = wb.sheets['Sheet1'].range('A2')
                    while rng.value:
                        rng2 = rng.offset(row_offset = 0, column_offset = 3)
                        list1 = wb.sheets['sheet1'].range('%s:%s' %(rng.address,rng2.address)).value
                        db.insert('study_signin',userid = str(int(list1[0])), userclass = list1[1], username = list1[2],signin_time = list1[3] )
                        rng = rng.offset(row_offset = 1, column_offset = 0)
                    wb.close()
                if ty == "消费记录":
                    rng = wb.sheets['Sheet1'].range('A2')
                    while rng.value:
                        rng2 = rng.offset(row_offset = 0, column_offset = 3)
                        list1 = wb.sheets['sheet1'].range('%s:%s' %(rng.address,rng2.address)).value
                        db.insert('consumption',userid = str(int(list1[0])), userclass = list1[1], consume_number = int(list1[2]),consume_time = list1[3] )
                        rng = rng.offset(row_offset = 1, column_offset = 0)
                    wb.close()
            except BaseException as e:
                wb.close()
                app2.quit()
                print(e)
                return render.fileimport(username, au, '导入失败（如有疑问请询问管理员）')

        return render.fileimport(username,au,'导入成功')


class Cleanone:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT dormitory FROM user WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        dorm = result1[0]['dormitory']
        sql2 = "SELECT clean_grade,inspect_time FROM clean_inspect WHERE userid = '%s'" % userid
        result2 = list(db.query(sql2))
        data = json.dumps(result2,cls=JsonExtendEncoder)
        you = 0
        liang = 0
        zhong = 0
        cha = 0
        for row in result2:
            if row['clean_grade'] == u"优":
                you += 1
            if row['clean_grade'] == u"良":
                liang += 1
            if row['clean_grade'] == u"中":
                zhong += 1
            if row['clean_grade'] == u"差":
                cha += 1
        return render.cleanone(session.username, dorm, data, you, liang, zhong, cha,session.au)


class Cleanclass:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM user WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        userclass = result1[0]['userclass']
        sql2 = "SELECT distinct dormitory,inspect_time,clean_grade FROM clean_inspect WHERE userclass = '%s'" % userclass
        result2 = list(db.query(sql2))
        print(result2)
        sql3 = "SELECT distinct userclass,dormitory FROM dorm_class WHERE userclass = '%s' ORDER BY dormitory" % userclass
        result3 = list(db.query(sql3))
        dormsum = len(result3)
        you = 0
        liang = 0
        zhong = 0
        cha = 0
        list1 = []
        for i in range(dormsum):
            dorm = result3[i]['dormitory']
            for row in result2:
                if row['dormitory'] == dorm:
                    if row['clean_grade'] == u"优":
                        you += 1
                    if row['clean_grade'] == u"良":
                        liang += 1
                    if row['clean_grade'] == u"中":
                        zhong += 1
                    if row['clean_grade'] == u"差":
                        cha += 1
            list1.append({'dormitory': dorm, 'you': you, 'liang': liang, 'zhong': zhong, 'cha': cha})
            you = 0
            liang = 0
            zhong = 0
            cha = 0
        data = json.dumps(list1,cls=JsonExtendEncoder)
        # print list1

        return render.cleanclass(session.username, userclass, data,session.au)


class Cleanclassmore:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM user WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        userclass = result1[0]['userclass']
        sql2 = "SELECT distinct dormitory,clean_grade,inspect_time FROM clean_inspect WHERE userclass = '%s' ORDER BY inspect_time,dormitory" % userclass
        result2 = list(db.query(sql2))
        data = json.dumps(result2,cls=JsonExtendEncoder)
        return render.cleanclassmore(session.username, userclass, data,session.au)


class Cleanall:
    def GET(self):
        userid=session.userid
        sql1="SELECT * FROM user WHERE userid = '%s'"%userid
        result1=list(db.query(sql1))
        userclass=result1[0]['userclass']
        sql2="SELECT distinct dormitory,clean_grade,inspect_time,userclass FROM clean_inspect"
        result2=list(db.query(sql2))
        sql3="SELECT DISTINCT userclass FROM clean_inspect ORDER BY dormitory"
        result3=list(db.query(sql3))
        classsum=len(result3)

        you=0
        liang=0
        zhong=0
        cha=0
        list1 = []
        for i in range(classsum):
            oneclass=result3[i]['userclass']
            for row in result2:
                if row['userclass']==oneclass:
                    if row['clean_grade']==u"优":
                        you+=1
                    if row['clean_grade']==u"良":
                        liang+=1
                    if row['clean_grade']==u"中":
                        zhong+=1
                    if row['clean_grade']==u"差":
                        cha+=1
            sumnum=you+liang+zhong+cha
            proyou=round(you*100/sumnum,2)
            proliang=round(liang*100/sumnum,2)
            prozhong=round(zhong*100/sumnum,2)
            procha=round(cha*100/sumnum,2)
            list1.append({'oneclass':oneclass,'you':proyou,'liang':proliang,'zhong':prozhong,'cha':procha})
            you=0
            liang=0
            zhong=0
            cha=0
        data=json.dumps(list1)

        return render.cleanall (session.username,data,session.au)


class Cleanallmore:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM user WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        userclass = result1[0]['userclass']
        sql2 = "SELECT distinct userclass,dormitory,clean_grade,inspect_time FROM clean_inspect ORDER BY inspect_time,dormitory"
        result2 = list(db.query(sql2))
        data = json.dumps(result2,cls=JsonExtendEncoder)
        return render.cleanallmore(session.username,data,session.au)


class Studyone:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM study_signin WHERE userid = '%s' ORDER BY signin_time" % userid
        result1 = list(db.query(sql1))
        studysum = len(result1)
        data = json.dumps(result1,cls=JsonExtendEncoder)
        return render.studyone(session.username, studysum, data,session.au)


class Studyclass:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM user WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        userclass = result1[0]['userclass']
        sql2 = "SELECT * FROM study_signin WHERE userclass = '%s'" % userclass
        result2 = list(db.query(sql2))
        sql3 = "SELECT DISTINCT username FROM user WHERE userclass = '%s' and role = 1 ORDER BY userid" % userclass
        result3 = list(db.query(sql3))
        usersum = len(result3)
        num = 0
        list1 = []
        for i in range(usersum):
            username = result3[i]['username']
            for row in result2:
                if row['username'] == username:
                    num += 1
            list1.append({'username': username, 'num': num})
            num = 0
        data = json.dumps(list1,cls=JsonExtendEncoder)
        return render.studyclass(session.username, userclass, data,session.au)


class Clubone:
    def GET(self):
        '''import sys
        reload(sys)
        sys.setdefaultencoding('utf8')'''
        userid = session.userid
        sql1 = "SELECT * FROM club_signin WHERE userid = '%s' ORDER BY signin_time" % userid
        result1 = list(db.query(sql1))
        data = json.dumps(result1)
        return render.clubone(session.username,session.au,data)


class Clubmanage:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM club_manage WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        clubname = result1[0]['club_name']
        sql2 = "SELECT * FROM club_signin WHERE club_name = '%s'" % clubname
        result2 = list(db.query(sql2))
        sql3 = "SELECT DISTINCT username FROM club_signin WHERE club_name = '%s'" % clubname
        result3 = list(db.query(sql3))
        clubsum = len(result3)
        num = 0
        list1 = []
        for i in range(clubsum):
            username = result3[i]['username']
            for row in result2:
                if row['username'] == username:
                    num += 1
            list1.append({'username': username, 'signinnum': num})
            num = 0
        data = json.dumps(list1)
        return render.clubmanage(session.username, clubname, data,session.au)


class Clubmore:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT * FROM club_manage WHERE userid = '%s'" % userid
        result1 = list(db.query(sql1))
        clubname = result1[0]['club_name']
        sql2 = "SELECT * FROM club_signin WHERE club_name = '%s' ORDER BY signin_time" % clubname
        result2 = list(db.query(sql2))
        data = json.dumps(result2)
        return render.clubmore(session.username,clubname, data,session.au)


class Clubenergy:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT DISTINCT username,club_name FROM club_signin"
        result1 = list(db.query(sql1))
        sql2 = "SELECT * FROM club_signin"
        result2 = list(db.query(sql2))
        sql3 = "SELECT DISTINCT club_name FROM club_signin"
        result3 = list(db.query(sql3))
        clubsum = len(result3)
        user = 0
        num = 0
        list1 = []
        for i in range(clubsum):
            clubname = result3[i]['club_name']
            for row in result2:
                if row['club_name'] == clubname:
                    num += 1
            for row in result1:
                if row['club_name'] == clubname:
                    user += 1
            list1.append({'clubname': clubname, 'signinuser': user, 'signinnum': num})
            num = 0
            user = 0
        data = json.dumps(list1)
        return render.clubenergy(session.username, data,session.au)


class Clubuser:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT DISTINCT username,club_name FROM club_signin"
        result1 = list(db.query(sql1))
        sql2 = "SELECT * FROM club_signin"
        result2 = list(db.query(sql2))
        sql3 = "SELECT DISTINCT club_name FROM club_signin"
        result3 = list(db.query(sql3))
        clubsum = len(result3)
        user = 0
        num = 0
        list1 = []
        for i in range(clubsum):
            clubname = result3[i]['club_name']
            for row in result2:
                if row['club_name'] == clubname:
                    num += 1
            for row in result1:
                if row['club_name'] == clubname:
                    user += 1
            list1.append({'clubname': clubname, 'signinuser': user, 'signinnum': num})
            num = 0
            user = 0
        data = json.dumps(list1)
        return render.clubuser(session.username, data,session.au)


class Clubnum:
    def GET(self):
        userid = session.userid
        sql1 = "SELECT DISTINCT username,club_name FROM club_signin"
        result1 = list(db.query(sql1))
        sql2 = "SELECT * FROM club_signin"
        result2 = list(db.query(sql2))
        sql3 = "SELECT DISTINCT club_name FROM club_signin"
        result3 = list(db.query(sql3))
        clubsum = len(result3)
        user = 0
        num = 0
        list1 = []
        for i in range(clubsum):
            clubname = result3[i]['club_name']
            for row in result2:
                if row['club_name'] == clubname:
                    num += 1
            for row in result1:
                if row['club_name'] == clubname:
                    user += 1
            list1.append({'clubname': clubname, 'signinuser': user, 'signinnum': num})
            num = 0
            user = 0
        data = json.dumps(list1)
        return render.clubnum(session.username, data,session.au)

class Consumption:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.consumption(username,au)

class MealConsumption:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        xx = web.input()
        data = []
        t = []
        for i in ['1','2','3','4','5','6','7','8','9','10','11','12']:
            mlist = list(db.query("SELECT consume_number FROM consumption WHERE DATE_FORMAT(consume_time,'%H')<8 and DATE_FORMAT(consume_time,'%m')=" + i))
            if mlist:
                t.append(round(sta.average(sta.excludeoutlier(mlist)),2))
            else:
                t.append(0)
        data.append(t)
        t = []
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            mlist = list(db.query(
                "SELECT consume_number FROM consumption WHERE DATE_FORMAT(consume_time,'%H')>=11 and DATE_FORMAT(consume_time,'%H')<=12 and DATE_FORMAT(consume_time,'%m')=" + i))
            if mlist:
                t.append(round(sta.average(sta.excludeoutlier(mlist)),2))
            else:
                t.append(0)
        data.append(t)
        t = []
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            mlist = list(db.query(
                "SELECT consume_number FROM consumption WHERE DATE_FORMAT(consume_time,'%H')>=6 and DATE_FORMAT(consume_time,'%H')<=12 and DATE_FORMAT(consume_time,'%m')=" + i))
            if mlist:
                t.append(round(sta.average(sta.excludeoutlier(mlist)),2))
            else:
                t.append(0)
        data.append(t)
        datastr = json.dumps(data)
        return render.mealconsumption(session.username, session.au, datastr)

class MealOccupy:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        sql1 = "SELECT userid FROM user WHERE role = 1"
        result1 = list(db.query(sql1))
        num = len(result1)

        data = []
        t = []
        for i in ['1','2','3','4','5','6','7','8','9','10','11','12']:
            mlist = list(db.query("SELECT userid FROM consumption WHERE DATE_FORMAT(consume_time,'%H')<8 and DATE_FORMAT(consume_time,'%m')=" + i))
            t.append(round(len(mlist)/num,2))
        data.append(t)
        t = []
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            mlist = list(db.query(
                "SELECT consume_number FROM consumption WHERE DATE_FORMAT(consume_time,'%H')>=11 and DATE_FORMAT(consume_time,'%H')<=12 and DATE_FORMAT(consume_time,'%m')=" + i))
            t.append(round(len(mlist) / num,2))
        data.append(t)
        t = []
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            mlist = list(db.query(
                "SELECT consume_number FROM consumption WHERE DATE_FORMAT(consume_time,'%H')>=6 and DATE_FORMAT(consume_time,'%H')<=12 and DATE_FORMAT(consume_time,'%m')=" + i))
            t.append(round(len(mlist) / num,2))
        data.append(t)
        datastr = json.dumps(data)
        return render.mealoccupy(session.username, session.au, datastr)

class ConsumptionStu:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.consumptionstu(username,au,'')
    def POST(self):
        xx = web.input()
        fsql = "SELECT consume_number FROM consumption WHERE DATE_FORMAT(consume_time,'%m') = " + str(datetime.datetime.now().month) + " and userid='%s'"%session.id
        list1 = list(db.query(fsql))
        cnt = 0
        for i in list1:
            cnt+= i['consume_number']
        return render.consumptionstu(session.username, session.au,str(cnt))
class ClassConsumption:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        data = []
        t = []
        cla = "'" + db.query("SELECT userclass FROM user WHERE userid = %s" %session.userid)[0]['userclass'] + "'"
        for i in ['1','2','3','4','5','6','7','8','9','10','11','12']:
            fsql = "SELECT consume_number FROM consumption WHERE userclass = " + cla + " and DATE_FORMAT(consume_time,'%H')<8 and DATE_FORMAT(consume_time,'%m')=" + i
            mlist = list(db.query(fsql))
            if mlist:
                t.append(round(sta.average(sta.excludeoutlier(mlist)),2))
            else:
                t.append(0)
        data.append(t)
        t = []
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            fsql = "SELECT consume_number FROM consumption WHERE userclass = "+ cla + " and DATE_FORMAT(consume_time,'%H')>=11 and DATE_FORMAT(consume_time,'%H')<=12 and DATE_FORMAT(consume_time,'%m')=" + i
            mlist = list(db.query(fsql))
            if mlist:
                t.append(round(sta.average(sta.excludeoutlier(mlist)),2))
            else:
                t.append(0)
        data.append(t)
        t = []
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            fsql = "SELECT consume_number FROM consumption WHERE userclass = " + cla + " and DATE_FORMAT(consume_time,'%H')>=6 and DATE_FORMAT(consume_time,'%H')<=12 and DATE_FORMAT(consume_time,'%m')=" + i
            mlist = list(db.query(fsql))
            if mlist:
                t.append(round(sta.average(sta.excludeoutlier(mlist)),2))
            else:
                t.append(0)
        data.append(t)
        datastr = json.dumps(data)
        return render.classconsumption(session.username, session.au, datastr)

class ClubSign:
    def GET(self):
        i = web.input(ct=None)
        re = db.query("SELECT signtime FROM clubsigntime WHERE signid = %s" %i.ct)[0]['signtime']
        if (datetime.datetime.now() - re).total_seconds() > 30:
            return render.clubsign(1)#超时
        else:
            return render.clubsign(2)#登录
    def POST(self):
        x = web.input(ct = None)
        pw = x.get('password')
        fuserid = x.get('userid')
        re = list(db.query("SELECT password,username FROM user WHERE userid ="+ fuserid))
        if re:
            if re[0]['password'] == pw:
                clubname = db.query("SELECT clubname FROM clubsigntime WHERE signid = %s"%x.ct)[0]['clubname']

                db.insert('club_signin',userid = fuserid,signin_time = datetime.datetime.now().strftime("%Y%m%d"),username = re[0]['username'],club_name = clubname)
                return render.clubsign(3)#签到成功
            else:
                return render.clubsign(4)#密码错误
        else:
            return render.clubsign(4)#密码错误

class ClubPic:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.clubpic(username,au,'')
    def POST(self):
        x = web.input()
        cnamel = list(db.query("SELECT club_name FROM club_manage WHERE userid = %s"%session.userid))
        cname = ''
        if cnamel:
            cname = cnamel[0]['club_name']
        signid = hash(datetime.datetime.now())
        db.insert('clubsigntime',signid = signid,signtime = datetime.datetime.now(),clubname = cname)
        img = qrcode.make("http://101.132.141.63/clubsign?ct=" + str(signid))
        filedir = "C:\计算机大赛\static"+"\\" + str(signid) + '.png'
        img.save(filedir)
        return render.clubpic2(session.username,session.au,'../static/' + str(signid) + '.png')

class PoorStudent:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/')
        username = session.username
        au = session.au
        return render.poorstudent(username, au, '','','','')
    def POST(self):
        x = web.input(myfile={})
        username = session.username
        au = session.au
        filedir = 'C:\计算机大赛\上传文件'
        if 'myfile' in x:
            filepath = x.myfile.filename.replace('\\', '/')
            filename = filepath.split('/')[-1]
            fout = open(filedir + '/' + filename, 'wb')
            fout.write(x.myfile.file.read())
            fout.close()
            pythoncom.CoInitialize()
            app2 = xw.App(visible=False)
            wb = app2.books.open(filedir + '/' + filename)
            rng = wb.sheets['Sheet1'].range('A2')
            poorlist = []#贫困学生列表
            while rng.value:
                poorlist.append(rng.value)
                rng = rng.offset(row_offset=1, column_offset=0)
            wb.close()

            idlist = list(db.query("SELECT userid FROM USER"))
            cs = {}#所有学生消费列表
            klist = []
            for id in idlist:
                cnt = 0
                clist = list(db.query("SELECT consume_number FROM consumption WHERE userid = %s"%id['userid']))
                for i in clist:
                    cnt+=int(i['consume_number'])
                cs[id['userid']] = cnt
                tmp = []
                tmp.append(cnt)
                if cnt>1000 :
                    klist.append(tmp)
            kcen = sorted(sta.Kmean(klist))
            #print(kcen)
            chigh = str(kcen[2])
            cmiddle = str(kcen[1])
            clow = str(kcen[0])
            datalist = []
            for id in poorlist:
                tmp = {}
                tmp['id'] = id
                tmp['cs'] = cs[id]
                datalist.append(tmp)
            datastr = json.dumps(datalist)
            return render.poorstudent2(session.username,session.au,datastr,chigh,cmiddle,clow)

class wechat:
    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "huangkaining"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()
        xml = etree.fromstring(str_xml)

        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        mc = memcache.Client(['127.0.0.1:11211'])

        if msgType == "event":
            msgContent = xml.find("Event").text
            if msgContent == "subscribe":
                return render.reply_news1(fromUser, toUser, int(time.time()), u'欢迎关注学生数据分析平台！！！\n\n01.进入网页版本\n02.用户登录\n05.热门词汇')

        if msgType == 'text':
            content = xml.find("Content").text  # 获得用户所输入的内容
            mc_content = mc.get(fromUser + '_content')  # 设置三个mc变量
            mc_userID = mc.get(fromUser + '_userID')
            mc_login = mc.get(fromUser + '_login')

            if content == 'menu':
                res = u'学生数据分析平台\n\n01.进入网页版本\n02.用户登录\n05.热门词汇'
                return render.reply_news1(fromUser, toUser, int(time.time()), res)
            if content == "01" :
                res = u'101.132.141.63'
                return render.reply_news1(fromUser, toUser, int(time.time()), res)
            if content == "02" :
                res = u'请以（账号xxx）输入账号'
                return render.reply_news1(fromUser, toUser, int(time.time()), res)
            if content[0:2] == "账号" :
                mc.set(fromUser + '_content', content[2:])
                res = u'请以（密码xxx）输入密码'
                return render.reply_news1(fromUser, toUser, int(time.time()), res)
            if content[0:2] == "密码":
                re = list(db.query("SELECT password FROM user WHERE userid ='%s'"%mc_content))
                if re :
                    if re[0]['password'] == content[2:] :
                        mc.set(fromUser + '_login', '1')
                        res = u'学生数据分析平台\n\n03.消费查询\n04.成绩查询'
                        return render.reply_news1(fromUser, toUser, int(time.time()), res)
                    else :
                        return render.reply_news1(fromUser, toUser, int(time.time()), u"账户名或密码错误")
                else:
                    return render.reply_news1(fromUser, toUser, int(time.time()), u"账户名或密码错误")
            if content == "03" :
                if mc_login == "1" :
                    list1 = list(db.query("SELECT consume_number FROM consumption WHERE userid = '%s'" %mc_content))
                    cnt = 0
                    for i in list1 :
                        cnt += i['consume_number']
                    return render.reply_news1(fromUser, toUser, int(time.time()), str(cnt))
                else :
                    return render.reply_news1(fromUser, toUser, int(time.time()),  u'学生数据分析平台\n\n01.进入网页版本\n02.用户登录\n05.热门词汇')
            if content == "04" :
                if mc_login == "1" :
                    return render.reply_news1(fromUser, toUser, int(time.time()), u"请以（课程xxx)输入课程名字")
                else :
                    return render.reply_news1(fromUser, toUser, int(time.time()),  u'学生数据分析平台\n\n01.进入网页版本\n02.用户登录\n05.热门词汇')
            if content[0:2] == "课程" :
                if mc_login == "1" :
                    list1 = list(db.query("SELECT subject_score FROM score WHERE userid='%s' and subject='%s'"%(mc_content,content[2:])))
                    if list1:
                        return render.reply_news1(fromUser, toUser, int(time.time()), list1[0]['subject_score'])
                    else:
                        return render.reply_news1(fromUser, toUser, int(time.time()), u"此课程未修习")
                else :
                    return render.reply_news1(fromUser, toUser, int(time.time()),  u'学生数据分析平台\n\n01.进入网页版本\n02.用户登录\n05.热门词汇')
            if content=="05":
                list1 = news.words()
                word = []
                cnt = []
                rep = ""
                for i in range(min(10, len(list1) - 1)):
                    #word.append(list1[i]['word'])
                    #cnt.append(list1[i]['cnt'])
                    rep+= list1[i]['word'] + "-->" + str(list1[i]['cnt']) + "   "
                return render.reply_news3(fromUser, toUser, int(time.time()), rep)

if __name__ == '__main__':
    app.run()

