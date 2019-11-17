from django.contrib import admin

from sign.models import Guest, Event


# Register your models here.

'''发布会注册'''
class EventAdmin(admin.ModelAdmin):
    # 取自model中的Event类中的变量（数组格式）
    list_display = ['id','name','status','address', 'start_time']
    #创建搜索栏，用name关键词匹配（数组格式）
    search_fields = ['name']
    #过滤器
    list_filter = ['status']

'''嘉宾注册'''
class GuestAdmin(admin.ModelAdmin):
    # 取自model中的Guest类中的变量
    list_display = ['realname', 'phone', 'email', 'sign','event']

    # 创建搜索栏，用name属性搜索
    search_fields = ['realname']
    # 过滤器
    list_filter = ['sign']

#用EventAdmin选项注册Event模块
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)

