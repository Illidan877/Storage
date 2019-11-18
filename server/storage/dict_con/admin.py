from django.contrib import admin

from dict_con.models import *


class BaseType_Manager(admin.ModelAdmin):
    list_display = ['id', 'type_name', 'order', 'parent_type', 'parent_class_type', 'is_active']
    list_filter = ['parent_type', 'parent_class_type']
    search_fields = ['type_name']


admin.site.register(BaseType, BaseType_Manager)


class BaseClass_Manager(admin.ModelAdmin):
    list_display = ['id', 'type_name', 'created_time', 'is_active']  # 展示字段


admin.site.register(BaseClass, BaseClass_Manager)


class Warehouse_Manager(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'area', 'stock_sum', 'stocked', 'stocking', 'type', 'created_time',
                    'updated_time', 'is_active']  # 展示字段
    list_filter = ['type']  # 过滤器
    search_fields = ['name', 'type_name']  # 搜索


admin.site.register(Warehouse, Warehouse_Manager)


# class Provider_Manager(admin.ModelAdmin):
#     list_display = ['id', 'provider', 'category', 'shopper', 'created_time', 'updated_time',
#                     'is_active']  # 展示字段
#     list_filter = ['category', 'shopper']  # 过滤器
#     search_fields = ['provider']  # 搜索
#
#
# admin.site.register(Provider, Provider_Manager)
