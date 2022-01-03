# -*- coding: utf-8 -*-
"""
@author: supermantx
@time: 2021/11/12 10:45
发送邮件
"""

import yagmail
import re
import pandas as pd
import os
from TbModel.models import User

def judge_email(target_email):
    """
    邮箱的正则表达式测试
    :param target_email:
    :return:
    """
    match = re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', target_email)
    return match is None


def read_for_name(xh):
    try:
        excel = pd.read_excel("/root/py/体温自动填报plus/resource/导入学生数据.xlsx")
        p = excel.loc[lambda x: x['学号'] == xh]
        if p is None:
            return False
        print(p)
        return p['姓名'].item()
    except Exception:
        Exception.with_traceback()


def re_email(target, xh, pwd):
    if judge_email(target):
        Exception('邮件名错误')
    name = read_for_name(xh)
    print(name.__str__())
    if name is False:
        Exception("账户错误")
    user = User(email=target, username=xh, password=pwd, name=name)
    user.save()
    yag = yagmail.SMTP(user='13584894459@163.com', password='BQIHFXEJAFZTEDYG', host='smtp.163.com')
    # yag.send('3170803065@qq.com', 'test', 'test')
    yag.send(target, '注册成功回信',
             '<h1>恭喜' + xh + "," + name + '注册服务成功<h1><hr><h2>本服务为sylu的学生提供免费'
                                          '的体温填报服务,'
                                          '每日中午10点自动填报以及健康日报并提供邮箱提醒</h2>'
                                          '<hr><h3>赞助一下可怜的开发者把</h3>'
                                          '<a href=\"http://121.5.21.159:8000/static/money.jpg\">赞助链接</a>')


def send_email(target, content):
    """
    :param target:
    :param content: dict("title", "content")
    :return:
    """
    yag = yagmail.SMTP(user='13584894459@163.com', password='BQIHFXEJAFZTEDYG', host='smtp.163.com')
    # yag.send('3170803065@qq.com', 'test', 'test')
    yag.send(target, content['title'], content['content'])
