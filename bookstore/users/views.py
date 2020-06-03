from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from .models import Passport
import re


# Create your views here.
def register(request):
    return render(request, 'users/register.html')


def register_handler(request):
    '''进行用户注册处理'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    # 进行数据校验
    if not all([username, password, email]):
        return render(request, 'users/register.html', {'errmsg': '参数不能为空!'})

    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg': '邮箱不合法!'})

    # 进行业务处理:注册，向账户系统中添加账户
    # Passport.objects.create(username=username, password=password, email=email)
    try:
        Passport.objects.add_one_passport(username=username, password=password, email=email)
    except Exception as e:
        print("e: ", e)  # 把异常打印出来
        return render(request, 'users/register.html', {'errmsg': '用户名已存在！'})

    # 注册完，还是返回注册页。
    return redirect(reverse('books:index'))


def login(request):
    '''显示登录页面'''
    if request.COOKIES.get('username'):
        username = request.COOKIES.get("username")
        checked = 'checked'

    else:
        username = ''
        checked = ''

    context = {
        'username': username,
        'checked': checked,
    }

    return render(request, 'users/login.html', context=context)


def login_check(request):
    # 获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    # 数据校验
    if not all([username, password, remember]):
        return JsonResponse({'res': 2})

    # 进行处理：根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username, password)

    if password:
        next_url = reverse('books:index')
        jres = JsonResponse({
            'res': 1,
            'next_url': next_url
        })
        # 判断是否需要记住用户名

        if remember == 'true':
            # 记住用户名
            jres.set_cookie('username', username, max_age=7*24*3600)
        else:
            jres.delete_cookie('username')

        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id

        return jres

    else:
        return JsonResponse({
            'res':0 # 用户名或密码错误
        })


def logout(request):
    request.session.flush()
    return redirect(reverse('books:index'))