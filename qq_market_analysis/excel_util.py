#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openpyxl
import openpyxl.utils
from openpyxl import Workbook
from openpyxl.compat import range
import time

wb = Workbook()
columnSize = 0
targetFileName = 'qq_market.xlsx'


def getWorkBook(fileName=targetFileName):
    global wb, targetFileName
    targetFileName = fileName
    try:
        wb = openpyxl.load_workbook(targetFileName)
    except FileNotFoundError as e:
        print("FileNotFoundError ", e)
        wb = Workbook(fileName)
        wb.save(fileName)
        wb = openpyxl.load_workbook(fileName)


# 初始化excel操作, 写入列名称
def initWorkBook(*columnName, fileName="qq_market.xlsx"):
    print("excel_util initWorkBook")
    global wb, columnSize
    getWorkBook(fileName)

    # 删除工作表,从最后一张表开始删除
    sheetNames = wb.get_sheet_names()  # 获取所有的工作表名
    sheetCount = len(sheetNames)
    print("总共有 %s 张表" % sheetCount)
    if sheetCount >= 1:
        for index in range(sheetCount - 1, -1, -1):
            print("正在删除表 %s" % sheetNames[index])
            wb.remove_sheet(wb[sheetNames[index]])
            # wb.remove(wb.get_sheet_by_name(sheetNames[index]))
        print("删除操作过后,总共有 %s 张表" % len(wb.get_sheet_names()))

    # 创建新表并写入列名
    columnSize = len(columnName)
    sheet = wb.create_sheet("market_%s" % (time.strftime("%Y%m%d%H%M%s", time.localtime(time.time()))))
    print("创建表名:%s  %s" % (sheet.title, columnSize))
    if columnSize > 0:
        try:
            for x in range(0, columnSize):
                columnIndex = x + 1
                # print("currentIndex=", columnIndex, columnSize, columnName[x])
                sheet.cell(row=1, column=columnIndex).value = "%s" % columnName[x]
        except Exception as e:
            print("error", e)
    wb.save(fileName)
    wb.close()


# 在表格的下一行追加一行数据
def appendItem(*info):
    global wb, targetFileName
    getWorkBook(targetFileName)
    sheetNames = wb.get_sheet_names()  # 获取所有的工作表名
    sheetCount = len(sheetNames)
    if sheetCount >= 1:
        sheet = wb[sheetNames[sheetCount - 1]]
        sheet.append(info)
        wb.save(targetFileName)
    else:
        wb.close()


def close():
    global wb
    if wb:
        wb.save(targetFileName)
        wb.close()

# initWorkBook(*[x for x in range(1, 10)])
# appendItem(*["hello", "hello", "hello", "hello", "hello"])
