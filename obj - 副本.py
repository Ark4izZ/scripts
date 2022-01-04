import requests
from PIL import Image
import hashlib
import json
import ast
import re
import time
import sys
import muggle_ocr


class qiangke:
    def __init__(self):
        self.session = requests.session()
        self.config_into = []
        self.course_select = []
        self.free_course = []
        self.select = "2020-2021-2-1"
        self.captcha_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
        self.check_url = "http://zhjw.scu.edu.cn/j_spring_security_check"
        self.course_select_url = "http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/callback"
        self.free_course_list_url = "http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/courseList"
        self.course_selecting_url = "http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit"
        self.token_url = "http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index"
        self.code_url = "http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/getYzmPic"
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'zhjw.scu.edu.cn',
            'Upgrade-Insecure-Requlogin_ests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        }

    # 读取写好的txt文件，获取需要的课程名等信息
    def getinto(self):
        with open('config.txt', 'r',  encoding='utf-8') as f:
            for line in f.readlines():
                self.config_into.append(line.strip())

    # 登录
    def login(self):
        while True:
            with open('captcha.jpg', 'wb') as f:
                f.write(self.session.get(url=self.captcha_url, headers=self.headers).content)
            with open("captcha.jpg", 'rb') as f:
                captcha_bytes = f.read()
            sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
            self.text = sdk.predict(image_bytes=captcha_bytes)
            login_data = {
                "j_username": self.config_into[0],
                "j_password": hashlib.md5(self.config_into[1].encode()).hexdigest(),
                # "j_captcha": input("请输入验证码：")
                "j_captcha": self.text
            }
            print(login_data)
            responce = self.session.post(url=self.check_url, headers=self.headers, data=login_data).text
            if "欢迎您" in responce:
                print("登录成功！")
                break
            else:
                print("登陆失败！")

    def dash(self):
            with open('code.jpg', 'wb') as f:
                f.write(self.session.get(url=self.code_url,headers=self.headers).content)
            with open("code.jpg", 'rb') as f:
                code_bytes = f.read()
            sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
            self.code = sdk.predict(image_bytes=code_bytes)

    # 查询已经选到的课
    def check_if_course_select(self):
        responce = self.session.get(url=self.course_select_url, headers=self.headers).text
        for info in json.loads(responce)['xkxx'][0]:
            self.course_select.append(json.loads(responce)['xkxx'][0][info]['courseName'])

    # 查询空余课表
    def get_free_course_list(self):
        list_data = {
            "searchtj": self.config_into[2],
            "xq": "0",
            "jc": "0",
            "kclbdm": ""
        }
        responce = self.session.post(url=self.free_course_list_url, headers=self.headers,
                                     data=list_data).content.decode()
        self.free_course = ast.literal_eval(json.loads(responce)["rwRxkZlList"])

    def get_kcms(self, ss):
        kcms = ""
        for s in ss:
            kcms += (str(ord(s)) + ',')
        self.kcms = kcms

    def get_token(self):
        response = self.session.get(url=self.token_url, headers=self.headers).text
        pat = re.compile("([a-fA-F0-9]{32})").findall(response)
        self.token_value = pat[0]
        self.dash()

    # 抢课
    def get_course(self, course):
        print("课程：" + course['kcm']+" 课序号"+str(course['kxh']) + " 教师：" + course['skjs'] + " 课余量" + str(course['bkskyl']))
        if course['bkskyl'] > 0 and self.config_into[3] == course['kch'] and self.config_into[4] == course['kxh']:
            kcm = course['kcm']
            kch = course['kch']
            kxh = course['kxh']
            # kcms = self.get_kcms(kcm + "(" + kch + "@" + kxh + ")")
            # token_value = self.get_token()
            self.get_kcms(kcm + "(" + kch + "@" + kxh + ")")
            self.get_token()
            # self.dash()  # 自己尝试打码
            select_data = {
                'dealType': "5",
                'kcIds': kch + '@' + kxh + '@' + self.select,
                'kcms': self.kcms,
                'fajhh': "5519",
                'sj': '0_0',
                'searchtj': '',
                'kclbdm': '704',
                'inputCode': self.code,
                'tokenValue': self.token_value
            }
            try:
                status = self.session.post(url=self.course_selecting_url, data=select_data).text
                print("选课状态：", status)
                return
            except Exception as e:
                print("get_course()出现问题" + str(e))
        else:
            pass

    # 主函数
    def last(self):
        self.getinto()
        self.login()
        count = 1
        while True:
            print("正在进行第{}轮抢课".format(count))
            count += 1
            # 1.查询是否已经选中
            self.check_if_course_select()
            for c in self.course_select:
                if self.config_into[2] in c:
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


if __name__ == '__main__':
    A = qiangke()
    A.last()
