from django.db import models


# 字典类型表
class BaseClass(models.Model):
    type_name = models.CharField(max_length=30, verbose_name='类型名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '字典类型表'
        verbose_name_plural = verbose_name


# 类型配置表
class BaseType(models.Model):
    type_name = models.CharField(max_length=30, verbose_name='类型名称')
    parent_type = models.IntegerField(default=0, verbose_name='父级类型')
    parent_class_type = models.ForeignKey(BaseClass, verbose_name='从属')


    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '类型配置表'
        verbose_name_plural = verbose_name


# 仓库表
class Warehouse(models.Model):
    name = models.CharField(max_length=20, verbose_name='仓库名称')
    nickname = models.CharField(max_length=20, verbose_name='仓库别名')
    type = models.ForeignKey(BaseType, null=True, verbose_name='仓库类型')
    area = models.IntegerField(verbose_name='面积')
    type = models.ForeignKey(BaseType, verbose_name='仓库类型')
    stock_sum = models.IntegerField(verbose_name='总库存')
    stocked = models.IntegerField(verbose_name='已入库库存')
    stocking = models.IntegerField(verbose_name='可容纳库存')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = verbose_name


# class TUser(models.Model):

#
# # 供应商
# class Suppliers(models.Model):
#     name = models.CharField(max_length=11, verbose_name='供应商名称')
#     category = models.ForeignKey(BaseType, verbose_name='供应商类别')
#     shopper = models.CharField(max_length=10, null=True, verbose_name='采购专员')
#     business_part = models.CharField(max_length=10, null=True, verbose_name='商务专员')
#     created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     updated_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = '供应商'
#         verbose_name_plural = verbose_name
