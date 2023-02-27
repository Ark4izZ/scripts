import os

txt_path = os.getcwd()+os.sep+"data"+os.sep+"data.txt"


def read_txt():
    with open(txt_path, "r", encoding="utf-8") as r:
        blogs = r.read()
        blogs = blogs.split("\n")
        # print(blogs)
        r.close()
        return blogs


def write_txt(blogs):
    with open(txt_path, "a", encoding="utf-8") as f:
        for i in blogs:
            d2w = '{uid}\t{name}\t{bid}\t{time}\t{text}\n'.format(uid=i.get("uid"), bid=i.get("bid"),
                                                                        name=i.get("name"),
                                                                        time=i.get("time"),
                                                                        text=i.get("text").replace("\n", "").replace(
                                                                            '\u200b', ''))
            f.write(d2w)
        f.close()


def check(bid):  # 没有被收录就返回真，否则返回假
    blogs = read_txt()
    for i in blogs:
        if str(bid) in i:
            return False
        else:
            continue
    return True

