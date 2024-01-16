#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 海
@Created on: 2024/1/4
@file: email_sender.py
@Description:
邮件发送服务
"""
__version__ = "0.0.1"
__link__ = "https://github.com/Singhoy/EmailSender"

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
from typing import List


class EmailSender:
    def __init__(self, sender_email, smtp_server, smtp_port, smtp_username, smtp_password):
        # 邮件信息
        self.sender_email = sender_email  # 寄件人邮箱地址
        self.smtp_server = smtp_server  # SMTP服务器地址
        self.smtp_port = smtp_port  # SMTP服务器端口
        self.smtp_username = smtp_username  # SMTP登陆账号
        self.smtp_password = smtp_password  # SMTP授权码
    
    @staticmethod
    def add_attachment(filename, message):
        # 添加附件
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            
            message.attach(part)
        return message
    
    def send_email(self, receiver_email, subject, body, _subtype: str = 'plain', filename: str = None, cc: List = None):
        message, send_list = self.make_message(body, receiver_email, subject, _subtype, cc)
        if filename is not None:
            message = self.add_attachment(filename, message)
        self.sender(message, send_list)
    
    def make_message(self, body, receiver_email, subject, _subtype, cc):
        # 创建邮件对象
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        send_list = [receiver_email]  # 收件人邮箱
        # 添加抄送
        if cc:
            send_list += cc
            message['Cc'] = ', '.join(cc)
        # 添加正文
        message.attach(MIMEText(body, _subtype, _charset='utf-8'))
        return message, send_list
    
    def sender(self, message, to_s):
        # 发送邮件
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = message.as_string()
            server.sendmail(self.sender_email, to_s, text)
            print('邮件发送成功')
            sleep(3)
