# -*- coding: utf-8 -*-
# @Time     : 2022/11/21 8:05
# @Author   : Ak4izZ
# @Blog     : https://ark4izz.github.io/

new_lines = []
with open("4.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        new_line=[]
        # print(repr(line))
        # line=list(line)
        # break
        tail=line[-6:].split(' ')
        line=line[:-6]+tail[0]+'\t'+tail[-1].strip('\n')
        # print(line)
        # break
        for i in line.split('\t'):
            # print()
            if i!='':
                new_line.append(i)
        new_lines.append(new_line)


with open("new_4.txt", "w", encoding="utf-8") as w:
    for line in new_lines:
        print(repr(line))
        w.write(f'{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}\t{line[4]}\n')

