#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
从腾讯应用市场下载应用排行榜上的apk,用于分析
'''

__author__ = "lynxz"

import requests, json
# from .excel_util import *
import excel_util as excelUtil

baseUrl = "http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=0&pageSize=20&pageContext=%s"
session = requests.session()


def getPageUrl(pageIndex=0):
    return baseUrl % (pageIndex * 20)


def getPageInfo(pageIndex=0):
    url = getPageUrl(pageIndex)
    print("目标url为: ", url)
    response = session.get(url)
    result = response.text
    if response.status_code == 200:
        print("获取成功 %s" % pageIndex)
    else:
        print("获取失败")
    print(result)
    return result


'''
打算存储的信息:
appName
fileSize
appDownCount
categoryName
apkUrl
pkgName
versionName
'''

excelUtil.initWorkBook(*["hello", "hello"])
# getPageInfo(3)