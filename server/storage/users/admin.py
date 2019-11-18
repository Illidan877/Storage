from django.contrib import admin

from users.models import *


class TUser_Manager(admin.ModelAdmin):
    list_display = [
        'login_phone',
        'password',
        'vername',
        'created_time',
    ]


admin.site.register(TUser, TUser_Manager)


class TRole_Manager(admin.ModelAdmin):
    list_display = [
        'id',
        'login_name',
        'parent_role',
        'created_time',
        'description',
        'right',
    ]


admin.site.register(TRole, TRole_Manager)


class TRight_Manager(admin.ModelAdmin):
    list_display = [
        'id',
        'right_name',
        'parent',
    ]


admin.site.register(TRight, TRight_Manager)
