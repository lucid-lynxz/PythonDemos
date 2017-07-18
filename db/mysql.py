#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

'''
使用python操作mysql数据库:增删改查
参考: http://www.cnblogs.com/woider/p/5926744.html
'''

import pymysql

# 连接到指定的mysql数据库
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='lynx@333',
                             db='py_demo',
                             charset='utf8')

cursor = connection.cursor()
version = cursor.execute("select version()")
data = cursor.fetchone()
print(version, data)


# 执行指定的sql语句
def executeSql(sql_cmd, is_query_action=False):
    try:
        # 执行sql语句item
        cursor.execute(sql_cmd)
        # 提交到数据库
        connection.commit()
        if is_query_action:
            # 获取所有记录
            '''
            fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
            fetchall(): 接收全部的返回结果行.
            rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
            '''
            result = cursor.fetchall()
            for item in result:
                fname = item[0]
                lname = item[1]
                age = item[2]
                sex = item[3]
                income = item[4]
                print("fname is : %s ,lanme is %s,income = %s" % (fname, lname, income))
    except:
        # 如果发生错误则回滚
        print("error while execute command: %s , rollback..." % sql_cmd)
        connection.rollback()


# 删除表
# sql_delete_table = 'DROP TABLE IF EXISTS EMPLOYEE'

# 创建表
sql_create_table = "CREATE TABLE if NOT EXISTS EMPLOYEE (FIRST_NAME CHAR(20) NOT NULL,LAST_NAME CHAR(20),AGE INT,SEX CHAR(1),INCOME FLOAT )"
executeSql(sql_create_table)

#  插入数据
sql_insert_data = "INSERT INTO EMPLOYEE (FIRST_NAME,LAST_NAME, AGE, SEX, INCOME) VALUES ('Mac1', 'Mohan', 20, 'W', 2304)"
executeSql(sql_insert_data)

# 查询操作
sql_query = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
executeSql(sql_query, True)

# 更新数据
sql_update = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('W')
executeSql(sql_update)

# 删除数据项
sql_delete = "DELETE FROM EMPLOYEE WHERE AGE >= '%d'" % (21)
executeSql(sql_delete)

# 关闭数据库
connection.close()