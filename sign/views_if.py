# -*- coding: utf-8 -*-
# @Time    : 2019/11/18 17:19
# @Author  : Fei.Wang
# @Email   : 415892223@qq.com
# @File    : views_if.py
# @Software: PyCharm

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse

from sign.models import Event

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

    if name!='':
        datas=[]
        results=Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event={}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['limit'] = r.limit
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': '200', 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status':'10022','message': 'query result is empty'})
