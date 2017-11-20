#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
python解析xml
sax会逐行解析
dom则一次性读取整个xml文件
[Python3 XML解析](http://www.runoob.com/python3/python3-xml-processing.html)
'''

import xml.dom.minidom

domTree = ""
domElement = ''
srcXmlFilePath = './AndroidManifest.xml'


def initDomTree(srcFile=srcXmlFilePath):
    global domTree, domElement
    if not domTree:
        domTree = xml.dom.minidom.parse(srcFile)
        domElement = domTree.documentElement


def getTagValue(tag, attribute):
    global domElement
    initDomTree()
    tagList = domElement.getElementsByTagName(tag)
    for tagInfo in tagList:
        # tagStr = tagInfo.toxml()
        # print(tagStr)
        attributeValue = tagInfo.getAttribute(attribute)
        return attributeValue
    else:
        print("找不到 %s 值" % tag)
        return ""


if __name__ == "__main__":
    minSdk = getTagValue("uses-sdk", 'android:minSdkVersion')
    targetSdk = getTagValue("uses-sdk", 'android:targetSdkVersion')
    print("minSdk = ", minSdk, "targetSdk = ", targetSdk)