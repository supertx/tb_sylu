"""
@author: supermantx
@time: 2021/11/12 10:26
@author: supermantx
@time: 2021/3/11 8:55
尝试自动填报每日温度
"""

from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from 体温自动填报plus.util import send_email
import requests
import datetime

dt = datetime.datetime


def tb(Uid, Pwd):
    # 提交信息得请求头
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    # 登陆时的用户名和密码
    url = "http://xg.sylu.edu.cn/SPCP/Web"
    session = HTMLSession()
    r = session.get(url)
    # r.html.render()
    # print(r.html.html)
    soup = bs(r.text, "html.parser")
    code = soup.find_all(id="code-box")[0].string
    hidden_code = soup(attrs={"type": "hidden"})
    ReSubmiteFlag = hidden_code[0].attrs["value"]
    StuLoginMode = hidden_code[1].attrs["value"]
    # with open("stuText.txt", "r", encoding="utf8") as info:
    #     try:
    #         Uid = info.readline()[:-1]
    #         Pwd = info.readline()
    #     except:
    #         pass
    # Uid = '1903050419'
    # Pwd = '016319'
    data = "ReSubmiteFlag=" + ReSubmiteFlag + "&StuLoginMode=1&txtUid=" + Uid + "&txtPwd=" + Pwd + "&codeInput=" + code
    post = requests.post(url, headers=headers, data=bytes(data, "utf-8"))
    # print(post.cookies)
    cookie = post.request.headers['Cookie']
    print(cookie)
    url = url + "/Temperature/StuTemperatureInfo"
    headers.update({"Upgrade-Insecure-Requests": "1", "Cookie": cookie})
    data2 = "TimeNowHour=10&TimeNowMinute=10&Temper1=36&Temper2=6&ReSubmiteFlag=" + ReSubmiteFlag
    post = requests.post(url, headers=headers, data=bytes(data2, "utf-8"))


def tb_ultimate():
    with open("/root/py/体温自动填报plus/resource/stuInfo.txt", 'r') as info:
        lines = info.readlines()
        print(lines)
        for line in lines:
            if line[-1] == '\n':
                line = dict(eval(line[:-1]))
            else :
                line = dict(eval(line))
            print(line['username'])
            print(line['password'])
            now = dt.now()
            print(now)
            tb(line['username'], line['password'])
            send_email.send_email(line['email'],
                                  {'title': '每日体温填报',
                                   'content': '<h1>用户' + send_email.read_for_name(
                                       line['username']) + '</h1><hr><h1>{0}/{1}/{2} {3}:{4}, 体温填报成功</h1>'.format(
                                       now.year, now.month, now.day, '10', now.minute)})

        # while line is not None:
        #
        #     tb(line['username'], line['password'])
        #     now = dt.now()
        #     line = eval(info.readline())
        #     print(line)
        #     # send_email.send_email(line['email'],
        #     #                       {'title': '每日体温填报',
        #     #                        'content': '<h1>用户' + send_email.read_for_name(
        #     #                            line['username']) + '</h1><hr><h1>{0}/{1}/{2} {3}:{4}, 体温填报成功</h1>'.format(
        #     #                            now.year, now.month, now.day, now.hour, now.minute)})

def tb_report():
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}

if __name__ == '__main__':
    tb_ultimate()