#! /usr/bin/env python
# coding=utf-8
'''
自动发送邮件
'''

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# 邮箱smtp服务器
host_server = 'smtp.exmail.qq.com'
# sender_qq为发件人的qq号码
email_account = '44***@qq.com'
# pwd为邮箱密码或者授权码
pwd = '***'
# 收件人邮箱
receiver = '55***@qq.com'

# 邮件的正文内容
mail_content = 'python登录qq邮箱发邮件测试'
# 邮件标题
mail_title = 'python测试'

# ssl登录
smtp = SMTP_SSL(host_server, port=465)
smtp.set_debuglevel(1)  # 1-开启调试 0-关闭
smtp.ehlo(host_server)
smtp.login(email_account, pwd)

msg = MIMEText(mail_content, "plain", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = email_account
msg["To"] = receiver
smtp.sendmail(email_account, receiver, msg.as_string())
smtp.quit()
