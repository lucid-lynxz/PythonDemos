#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
分析本目录下 `apkDownload` 中的apk文件,提取最低版本号和target版本号,并追加到相应的excel条目中以便分析
'''

import excel_util as excelUtil
import os
import xml.dom.minidom

srcFilePath = './qq_market.xlsx'
srcApkFolder = './apkDownload'
aaptPath = '/Users/lynxz/Applications/AndroidSDK/build-tools/26.0.2/aapt'

tagName = 'uses-sdk'
tagMinSdkVersion = "android:minSdkVersion"
tagTargetSdkVersion = "android:targetSdkVersion"


# 十六进制 to 十进制
def hex2dec(string_num):
    string_num = string_num.replace("\n", "")
    return str(int(string_num.upper(), 16))


# 反编译指定的apk,用于提取manifest,并获得所需参数
def getInfoFromManifest(apkFilePath, attributeName):
    global aaptPath
    if not os.path.exists(apkFilePath):
        print("apk文件不存在,请检查后重试 %s" % apkFilePath)
        return ""
    elif os.path.getsize(apkFilePath) <= 10000:
        print("文件过小,请检查后再试 %s" % apkFilePath)
        return ""

    print("正在反编译 %s" % apkFilePath)
    decompileCmd = '%s list -a %s |grep %s' % (aaptPath, apkFilePath, attributeName)
    # result = os.system(decompileCmd)
    # 需要删除可能存在的换行符,避免十六进制转换时异常
    result = os.popen(decompileCmd).read()
    # print("result", result)
    # 需要考虑manifest中有多个相同tag的情况
    splitArr = result.split("\n")[0].replace("\n", "").split("0x10)")
    if len(splitArr) > 1:
        try:
            value = hex2dec(splitArr[1])
        except ValueError as e:
            print(e)
            return ""
    else:
        print("split length <= 1", result)
        value = ""
        # value = hex2dec(splitArr[0])
    # print(result)
    print("%s value is: %s" % (attributeName, value))
    return value


if __name__ == '__main__':
    allItem = excelUtil.getAllItemList()
    for item in allItem:
        apkName = item['localApkFileName']
        # if "天猫_208787" in apkName:
        apkPath = os.path.join(srcApkFolder, apkName)
        if os.path.exists(apkPath):
            minSdkVersion = getInfoFromManifest(apkPath, tagMinSdkVersion)
            targetSdkVersion = getInfoFromManifest(apkPath, tagTargetSdkVersion)
            # minSdkVersion = getAttribute(tagName, tagMinSdkVersion)
            # targetSdkVersion = getAttribute(tagName, tagTargetSdkVersion)
            # print("minSdkVersion = ", minSdkVersion, "tagTargetSdkVersion = ", targetSdkVersion)
            excelUtil.appendInfo('', item['row_index'], minSdkVersion, 'minSdkVersion')
            excelUtil.appendInfo('', item['row_index'], targetSdkVersion, 'targetSdkVersion')
        else:
            print("%s 不存在,下一个" % apkPath)
            # break
