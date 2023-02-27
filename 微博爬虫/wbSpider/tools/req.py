# -*- coding: utf-8 -*-
# @Time     : 2022/11/17 17:31
# @Author   : Ak4izZ
# @Blog     : https://ark4izz.github.io/
import requests
#  -100 cookie过期


cookies = {
    'UOR': 'www.google.com,weibo.com,www.google.com',
    'SINAGLOBAL': '6966175749310.459.1668385075197',
    'PC_TOKEN': '0868b61aaf',
    'SCF': 'AvdGO91vd4Em-689kt8-puGwV9ZyA9zmbkbDTwlErtlSkS4dWontUwwo1DkIAttWJMFJi0w3JXEKRbQah2gpOQs.',
    'SUB': '_2A25OfBwKDeRhGeBP6lcY8ijKzTmIHXVtCArCrDV8PUJbmtAKLW7MkW9NRW63O2eQygL8Dk4XkH3G_7O-mCJCP-HU',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFuCDln6ydKV_T3f34VmNxm5JpX5K-hUgL.FoqpeK-4eoqcSo-2dJLoI7yNUNM_9s8XqBtt',
    'ALF': '1700357327',
    'SSOLoginState': '1668836442',
    'XSRF-TOKEN': '6GLzKilp4Q3F7wXHDxu3ydts',
    '_s_tentry': 'weibo.com',
    'Apache': '5169647947104.501.1668836451314',
    'ULV': '1668836451395:9:9:9:5169647947104.501.1668836451314:1668676684118',
    'WBPSESS': 'sjwj-ekA2wA2yELzu6mmyK0MUuapStRuOSm5rF2dwt2lYIHbfh0bhk9NNyu7X4GIrDXPr3kkA3Dr4b4vNU2cYMnlxEPRJRFm_bUrS5a7i3Ls7qtKAT7x2j5CdUcVfPUN-TRgaCN2kfn-_TOPb4KLaw==',
}

headers = {
    'authority': 'weibo.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,es;q=0.8',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'UOR=www.google.com,weibo.com,www.google.com; SINAGLOBAL=6966175749310.459.1668385075197; PC_TOKEN=0868b61aaf; SCF=AvdGO91vd4Em-689kt8-puGwV9ZyA9zmbkbDTwlErtlSkS4dWontUwwo1DkIAttWJMFJi0w3JXEKRbQah2gpOQs.; SUB=_2A25OfBwKDeRhGeBP6lcY8ijKzTmIHXVtCArCrDV8PUJbmtAKLW7MkW9NRW63O2eQygL8Dk4XkH3G_7O-mCJCP-HU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFuCDln6ydKV_T3f34VmNxm5JpX5K-hUgL.FoqpeK-4eoqcSo-2dJLoI7yNUNM_9s8XqBtt; ALF=1700357327; SSOLoginState=1668836442; XSRF-TOKEN=6GLzKilp4Q3F7wXHDxu3ydts; _s_tentry=weibo.com; Apache=5169647947104.501.1668836451314; ULV=1668836451395:9:9:9:5169647947104.501.1668836451314:1668676684118; WBPSESS=sjwj-ekA2wA2yELzu6mmyK0MUuapStRuOSm5rF2dwt2lYIHbfh0bhk9NNyu7X4GIrDXPr3kkA3Dr4b4vNU2cYMnlxEPRJRFm_bUrS5a7i3Ls7qtKAT7x2j5CdUcVfPUN-TRgaCN2kfn-_TOPb4KLaw==',
    'pragma': 'no-cache',
    'referer': 'https://s.weibo.com/',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}


def get_res(url):

    res=requests.get(url, headers=headers, cookies=cookies)

    if '"ok":-100' in res.content.decode():
        print("cookie信息失效！！")
        return -100
    return res


# res=get_res("https://weibo.com/ajax/profile/searchblog?uid=2343014623&page=45&feature=0&q=%E4%B9%8C")
# print(res.content.decode())