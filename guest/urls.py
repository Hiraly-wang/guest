"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

# 导入sign应用的views文件
from sign import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    # 添加index/路径配置
    url(r'^index/$', views.index),
    url(r'^login_action/$', views.login_action),
    url(r'^event_manage/$', views.event_manage),
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^accounts/login/$', views.index),
    url(r'^search_name/$', views.search_name),
    url(r'^search_phone/$', views.search_phone),
    # 匹配发布会id，匹配的数字eid将会作为sign_index（）视图函数的参数
    url(r'^sign_index/(?P<eid>\d+)/$', views.sign_index),
    url(r'^sign_index_action/(?P<eid>\d+)/$', views.sign_index_action),
    url(r'^logout/$', views.logout),
    # 配置接口路径
    url(r'^api/',include('sign.urls',namespace='sign'))
]
