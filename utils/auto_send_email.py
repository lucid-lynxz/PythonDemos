#! /usr/bin/env python
# coding=utf-8

'''
收发邮件demo
'''

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import email, imaplib, base64, re

# 邮箱smtp服务器
smtp_server = 'smtp.exmail.qq.com'
imap_server = 'imap.exmail.qq.com'
# sender_qq为发件人的qq号码
email_account = '55**@qq.com'
# pwd为邮箱密码或者授权码
pwd = '***'
# 收件人邮箱
receiver = '44**@qq.com'

# 邮件主体
mail_subject = 'python测试'
# 邮件的正文内容
mail_content = 'python登录qq邮箱发邮件测试'


# 对收取的邮件内容进行解码显示,源数据类似: '"=?gb2312?B?zNrRtsbz0rXTys/k?="   <10000@qq.com>'
def decode_mail_info(info):
    detail = re.split(r'\s+', info)
    if len(detail) >= 2:
        detail = detail[1]
    else:
        detail = ""

    match = re.search(r'=\?.*\?=', info)
    if match:
        result = match.group()
        data = result.split(sep='?')
        if len(data) >= 5:
            src_coding = data[1]
            cur_coding = data[2]
            value = data[3]
            decode_result = base64.b64decode(value)
            actualValue = str(decode_result, str(src_coding)) + detail
            print("ori: %s\tnow: %s" % (info, actualValue))
            return actualValue
    else:
        print("未找到有效信息 %s " % info)


# 使用指定sender邮箱账号密码,登录到 smtp_server 服务器(smtp服务器,使用ssl),发送邮件给指定receiver
def send_mail_by_smtp_ssl(sender_mail_account='from@gmail.com', sender_mail_pwd='',
                          receiver_mail_account='lucid_lynxz@gmail.com',
                          smtp_server='', ssl_port=465, subject='from python', content='hello'):
    # ssl登录
    smtp = SMTP_SSL(smtp_server, port=ssl_port)
    smtp.set_debuglevel(1)  # 1-开启调试 0-关闭
    smtp.ehlo(smtp_server)
    smtp.login(sender_mail_account, sender_mail_pwd)

    msg = MIMEText(content, "plain", 'utf-8')
    msg["Subject"] = Header(subject, 'utf-8')
    msg["From"] = sender_mail_account
    msg["To"] = receiver_mail_account
    smtp.sendmail(sender_mail_account, receiver_mail_account, msg.as_string())
    smtp.quit()


# 收取邮件,参考: http://blog.csdn.net/q932104843/article/details/52502447
def get_mail_by_imap_ssl(email_account='', email_pwd='', imap_server='', ssl_port=993):
    conn = imaplib.IMAP4_SSL(host=imap_server, port=ssl_port)  # 如果未启用ssl,使用 imaplib.IMAP4(...)
    conn.login(email_account, email_pwd)
    conn.select()  # 选择指定的文件夹,默认为 INBOX , 按时间先后顺序读取
    type, data = conn.search(None, 'ALL')  # 搜索匹配目录下的邮件
    newList = data[0].split()
    type, data = conn.fetch(newList[0], '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    '''
    b'Date: Mon, 12 Dec 2016 17:41:30 +0800\r\n
    From: "=?gb2312?B?zNrRtsbz0rXTys/k?=" <10000@qq.com>\n
    To: "=?gb2312?B?zNrRtsbz0rXTys/k08O7pw==?="\n
    Subject: =?gb2312?B?u7bTrcq508PM2tG2xvPStdPKz+Q=?=\n
    X-QQ-STYLE: 1\n
    Content-Type: text/html;\n
    charset="gb2312"\n\n
    <!DOCTYPE html*****n'
    '''
    print(data[0][1])
    sender = decode_mail_info(msg.get("From"))
    receiver = decode_mail_info(msg.get("To"))
    subject = decode_mail_info(msg.get('subject'))
    conn.close()
    conn.logout()
    # msg.get('subject') 得到的邮件主体内容: =?gb2312?B?u7bTrcq508PM2tG2xvPStdPKz+Q=?=
    # 参考: http://blog.renren.com/share/222201157/12379181045 得到如下分解含义:
    # =?  ....  ?= 表示开头和结束标识符,不同参数使用?分隔
    # gb2312 表示原始编码
    # B 表示现在的编码 'B-encoding'，也就是base64的意思
    # u7bTrcq508PM2tG2xvPStdPKz+Q= 为编码后的值
    # 解码方法:
    # echo u7bTrcq508PM2tG2xvPStdPKz+Q= | base64 -D | iconv -f gbk -t utf-8

    # for num in data[0].split():
    #     email_type, email_data = conn.fetch(num, '(RFC822)')
    #     print('Message %s\n%s\n' % (num, email_data[0][1]))


send_mail_by_smtp_ssl(email_account, pwd, receiver, smtp_server, 465, mail_subject, mail_content)
get_mail_by_imap_ssl(email_account, pwd, imap_server, 993)
