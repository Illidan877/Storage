from django.contrib import admin

from base_dict.models import BaseType, Jurisdiction, Roles, Users


class BaseType_Manager(admin.ModelAdmin):
    list_display = ['id', 'name', 'pid', 'is_active', ]


admin.site.register(BaseType, BaseType_Manager)


class Jurisdiction_Manager(admin.ModelAdmin):
    list_display = ['id', 'pid', 'name', 'type', 'order', 'link', 'params', 'sign', 'is_active', ]
    list_filter = ['pid']  # 过滤器


admin.site.register(Jurisdiction, Jurisdiction_Manager)


class Roles_Manager(admin.ModelAdmin):
    list_display = ['id', 'name', 'roleof', 'is_active']


admin.site.register(Roles, Roles_Manager)


class Users_Manager(admin.ModelAdmin):
    list_display = ['id', 'name', 'password', 'vname', 'rolesto', 'is_active']


admin.site.register(Users, Users_Manager)
