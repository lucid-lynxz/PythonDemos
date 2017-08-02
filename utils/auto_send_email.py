#! /usr/bin/env python
# coding=utf-8

'''
收发邮件demo
'''

from email.mime.text import MIMEText
from email.header import Header
from email.header import decode_header
from smtplib import SMTP_SSL
import email, imaplib, base64, re

# 邮箱smtp服务器
smtp_server = 'smtp.exmail.qq.com'
imap_server = 'imap.exmail.qq.com'
# sender_qq为发件人的qq号码
email_account = '44***@qq.cn'
# pwd为邮箱密码或者授权码
pwd = 'lynx***'
# 收件人邮箱
receiver = '55***@qq.com'

# 邮件主体
mail_subject = 'python测试'
# 邮件的正文内容
mail_content = 'python登录qq邮箱发邮件测试'


# 对收取的邮件内容进行解码显示,源数据类似: '"=?gb2312?B?zNrRtsbz0rXTys/k?="   <10000@qq.com>'
def decode_mail_info(info):
    # 可能报错: TypeError: expected string or bytes-like object ,比如 撤回邮件时
    # print("==> ", type(info), isinstance(info, (str, bytes)), info)
    if not isinstance(info, (str, bytes)):
        return info

    detail = re.split(r'"\s+', info)
    if len(detail) >= 2:
        detail = detail[1]
    else:
        detail = ""
    all_result = re.findall(r'=\?.*\?=', info)
    result_info = ''
    for index in range(len(all_result)):
        part = all_result[index]
        text, encoding = decode_header(part)[0]
        actualValue = str(text, encoding=str(encoding))
        result_info += actualValue
    result_info += detail
    if len(result_info) == 0:
        result_info = info
    print("result_info = ", result_info)
    return result_info
    # match = re.search(r'=\?.*\?=', info)
    # if match:
    #     result = match.group()
    #     text, encoding = decode_header(result)[0]
    #     actualValue = str(text, encoding=str(encoding))
    #     print("==>", actualValue)
    #     # print("%s -----> %s \n %s" % (text, encoding, actualValue))
    #
    #     # data = result.split(sep='?')
    #     # if len(data) >= 5:
    #     #     src_coding = data[1]
    #     #     cur_coding = data[2]
    #     #     value = data[3]  # =?UTF-8?Q?***?=
    #     #     decode_result = base64.b64decode(value)
    #     #     print("src_coding is : %s , %s , %s , %s" % (src_coding, str(src_coding), decode_result, value))
    #     #     # actualValue = str(decode_result, encoding=str(src_coding)) + detail
    #     #     actualValue = str(b'\xe5\x8d\x87\xe7\xba\xa7', encoding=str(src_coding)) + detail
    #     #     print("ori: %s\tnow: %s" % (info, actualValue))
    #     #     return actualValue
    #     # else:
    #     #     return info
    # else:
    #     print("未找到有效信息 %s " % info)
    #     return info


# 使用指定sender邮箱账号密码,登录到 smtp_server 服务器(smtp服务器,使用ssl),发送邮件给指定receiver
def send_mail_by_smtp_ssl(sender_mail_account='', sender_mail_pwd='',
                          receiver_mail_account='',
                          smtp_server='', ssl_port=465, subject='', content=''):
    # ssl登录
    smtp = SMTP_SSL(smtp_server, port=ssl_port)
    # smtp.set_debuglevel(1)  # 1-开启调试 0-关闭
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
    '''
    search() 搜索指定类型的邮件
    参考: http://blog.csdn.net/longzhiwen888/article/details/46562723
    ALL - 所有邮件
    Recent - 未读邮件,我测试了下貌似无效
    Seen - 已读邮件
    Answered - 已回复的邮件
    '''
    type, data = conn.search(None, 'ALL')  # 搜索匹配目录下的邮件
    # for num in data[0].split():
    #     email_type, email_data = conn.fetch(num, '(RFC822)')
    #     print('Message %s\n%s\n' % (num, email_data[0][1]))
    newList = data[0].split()
    mail_count = len(newList)
    if mail_count == 0:
        print("未搜索到符合条件的邮件")
        return
    # print("总邮件数量: ", mail_count)
    type, data = conn.fetch(newList[mail_count - 1], '(RFC822)')  # 读取最新的邮件信息
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
    # print(data[0][1])
    sender = decode_mail_info(msg.get("From"))  # 发件人
    receiver = decode_mail_info(msg.get("To"))  # 收件人
    subject = decode_mail_info(msg.get('subject'))  # 邮件主题
    date = decode_mail_info(msg.get('date'))  # 邮件时间
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


# send_mail_by_smtp_ssl(email_account, pwd, receiver, smtp_server, 465, mail_subject, mail_content)
get_mail_by_imap_ssl(email_account, pwd, imap_server, 993)
