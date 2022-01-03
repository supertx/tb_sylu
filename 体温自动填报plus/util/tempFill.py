"""
@author: supermantx
@time: 2021/11/12 10:26
@author: supermantx
@time: 2021/3/11 8:55
尝试自动填报每日温度
"""

from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import re
from 体温自动填报plus.util import send_email
from TbModel.models import User
import requests
import datetime
from urllib import parse
from paddleocr import PaddleOCR
import time
dt = datetime.datetime
ocr = PaddleOCR()
temp_file_name = "temp.png"


def get_cookie(uid, pwd):
    # 提交信息得请求头
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    url = "http://xg.sylu.edu.cn/SPCP/Web"
    session = HTMLSession()
    r = session.get(url)
    soup = bs(r.text, "html.parser")
    code = soup.find_all(id="code-box")[0].string
    hidden_code = soup(attrs={"type": "hidden"})
    ReSubmiteFlag = hidden_code[0].attrs["value"]
    data = "ReSubmiteFlag=" + ReSubmiteFlag + "&StuLoginMode=1&txtUid=" + uid + "&txtPwd=" + pwd + "&codeInput=" + code
    post = requests.post(url, headers=headers, data=bytes(data, "utf-8"))
    return post.request.headers['Cookie'], ReSubmiteFlag


def tb(cookie, ReSubmiteFlag):
    # 提交信息得请求头
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    # 登陆时的用户名和密
    url = "http://xg.sylu.edu.cn/SPCP/Web/Temperature/StuTemperatureInfo"
    headers.update({"Upgrade-Insecure-Requests": "1", "Cookie": cookie})

    data2 = "TimeNowHour=10&TimeNowMinute=10&Temper1=36&Temper2=6&ReSubmiteFlag=" + ReSubmiteFlag
    post = requests.post(url, headers=headers, data=bytes(data2, "utf-8"))
    return cookie


@DeprecationWarning
def tb_ultimate_old():
    with open("/root/py/体温自动填报plus/resource/stuInfo.txt", 'r') as info:
        lines = info.readlines()
        print(lines)
        for line in lines:
            if line[-1] == '\n':
                line = dict(eval(line[:-1]))
            else:
                line = dict(eval(line))
            now = dt.now()
            # cookie = tb(line['username'], line['password'])
            # parser_info(cookie)
            # send_email.send_email(line['email'],
            #                       {'title': '每日体温填报',
            #                        'content': '<h1>用户' + send_email.read_for_name(
            #                            line['username']) + '</h1><hr><h1>{0}/{1}/{2} {3}:{4}, 体温填报成功</h1>'.format(
            #                            now.year, now.month, now.day, '10', now.minute)})


def tb_ultimate():
    users = User.objects.all()
    for user in users:
        try:
            now = dt.now()
            tup = get_cookie(user.username, user.password)
            tb(tup)
            tb_report(tup[0], user)
            send_email.send_email(user.email,
                                  {'title': '每日体温以及日报填报完成',
                                   'content': '<h1>用户' + user.name + '</h1><hr><h1>{0}/{1}/{2} {3}:{4}, 体温填报成功</h1><br>'
                                                                     '<h1>填报系统重要更新,日报填写是按照之前已经填写的信息重新填报,如果出现信息变更请及时和开发者联系,开发者qq:1374411672</h1><br>'
                                                                     '<h1>祝大家虎年事事如意,2022年心想事成</h1><br>'+
                                                                     '<h1>这个验证码验证是真的烦</h1>'
                                                                     '<h1><a href="http://121.5.21.159:8000/static/money.jpg">开发者赞助链接(复制到浏览器里打开)</a></h1>'.format(
                                       now.year, now.month, now.day, now.hour + 8, now.minute)})
            # send_email.send_email(user.email,
            #                       {'title': '每日体温以及日报填报完成',
            #                        'content': """"""})
            # break
        except Exception as e:
            # e.with_traceback()
            continue


def parser_info(cookie, user):
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    url = "http://xg.sylu.edu.cn/SPCP/Web/Report/Index"
    headers.update({"Referer": "http://xg.sylu.edu.cn/SPCP/Web/Account/ChooseSys", "Cookie": cookie})
    html = requests.get(url, headers=headers).text
    soup = bs(html, "html.parser")
    raw_basic_info = soup.find_all('input')
    data = {}
    # 省份数字未处理
    for info in raw_basic_info:
        # info = basic_info.find('input')
        if info is None:
            continue
        if 'name' not in info.attrs.keys() or ('checked' in info.attrs.keys() and info.attrs['checked'] != 'checked'):
            continue
        if info.attrs['name'] == "VCcode":
            continue
        data.update({info.attrs['name']: info.attrs['value']})
    # print(data)
    # 处理pzdata
    PZdata = [{'TitleId': '926853bd-6292-48ef-b554-0ea0cb99b808', 'OptionName': '是', 'Selectid': 'e2f169d0-0778-4e3e-8ebf-64ce5a44f307', 'OptionType': 0}, {'TitleId': '5c2ddaef-1cf4-4995-921c-de1585e71fe1', 'OptionName': '否', 'Selectid': 'c8ecb725-9788-4ed0-b9d2-4be23444ce3e', 'OptionType': 0}, {'TitleId': '6f95a926-c6d6-4fa7-9d74-fbcfcd79ec7b', 'OptionName': '否', 'Selectid': 'a884f81e-f401-451d-9f3d-0526aa886feb', 'OptionType': 0}, {'TitleId': '6cd479f3-dd6a-4bab-809a-3abdf28e5a46', 'OptionName': '否', 'Selectid': '62ad9bed-3201-4607-b845-5e279a0311d0', 'OptionType': 0}, {'TitleId': 'e6f578a6-6a0d-4b17-a18f-f1de3cb81d29', 'OptionName': '否', 'Selectid': '57722ddd-3093-4978-86da-1213420f36c4', 'OptionType': 0}, {'TitleId': '23dfd17a-84b0-462c-a27d-fbafbe670278', 'OptionName': '否', 'Selectid': 'c6bcc8ce-86f1-404c-b7f8-ac583d899c75', 'OptionType': 0}, {'TitleId': '0428ad6d-0c14-4c38-81fb-dc6928ae6608', 'OptionName': '否', 'Selectid': '12727e9b-cd2f-413e-ae30-36adafd5203f', 'OptionType': 0}, {'TitleId': '85e00a79-176f-4fcf-8d14-8bb14075d51f', 'OptionName': '否', 'Selectid': 'e0559a52-d3d1-4203-ac9a-d221506a507f', 'OptionType': 0}, {'TitleId': 'bd5a0708-79a3-4c92-a978-03aba2dac8a8', 'OptionName': '否', 'Selectid': 'c16d5a27-5923-43d8-b6a6-d5733803490b', 'OptionType': 0}, {'TitleId': '91d7f9a5-aed8-462f-81f5-9d339c3f2d3a', 'OptionName': '否', 'Selectid': '3a5fbe75-7bf4-4b6d-93f1-f561dbbf0ead', 'OptionType': 0}, {'TitleId': '025d0800-de7d-45e3-b2b4-c240bec5aa51', 'OptionName': '否', 'Selectid': '3a36a22f-5af7-4b48-a472-7df55a8ba374', 'OptionType': 0}, {'TitleId': '0827f0a0-60eb-4c62-9741-d742bf569ece', 'OptionName': '否', 'Selectid': '8f1dddba-8bfc-4b06-8f9c-44a50d7c5ceb', 'OptionType': 0}, {'TitleId': '7d852786-1eca-4beb-82f2-9b52fd46ad6e', 'OptionName': '否', 'Selectid': '51fac408-9d07-4a7a-9375-b1872c4ab0bd', 'OptionType': 0}]
    data['PZData'] = PZdata
    if user.flag == 0:
        allmap = soup.find(id='allmap')
        maps = allmap.find_parent().find_all('select')
        province = maps[0].find('option', attrs={"selected": "selected"}).attrs['value']
        city = maps[1].attrs['data-defaultvalue']
        county = maps[2].attrs['data-defaultvalue']
        user.province_name = province
        user.city_name = city
        user.city_name = county
    else:
        province = user.province_name
        city = user.city_name
        county = user.county_name
    data.update({'Province': province, "City": city, "Country": county, 'FaProvince': province, "FaCity": city,
                 "FaCountry": county})
    code = parse_code_img(cookie)
    data['VCcode'] = code
    return data


def get_code_img(cookie):
    url = "http://xg.sylu.edu.cn/SPCP/Web/Report/GetLoginVCode?dt"+str(int(time.time()*1000))
    try:
        with open(temp_file_name, 'wb') as img:
            headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                                     "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
                       "Host": "xg.sylu.edu.cn",
                       "Upgrade-Insecure-Requests": "1",
                       "Cookie": cookie}
            get = requests.get(url, headers=headers)
            img.write(get.content)
    except Exception as e:
        e.with_traceback()


def parse_code_img(cookie):
    flag = True;
    while flag:
        get_code_img(cookie)
        n = ocr.ocr(temp_file_name, det=False)
        code = n[0][0].replace(' ', '')
        code = code.replace('@', 'Q')
        if len(code) == 4:
            flag = False
    return code


def tb_report(cookie, user):
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    # 又臭又长的data
    data = parser_info(cookie, user)
    url = "http://xg.sylu.edu.cn/SPCP/Web/Report/Index"
    headers.update({"Referer": "http://xg.sylu.edu.cn/SPCP/Web/Report/Index",
                    "Upgrade-Insecure-Requests": '1',
                    "Cookie": cookie})
    post = requests.post(url, headers=headers, data=parse.urlencode(data))
    if post.status_code == 200:
        if len(re.findall("提交成功", post.text)) == 0:
            tb_report(cookie, user)
        else:
            # 填报成功
            return data
    else:
        Exception("填报失败")


if __name__ == '__main__':
    tb_report(1)