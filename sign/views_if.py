# -*- coding: utf-8 -*-
# @Time    : 2019/11/18 17:19
# @Author  : Fei.Wang
# @Email   : 415892223@qq.com
# @File    : views_if.py
# @Software: PyCharm

import time

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import JsonResponse

from sign.models import Event, Guest

'''添加发布会接口'''


def add_event(request):
    eid = request.POST.get('eid', '')
    limit = request.POST.get('limit', '')
    name = request.POST.get('name', '')
    start_time = request.POST.get('start_time', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')

    if eid == '' or name == '' or limit == '' or start_time == '' or address == '':
        return JsonResponse({'status': '10021', 'message': 'Parameter error'})
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': '10022', 'message': 'event id already exits'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': '10023', 'message': 'event name already exits'})
    if status == '':
        status = 1
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    # 日期格式错误
    except ValidationError:
        error = 'start_time format error. It Must be in YYYY-MM-DD HH:MM:SS format .'
        return JsonResponse({'status': '10023', 'message': error})
    return JsonResponse({'status': '200', 'message': 'add event success'})


'''查询发布会接口'''


def get_event_list(request):
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')
    if eid == '' or name == '':
        return JsonResponse({'status': '10021', 'message': 'Parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': '10022', 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['limit'] = result.limit
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': '200', 'message': 'success', 'data': 'event'})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['limit'] = r.limit
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': '200', 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': '10022', 'message': 'query result is empty'})


'''添加嘉宾接口'''


def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')

    if eid == '' or realname == '' or phone == '' or email == '':
        return JsonResponse({'status': '10021', 'message': 'Parameter error'})
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': '10022', 'message': 'event id null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': '10023', 'message': 'event id is not availbale'})
    # 发布会人数限制
    event_limit = Event.objects.get(id=eid).limit
    # 发布会已经添加的嘉宾数
    guest_limit = Guest.objects.filter(event_id=eid)

    if len(guest_limit) >= event_limit:
        return JsonResponse({'status': '10024', 'message': 'event number is full'})

    # 发布会时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split('.')[0]
    timeArray = time.strptime(etime, '%Y-%M-%D %H:%M:%S')
    e_time = int(time.mktime(timeArray))

    # 当前时间
    now_time = str(time.time())
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': '10025', 'message': 'event has started'})
    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status': '10026', 'message': 'the event guest phone is repeat'})
    return JsonResponse({'status': '200', 'message': 'add guset success'})


'''查询嘉宾接口'''


def get_guest_list(request):
    eid = request.POST.get('eid', '')
    phone = request.POST.get('phone', '')

    if eid == '':
        return JsonResponse({'status': '10021', 'message': 'eid is empty'})
    if eid != '' and phone == '':
        datas = []
        result = Guest.objects.filter(event_id=eid)
        if result:
            for r in result:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['sign'] = r.sign
                guest['email'] = r.email
                datas.append(guest)
                return JsonResponse({'status': '200', 'message': 'success'})
        else:
            return JsonResponse({'status': '10022', 'message': 'query result is empty'})
    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(event_id=eid, phone=phone)
        except ObjectDoesNotExist:
            return JsonResponse({'status': '10022', 'message': 'query result is empty'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['sign'] = result.sign
            guest['email'] = result.email
            return JsonResponse({'status': '200', 'message': 'success', 'data': guest})


'''发布会签到接口'''


def user_sign(request):
    eid = request.POST.get('eid', '')
    phone = request.POST.get('phone', '')

    if eid == '' or phone == '':
        return JsonResponse({'status': '10021', 'message': 'Parameter error'})
    result = Event.objects.get(id=eid)
    if not result:
        return JsonResponse({'status': '10022', 'message': 'event id is null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': '10023', 'message': 'event id is not availbale'})
    # 发布会时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split('.')[0]
    timeArray = time.strptime(etime, '%Y-%M-%D %H:%M:%S')
    e_time = int(time.mktime(timeArray))

    # 当前时间
    now_time = str(time.time())
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': '10024', 'message': 'event has started'})
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': '10025', 'message': 'user phone is null'})

    result = Guest.objects.filter(even_id=eid, phone=phone)
    if not result:
        return JsonResponse({'status': '10026', 'message': 'user did not participate in the conference'})
    result = Guest.objects.get(even_id=eid, phone=phone).sign
    if not result:
        return JsonResponse({'status': '10027', 'message': 'user has signed'})
    else:
        Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
        return JsonResponse({'status': '200', 'message': 'sign success'})
