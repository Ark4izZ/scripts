# -*- coding: utf-8 -*-
# @Time     : 2022/11/15 16:57
# @Author   : Ak4izZ
# @Blog     : https://ark4izz.github.io/
import json


def read_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            conf = json.load(f)
            return conf
    except FileNotFoundError:
        print("无法找到config，请检查文件路径")
        return None


def update_config(new_conf):
    try:
        with open("config.json", "w+", encoding="utf-8") as f:
            json.dump(new_conf, f, indent=4, sort_keys=True, ensure_ascii=False)
    except Exception as e:
        print(type(e))
        print(e)



