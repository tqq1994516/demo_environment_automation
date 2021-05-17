# coding:utf-8
import configparser
import os
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.header import Header


def send_email(file):
    config = configparser.ConfigParser()
    file_path = os.getcwd() + '/config/config.ini'
    config.read(file_path)
    email_host = config.get("emailInfo", "email_host")
    send_user = config.get("emailInfo", "send_user")
    password = config.get("emailInfo", "password")
    to_users = config.get("emailInfo", "to_users").split(',')
    send_header = config.get("emailInfo", "send_header")
    rq = str(date.today())
    email_title = rq + "演示环境测试报告"
    with open(file, "r", encoding="utf-8") as f:
        mail_body = f.read()
    tips = "以下为概要报告，由于手机浏览器解析原因存在显示异常情况推荐电脑查看，<br>如需查看详细报告请访问以下网址：http://122.112.243.85:10115<br>Tips：导航栏下方’En‘按钮可切换语言,可重点关注【功能】与【图表】模块"
    message = MIMEText(_text=tips + mail_body, _subtype='html', _charset='utf-8')
    message['Subject'] = Header(email_title, "utf-8")
    message['From'] = Header(send_header, "utf-8")
    # 因为收件人列表是;分割
    message['To'] = ";".join(to_users)
    with smtplib.SMTP_SSL(host=email_host, port=465, timeout=10) as server:
        server.login(send_user, password)
        server.sendmail(send_user, to_users, message.as_bytes())
