import ast
import hashlib
import json
import re
import time

import requests
import muggle_ocr



class QK:

    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        # 'Cookie': 'selectionBar=1293218; JSESSIONID=abcSqj_vxPiEdc9-3v7my',
        # 'DNT': '1',
        'Host': 'zhjw.scu.edu.cn',
        'Upgrade-Insecure-Requlogin_ests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        }

        self.select = "2022-2023-1-1" # 待修改
        self.url_logout1='http://zhjw.scu.edu.cn/logout'
        self.url_logout2='http://zhjw.scu.edu.cn/enterOut'
        self.url_captcha = 'http://zhjw.scu.edu.cn/img/captcha.jpg'
        self.url_index = "http://zhjw.scu.edu.cn/login"
        self.url_check='http://zhjw.scu.edu.cn/j_spring_security_check'
        self.url_code='http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/getYzmPic'
        self.course_select_url = "http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/callback"
        self.free_course_list_url = "http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/courseList"
        self.course_selecting_url = "http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit"

        self.session= requests.session()
        self.config_info = []
        self.course_select = []
        self.free_course = []
        self.getConfig()

    def get_fajhh(self):
        res=self.session.get(url='http://zhjw.scu.edu.cn/student/rollManagement/rollInfo/index', headers=self.headers)
        fajhh = re.findall('<input type="hidden" id="zx" name="zx" value="(.*?)"/>', res.content.decode(),re.S)
        # print(1)
        # print(res.content.decode())
        # print(fajhh)
        return fajhh[0]

    def getConfig(self):
        with open('config.txt', 'r',  encoding='utf-8') as f:
            for line in f.readlines():
                self.config_info.append(line.strip())

    def get_token(self):
        res=self.session.get(url=self.url_index, headers=self.headers).content.decode()
        token=re.findall('name="tokenValue" value="(.*)">', res)
        print("token:", token[0])
        # print("get_token_cookie:",self.session.cookies)
        self.tokenValue=token[0]
        return token[0]

    def get_captcha(self, turl):
        # print("get_captcha_cookie:", self.session.cookies)
        with open('captcha.jpg', 'wb') as f:
            f.write(self.session.get(url=turl, headers=self.headers).content)
        with open("captcha.jpg", 'rb') as f:
            captcha_bytes = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        captcha = sdk.predict(image_bytes=captcha_bytes)
        print("验证码:", captcha)
        return captcha

    def login(self):
        login_data = {
            "j_username": self.config_info[0],
            "j_password": hashlib.md5(self.config_info[1].encode()).hexdigest(),
            "j_captcha": self.get_captcha(self.url_captcha),
            "tokenValue": self.get_token()
        }
        print(login_data)
        res=self.session.post(url=self.url_check, headers=self.headers, data=login_data)
        if "欢迎您" in res.content.decode():
            print("登录成功")
            self.fajhh=self.get_fajhh()
        else:
            print("登录失败")
            if "您输入的验证码错误" in res.content.decode():
                print("验证码错误")
            elif "token校验失败" in res.content.decode():
                print("token校验失败")
            # print(res.content.decode())

    def logout(self):
        res1=self.session.get(url=self.url_logout1, headers=self.headers).content.decode()
        res2=self.session.get(url=self.url_logout2,headers=self.headers).content.decode()
        with open(" logout1.html", 'w', encoding="utf-8") as f1:
            f1.write(res1)
            f1.close()
        with open("retest.py", 'w', encoding="utf-8") as f2:
            f2.write(res2)
            f2.close()
        print("尝试注销")

    def check_if_course_select(self):
        responce = self.session.get(url=self.course_select_url, headers=self.headers).text
        for info in json.loads(responce)['xkxx'][0]:
            self.course_select.append(json.loads(responce)['xkxx'][0][info]['courseName'])

    def get_free_course_list(self):
        list_data = {
            "searchtj": self.config_info[2],
            "xq": "0",
            "jc": "0",
            "kclbdm": ""
        }
        responce = self.session.post(url=self.free_course_list_url, headers=self.headers,
                                     data=list_data).content.decode()
        # print(responce)
        self.free_course = ast.literal_eval(json.loads(responce)["rwRxkZlList"])

    def get_kcms(self, ss):
        kcms = ""
        for s in ss:
            kcms += (str(ord(s)) + ',')
        self.kcms = kcms

    def get_course(self,course):
        print("课程：" + course['kcm']+" 课序号"+str(course['kxh']) + " 教师：" + course['skjs'] + " 课余量" + str(course['bkskyl']))
        if course['bkskyl'] > 0 and self.config_info[3] == course['kch'] and self.config_info[4] == course['kxh']:
            kcm = course['kcm']
            kch = course['kch']
            kxh = course['kxh']
            self.get_kcms(kcm + "(" + kch + "@" + kxh + ")")
            res = self.session.get(url='http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index',
                                headers=self.headers).content.decode()
            tokenValue=re.findall('<input type="hidden" id="tokenValue" value="(.*?)"/>', res)
            select_data = {
                'dealType': "2", # 待修改
                'kcIds': kch + '@' + kxh + '@' + self.select,
                'kcms': self.kcms,
                'fajhh': self.fajhh, # 待修改
                'sj': '0_0',
                'searchtj': '',
                'kclbdm': '',
                'inputCode': self.get_captcha(self.url_code),
                #
                'tokenValue': tokenValue[0]
            }
            try:
                status = self.session.post(url=self.course_selecting_url, data=select_data).text
                print("选课状态：", status)
                return
            except Exception as e:
                print("get_course()出现问题" + str(e))
        else:
            pass

    def loop(self):
        self.login()
        count = 1
        while True:
            print("正在进行第{}轮抢课".format(count))
            count += 1
            # 1.查询是否已经选中
            self.check_if_course_select()
            if self.config_into[2] in self.course_select:
                print("您已经选中这门课了！")
                exit()

            # 2.查看相应的空余课表
            self.get_free_course_list()
            if self.free_course is None:
                continue
            for course in self.free_course:
                self.get_course(course)

            # 3.等候时间
            time.sleep(1.5)


if __name__=="__main__":
    A=QK()
    A.loop()
    # A.login()
    # print(A.fajhh)
    # res=A.session.get(url='http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index',headers=A.headers).content.decode()
    # print(re.findall('<input type="hidden" id="tokenValue" value="(.*?)"/>',res))
    # 抢课完成，进行退出
    A.logout()
    A.session.close()

