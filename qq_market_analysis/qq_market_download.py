#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
从腾讯应用市场下载应用排行榜上的apk,用于分析
'''

__author__ = "lynxz"

import requests, json, os, re
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
        pageObj = json.loads(result)
        if pageObj['success']:
            return pageObj
        else:
            print("json数据异常:", result)
    else:
        print("获取失败")
        # print(result)


def downloadApk(apkUrl, apkName, subFolderName="apkDownload"):
    print("downloadApk.... %s %s" % (apkName, apkUrl))
    targetFolder = os.path.join("./", subFolderName)
    if not os.path.exists(targetFolder):
        os.mkdir(targetFolder)
    targetApkPath = os.path.join(targetFolder, apkName)
    if os.path.exists(targetApkPath):
        print("下载 %s 失败, apk文件已存在,继续下一个apk下载" % apkName)
    else:
        response = session.get(apkUrl)
        if response.status_code == 200:
            with open(targetApkPath, "wb") as f:
                f.write(response.content)
            print("下载 %s 成功" % apkName)
        else:
            print("下载apk: %s 失败: %s" % (apkName, response.status_code))


if __name__ == '__main__':
    appList = []
    columnNames = ["appName", "appId", "categoryName", "fileSize", "appDownCount",
                   "apkUrl", "pkgName", "versionName", "localApkFileName", "minSdkVersion", "targetSdkVersion"]
    excelUtil.initWorkBook(*columnNames)
    for x in range(0, 5):
        retry = 0
        while (retry <= 3):
            retry += 1
            page = getPageInfo(x)
            if page:
                for appInfo in page['obj']:
                    tempFileName = "%s_%s.apk" % (appInfo["appName"], appInfo["appId"])
                    # 文件名中的空格替换为下划线,不然后续执行shell命令时可能会报错
                    space = re.compile("\s+")
                    vline = re.compile("\|")
                    bracket = re.compile("\(|\)")

                    tempFileName = re.sub(space, "_", tempFileName)
                    tempFileName = re.sub(vline, "_", tempFileName)
                    tempFileName = re.sub(bracket, "_", tempFileName)
                    appInfo["localApkFileName"] = tempFileName
                    item = [appInfo.get(x, "") for x in columnNames]
                    appList.append(item)
                    excelUtil.appendItem(*item)
                break
    excelUtil.close()

    print("共抓取app:%s个" % len(appList))
    for app in appList:
        downloadApk(app[5], app[8])
