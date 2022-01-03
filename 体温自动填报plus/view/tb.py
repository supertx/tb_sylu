"""
@author: supermantx
@time: 2021/11/12 16:46
体温填报逻辑填报的视图层
1. 首先注册, 填写登陆体温填报系统账号和密码, 并效验整正确性(加密)
2. 邮箱提醒用户, 服务注册成功
3. 每天中午12点运行脚本执行体温填报, 并且邮箱提醒
"""

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from 体温自动填报plus.util import send_email
from 体温自动填报plus.util import tempFill
from TbModel.models import User

def tb(request):
    data = request.POST
    email = data.get('userEmail')
    username = data.get('username')
    password = data.get('password')
    with open("/root/py/体温自动填报plus/resource/stuInfo.txt", 'r') as info:
        lines = info.readlines()
        print(lines)
        for line in lines:
            for line in lines:
                if line[-1] == '\n':
                    line = dict(eval(line[:-1]))
                else:
                    line = dict(eval(line))
            if line['username'] == username:
                return HttpResponse("<h1>已完成注册请勿重复注册</h1>")
    try:
        send_email.re_email(email, username, password)
        # 将文件信息保存至txt文件中
        with open('/root/py/体温自动填报plus/resource/stuInfo.txt', 'a') as stuInfo:
            stuInfo.write(dict.__str__({"email": email, 'username': username, 'password': password}) + "\n")
            stuInfo.flush()
    except Exception as e:
        return HttpResponse("<h1>注册失败"+"</h1>")
    return HttpResponse("<h1>注册成功,每日10点自动填报</h1>")


def tianbao(request):
    tempFill.tb_ultimate()
    return JsonResponse({'message': '体温填报成功', 'code': 200})


def index(request):
    return render(request, 'index.html')


def hello(request):
    return JsonResponse({"message": "hello"})
