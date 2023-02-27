# -*- coding: utf-8 -*-
# @Time     : 2022/11/15 16:37
# @Author   : Ak4izZ
# @Blog     : https://ark4izz.github.io/
import calendar
import random
import time
import json
import tools.config
import tools.req
import sys
from tools import writer
from tqdm import tqdm


class Spider:
    def __init__(self):
        self.url = {}
        self.config = tools.config.read_config()
        self.url.update({"info": "https://weibo.com/ajax/profile/info?uid="}) # 用户信息
        self.url.update({"blogs_w": "https://weibo.com/ajax/profile/searchblog?uid={}&page={}&feature=0&q={}"}) # 指定内容微博
        self.url.update({"blogs_all": "https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0"})
        self.uid_list = self.config["uid_list"]

    def save_status(self, name, page, uid):  # 保存爬取进度
        self.config["last_status"]["name"] = name
        self.config["last_status"]["page"] = page
        self.config["last_status"]["uid"] = uid
        tools.config.update_config(self.config)

    def load(self):  # 加载上次爬取的进度
        name = self.config["last_status"]["name"]
        page = self.config["last_status"]["page"]
        uid = self.config["last_status"]["uid"]
        return uid, page

    def getinfo(self, uid):
        url = self.url["info"] + uid
        info = tools.req.get_res(url)
        # tqdm.write(info)
        if info == -100:
            sys.exit()
        return info.json()

    def str2time(self, t):  # 切换时间格式
        t = t.split(" ")
        m = list(calendar.month_abbr).index(t[1])
        d = t[2]
        y = t[-1]
        h = t[3]
        TIME = f"{y}-{m}-{d}-{h}"
        return TIME

    def get_blogs(self, uid, page,users):
        global username
        k = self.config["key_word"]
        # since_id = ''
        # tqdm.write("正在爬取", uid, "的博客")
        c = 0
        while 1:
            users.set_description(f"正在爬取第{page}页")
            page_url = self.url['blogs_w'].format(uid, str(page), k)
            url = page_url
            json_data = tools.req.get_res(url).json()

            wait_t = random.randint(1, 6)
            users.set_description(f"正在等待{wait_t}秒")
            time.sleep(wait_t)

            data = json_data['data']
            total = data['total']

            if total == 0:  # 表示当前页面已经是空白
                break  # 循环到下一个用户，页数从头开始
            for blog in data['list']:
                blogs = []  # 这里是列表元素，列表内再套字典
                creat_at = self.str2time(blog['created_at'])  # 帖子发表时间
                text = blog['text_raw']  # 帖子内容
                username = blog['user']['screen_name']
                bid = blog['id']
                if writer.check(bid):
                    blogs.append(dict(uid=uid, bid=bid, name=username, time=creat_at, text=text))
                    c += 1
                    # users.set_description(f"{username}获取贴子数{c}")
                writer.write_txt(blogs)
            page += 1
            self.save_status(uid=uid, name=username, page=page)  # 保存状态

    def start(self):
        uid, page = self.load()
        users=tqdm(self.uid_list[self.uid_list.index(uid):])
        for uid in users:
            tqdm.write(uid)
            userinfo = self.getinfo(uid)
            username = userinfo['data']['user']['screen_name']
            users.write("正在获取  "+username+"  的微博......")
            self.get_blogs(uid, page, users)
            page = 1
        users.write("任务完成！！")


if __name__ == '__main__':
    spider = Spider()
    spider.start()
