from django.db import models


class TUser(models.Model):
    login_phone = models.CharField(max_length=20, verbose_name='手机号')
    password = models.CharField(max_length=64, verbose_name='登录密码')
    vername = models.CharField(max_length=64, verbose_name='用户姓名')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class TRight(models.Model):
    parent = models.IntegerField(default=0, verbose_name='父级权限')
    right_name = models.CharField(max_length=20, default="", verbose_name='权限名称')

    class Meta:
        def __str__(self):
            return self.right_name

        verbose_name = '权限表'
        verbose_name_plural = verbose_name


class TRole(models.Model):
    login_name = models.CharField(max_length=20, verbose_name='角色名称')
    parent_role = models.IntegerField(default=0, verbose_name='父级角色')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.CharField(max_length=200, default="", verbose_name='角色描述')
    right = models.ForeignKey(TRight, verbose_name="权限")

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
