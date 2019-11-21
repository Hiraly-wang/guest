# -*- coding: utf-8 -*-
# @Time    : 2019/11/18 17:16
# @Author  : Fei.Wang
# @Email   : 415892223@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from sign import views_if

urlpatterns = {
    # sign system interface:

    # ex:/api/add_event/
    url(r'^add_event/', views_if.add_event, name='add_event'),
    url(r'^add_guest/', views_if.add_guest, name='add_guest'),
    url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
    url(r'^get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    url(r'^user_sign/', views_if.user_sign, name='user_sign'),

}
