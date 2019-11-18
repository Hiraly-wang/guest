from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from sign.models import Event, Guest

# Create your views here.
'''登录页面index'''


def index(request):
    # 以字符串的形式传递给客户端（浏览器）
    # return HttpResponse("Hello Django")
    return render(request, 'index.html')


'''执行登录过程'''


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 使用authenticate()函数认证给出的用户名和密码，在username和password正确的情况下返回user对象
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            # if username == 'admin' and password == 'admin123':
            # return HttpResponse('login success!')
            # 重定向到http://127.0.0.1:8000/event_manage/
            request.session['user'] = username  # 将session信息记录在浏览器中
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)  # 添加浏览器cookie
            return response

        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


'''登录成功后的页面，发布会管理'''


@login_required()
def event_manage(request):
    # 查询发布会所有的对象event
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '')  # 读取浏览器session
    # 将查询到的数据，返回到event_manage.html中
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


'''发布会名字搜索'''


@login_required()
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.POST.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


'''发布会管理'''


@login_required()
def guest_manage(request):
    # 查询嘉宾所有的对象（数据）guest
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')
    # 把查询出来的嘉宾列表放在分页Paginator类中，每页显示2个
    paginator = Paginator(guest_list, 2)
    # 通过Get请求得到当前要显示的第几页的数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    # 如果没有page页，抛出PageNotAnInteger异常，返回第一页的数据
    except PageNotAnInteger:
        contacts = paginator.page(1)
    # 如果page不在范围中（超出范围），取最后一页数据
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


'''通过手机号搜索嘉宾'''


@login_required()
def search_phone(request):
    phoneNumber = request.session.get('phone', '')
    search_phone = request.GET.get('phone', '')
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    return render(request, 'guest_manage.html', {'phone': phoneNumber,
                                                 'guests': guest_list})


'''发布会签到页面'''


@login_required()
def sign_index(request, eid):
    # get_object_or_404，默认调用diango的tabel.objects.get()方法，如果查询对象不存在，抛出Http404异常
    # 这样省去了对tabel.objects.get()
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


'''发布会签到动作'''


@login_required()
# 屏蔽CSRF
# @csrf_exempt
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    # 通过post请求获取phone
    phone = request.POST.get('phone', '')
    print(phone)
    # 获取所有的嘉宾
    # guest_list = Guest.objects.all()
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event_id or phone error'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    # sign 状态为true，已经签到
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'user has sign in'})
    else:
        # 修改sign状态为1，并提示签到成功
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success',
                                                   'guest': result})


'''退出登录'''


@login_required()
def logout(request):
    auth.logout(request)
    # 重定向到登录界面
    response = HttpResponseRedirect('/index/')
    return response
