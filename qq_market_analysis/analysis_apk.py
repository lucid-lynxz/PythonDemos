#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
分析本目录下 `apkDownload` 中的apk文件,提取最低版本号和target版本号,并追加到相应的excel条目中以便分析
'''

import excel_util as excelUtil
import os

srcFilePath = './qq_market.xlsx'
srcApkFolder = './apkDownload'
jadxPath = '/Users/lynxz/ProgramFiles/jadx-0.6.1/bin/jadx'


# 反编译指定的apk,用于提取manifest,并获得所需参数
def decompilingApk(apkFilePath):
    decompileCmd = '%s -d ./out %s' % (jadxPath, apkFilePath)
    os.system(decompileCmd)


if __name__ == '__main__':
    excelUtil.init()
    pass
