#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

'''
range()功能demo
range(from,to,step) => [from,to) 包含from,不包含to
不指定时,默认从 0~(to-1) ,步长为1
'''

for x in range(5):
    print(x)  # 0 1 2 3 4

for x in range(1, 5):
    print(x)  # 1 2 3 4

for x in range(1, 5, 2):
    print(x)  # 1 3
