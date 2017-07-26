# _*_ coding: utf-8 _*_
import urllib.error

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

try:
    # html = urlopen("http://cn.bing.com/")
    # html = urlopen("http://pythonscraping.com/pages/page1.html")
    # print(html.read())
    # bsObj = BeautifulSoup(html.read(), "lxml")
    context = b'<html>\n<head>\n<title>A Useful Page</title>\n</head>\n<body>\n<h1>An Interesting Title</h1>\n<div>\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n</div>\n</body>\n</html>\n'
    bsObj = BeautifulSoup(context, "lxml")
    nameList = bsObj.find_all("title", {"id": 'hello'})  # 查找所有包含指定属性的 title 标签
    for name in nameList:
        print(name.get_text())
    try:
        print(bsObj.h1)
    except AttributeError as e:
        print("tag not found")
    else:
        print("tag h1 is exist")
except urllib.error.HTTPError as e:
    print("exception %s" % e)
else:
    print("not error occur")
finally:
    print("finally code")

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html, 'lxml')
for link in bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])

print(".........")
# import datetime
# import random
#
# random.seed(datetime.datetime.now())
# def getLinks(articleUrl):
#     html = urlopen("http://en.wikipedia.org" + articleUrl)
#     bsObj = BeautifulSoup(html, "lxml")
#     return bsObj.find("div", {"id": "bodyContent"}) \
#         .findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
#
#
# links = getLinks("/wiki/Kevin_Bacon")
# while len(links) > 0:
#     newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
#     print(newArticle)
#     links = getLinks(newArticle)
