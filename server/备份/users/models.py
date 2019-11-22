from django.db import models

from dict_con.models import BaseType


class Base_Model(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')


class TRight(Base_Model):
    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    parent = models.IntegerField(default=0, verbose_name='父级权限')
    right_name = models.CharField(max_length=20, default="", verbose_name='权限名称')
    type = models.ForeignKey(BaseType, null=True, verbose_name='类型')
    order = models.IntegerField(default=0, verbose_name='排序号')
    link = models.CharField(default="", max_length=150, verbose_name='链接')
    params = models.CharField(default="", max_length=200, verbose_name='参数')
    sign = models.CharField(default="", max_length=200, verbose_name='签名')

    def __str__(self):
        return self.right_name


class TRole(Base_Model):
    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=20, verbose_name='角色名称')
    parent_role = models.IntegerField(default=0, verbose_name='父级角色')
    description = models.CharField(max_length=200, default="", verbose_name='角色描述')
    right = models.ForeignKey(TRight, verbose_name="权限")

    def __str__(self):
        return self.name


class TUser(Base_Model):
    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    login_phone = models.CharField(max_length=20, verbose_name='手机号')
    password = models.CharField(max_length=64, verbose_name='登录密码')
    vername = models.CharField(max_length=64, verbose_name='用户姓名')
    count = models.IntegerField(default=0, verbose_name='登录次数')
    tRole = models.ForeignKey(TRole, verbose_name='角色')

    def __str__(self):
        return self.name
