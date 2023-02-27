# -*- coding: utf-8 -*-
# @Time     : 2022/11/17 17:12
# @Author   : Ak4izZ
# @Blog     : https://ark4izz.github.io/
import json
import random
import time

import tools.config
from wbSpider.tools import req


def read_users():
    with open("username_list.txt", "r", encoding="utf-8") as f:
        content = f.read()
        username_list = content.split("、")
        return username_list


def update_uid_list(new_uid_list):
    config = tools.config.read_config()
    if config is None:
        config={"uid_list": []}
    for uid in new_uid_list:
        if uid["uid"] not in config['uid_list']:
            config['uid_list'].append(uid["uid"])
    print(config)
    tools.config.update_config(config)


class UidCollector:
    def __init__(self):
        self.users = read_users()
        self.uid_list = self.get_uid()

    def get_uid(self):
        uid_list = []
        failed_user = []
        for user in self.users:
            time.sleep(random.randint(1, 4))
            print(user)
            try:
                url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{user}&page_type=searchall"
                # print(url)
                res = req.get_res(url=url)
                data = json.loads(res)
                uid = data['data']['cards'][0]['card_group'][0]['user']['id']
                uid_list.append(dict(name=user, uid=uid))
            except KeyError:
                failed_user.append(user)
                print("获取", user, '的uid失败，请手动添加')
            continue
        print("获取失败的用户：", failed_user)
        return uid_list  # 返回一个[{name:uid},{name,uid}]形式的列表


if __name__ == "__main__":
    uc=UidCollector()
    # update_uid_list([{"name": "我", "uid":"11111"}, {"name":"你", "uid":"2"}, {"name":"他", "uid":"3"}])
    update_uid_list(uc.uid_list)