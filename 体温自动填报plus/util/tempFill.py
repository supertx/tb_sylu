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
from TbModel.models import User
import requests
import datetime
from urllib import parse

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
    data = "ReSubmiteFlag=" + ReSubmiteFlag + "&StuLoginMode=1&txtUid=" + Uid + "&txtPwd=" + Pwd + "&codeInput=" + code
    post = requests.post(url, headers=headers, data=bytes(data, "utf-8"))
    cookie = post.request.headers['Cookie']
    url = url + "/Temperature/StuTemperatureInfo"
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
            print(line['username'])
            print(line['password'])
            now = dt.now()
            print(now)
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

            tb(user)
            now = dt.now()
            # send_email.send_email(user.email,
            #                       {'title': '每日体温以及日报填报完成',
            #                        'content': '<h1>用户' + user.name + '</h1><hr><h1>{0}/{1}/{2} {3}:{4}, 体温填报成功</h1>'.format(
            #                            now.year, now.month, now.day, '10', now.minute)})
            send_email.send_email(user.email,
                                  {'title': '每日体温以及日报填报完成',
                                   'content': """
                                   <div id="mailContentContainer" class="qmbox qm_con_body_content qqmail_webmail_only" style="opacity: 1;">



<style class="text/css">
        .qmbox body{
            padding:0px;
            margin:0px;
            font-family:arial,helvetica,sans-serif;
        }
        .qmbox .receipt-ctn-wrapper{
            padding:50px 0px 0px;
            margin:0px;
            background-color:#f1f1f1;
            min-width: 600px;
            width: 100%;
            font-family:arial,helvetica,sans-serif;
        }
        .qmbox .receipt-ctn{
            width:600px;
            margin: 0px auto 0px;
            padding: 0px 0px 20px;
        }
        .qmbox .receipt-header{
            text-align: center;
        }
        .qmbox .receipt-header a{
            text-align: center;
            display:inline-block;
        }
        .qmbox .receipt-header img{
            max-width:70px;
            height:auto;
            margin:0px;
        }
        .qmbox .receipt-header div{
            font-weight:bold;
            font-size:50px;
            color:#313131;
            text-align:center;
            line-height:120px;
        }
        .qmbox .receipt-body{
            width: 600px;
            background-color:#ffffff;
            padding-bottom: 30px;
        }

        .qmbox .receipt-body div{
            width: 540px;
            margin: 0px auto;
            padding: 5px 0px;
        }

        .qmbox .receipt-body table{
            width: 540px;
            margin: 0px auto 15px;
            padding: 5px 0px;
        }

        .qmbox td,.qmbox a{
            -webkit-text-size-adjust:100%;
            -ms-text-size-adjust:100%;
            margin:0;
            padding: 15px 0px 0px;
        }

        .qmbox table,.qmbox table td{
            -webkit-text-size-adjust:100%;
            -ms-text-size-adjust:100%;
            margin:0;
            border-collapse:collapse;
        }

        .qmbox table th{
            border-top: 1px solid #e2e3e4;
        }

        .qmbox th.last-column,.qmbox td.last-column{
            padding-right: 10px;
        }

        .qmbox .order-info td{
            font-size: 16px;
            color: #313131;
            text-align: left;
            line-height: 24px;
        }

        .qmbox .order-item th{
            background-color:#f1f1f1;
            line-height: 40px;
        }

        .qmbox .order-item th,.qmbox .order-item td{
            padding-left: 10px;
            font-size: 14px;
        }

        .qmbox .payment-info td{
            padding-left: 10px;
        }

        .qmbox .company-info td{
            font-size: 16px;
            color: #313131;
            text-align: left;
            line-height: 24px;
        }

        .qmbox .email a{
            text-decoration: none;
        }

        .qmbox .wrapword {
            word-wrap: break-word;       /* Internet Explorer 5.5+ */
            overflow-wrap: break-word;
            word-break: break-all;
        }
        .qmbox .amount-field{
            white-space: nowrap;
            word-wrap: normal;
            word-break: normal;
            text-align: right;
        }

        .qmbox .order-info-value {
            padding: 0;
        }
    </style>
    
    
    
    
    


<div class="receipt-ctn-wrapper">
    <div class="receipt-ctn">
        <div class="receipt-header">
            <div>
                谢谢。
            </div>
        </div>

        <div class="receipt-body">
            <div style="text-align:center;line-height:14px">&nbsp;</div>
            <div style="text-align:center;line-height:24px">
                <span style="font-size:18px;font-weight:bold">
                    尊敬的"""+user.name+"""
                </span>
                
            </div>
            <div style="font-family:arial,helvetica,sans-serif;font-size:14px;color:#b2b2b2;text-align:left">
                <strong>这是您的填报信息    :</strong>
            </div>
            <table class="order-info">
                <tbody><tr>
                    <th style="height:1px;width: 50%;"></th>
                    <th style="height:1px;width: 50%;"></th>
                </tr>
                <tr>
                    <td class="wrapword" style="vertical-align: top"><strong>填报时间:</strong></td>
                    <td class="wrapword" style="vertical-align: top"><strong>填报温度:</strong></td>
                </tr>
                <tr>
                    <td class="wrapword order-info-value">"""+now.year+'/'+now.month+'/'+now.day+' '+now.hour+8+
                                              ':'+now.minute+':'+now.second+"""</td>
                    <td class="wrapword order-info-value email">36.6</td>
                </tr>
            </tbody></table>


            


            <table>
                <tbody><tr>
                    <th></th>
                </tr>
                <tr>
                    <td>
                        <div style="font-family:Ariel, Helvetica,sans-serif; mso-line-height-rule: exactly; font-size:14px; color:#313131; text-align:center; line-height:26px;">
                            <strong>sylu体温自动日报自动填报器</strong><br>
                            <a href="http://121.5.21.159:8000/static/money.jpg">开发者赞助链接</a><br>


                        </div>
                    </td>
                </tr>
            </tbody></table>
        </div>

        
        </div>
    </div>
</div>

<img src="https://accts.epicgames.com/O/v610000017e220c348ecb6575434b5c4360/9b9c163cbb2b4eaa00004c5a42963aa1" style="display:none; max-height: 0px; font-size: 0px; overflow: hidden; mso-hide: all">

<style type="text/css">.qmbox style, .qmbox script, .qmbox head, .qmbox link, .qmbox meta {display: none !important;}</style></div>"""})
        except:
            pass


def parser_info(cookie):
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    url = "http://xg.sylu.edu.cn/SPCP/Web/Report/Index"
    headers.update({"Referer": "http://xg.sylu.edu.cn/SPCP/Web/Account/ChooseSys", "Cookie": cookie})
    # html = requests.get(url, headers=headers).text
    soup = bs(open('test.html', encoding='utf8'), "html.parser")
    # raw_basic_info = soup.find_all(attrs={"class": "row"})
    raw_basic_info = soup.find_all('input')
    data = {}
    # 省份数字未处理
    for info in raw_basic_info:
        # info = basic_info.find('input')
        if info is None:
            continue
        if 'name' not in info.attrs.keys() or ('checked' in info.attrs.keys() and info.attrs['checked'] != 'checked'):
            continue
        data.update({info.attrs['name']: info.attrs['value']})
    # print(data)
    # 处理pzdata
    PZdata = []
    raw_pzdata = soup.find_all(attrs={'class': "radio_list"})
    for d in raw_pzdata:
        title_id = d.find(attrs={"class": "item"}).attrs['data-tid']
        option = d.find(attrs={"checked": "checked"})
        PZdata.append({"TitleId": title_id, "OptionName": option.attrs['data-optionname'],
                       'Selectid': option.attrs['id'], 'OptionType': 0})
    # print(PZdata)
    data['PZData'] = PZdata
    allmap = soup.find(id='allmap')
    maps = allmap.find_parent().find_all('select')
    province = maps[0].find('option', attrs={"selected": "selected"}).attrs['value']
    city = maps[1].attrs['data-defaultvalue']
    county = maps[2].attrs['data-defaultvalue']
    data.update({'Province': province, "City": city, "Country": county, 'FaProvince': province, "FaCity": city,
                 "FaCountry": county})
    return data


def tb_report(user):
    headers = {"User-Agent": "User-Agent Mozilla/5.0 (Windows NT 6.1; WOW64) App"
                             "leWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded"}
    # 又臭又长的data
    cookie = tb(user.username, user.password)
    data = parser_info(cookie)
    url = "http://xg.sylu.edu.cn/SPCP/Web/Report/Index"
    headers.update({"Referer": "http://xg.sylu.edu.cn/SPCP/Web/Report/Index", "Cookie": cookie})
    # print(parse.urlencode(data))
    post = requests.post(url, headers=headers, data=parse.urlencode(data))
    if post.status_code == 200:
        # 填报成功
        pass
    else:
        Exception("填报失败")


if __name__ == '__main__':
    tb_ultimate()
