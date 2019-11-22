from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')


class BaseType(BaseModel):
    name = models.CharField(max_length=30, verbose_name='类型名称')
    pid = models.IntegerField(verbose_name='父级类型')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '字典类型表'
        verbose_name_plural = verbose_name


class Jurisdiction(BaseModel):
    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    pid = models.IntegerField(default=0, verbose_name='父级权限')
    name = models.CharField(max_length=20, default="", verbose_name='权限名称')
    type = models.ForeignKey(BaseType, null=True, verbose_name='类型')
    order = models.IntegerField(default=0, verbose_name='排序号')
    link = models.CharField(default="", max_length=150, verbose_name='链接')
    params = models.CharField(default="", max_length=200, verbose_name='参数')
    sign = models.CharField(default="", max_length=200, verbose_name='签名')

    def __str__(self):
        return self.name


class Roles(BaseModel):
    name = models.CharField(max_length=30, verbose_name='角色名称')
    roleof = models.CharField(max_length=200, default="", verbose_name='拥有权限')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name


class Users(BaseModel):
    name = models.CharField(max_length=30, verbose_name='登录名')
    password = models.CharField(max_length=128, verbose_name='密码')
    vname = models.CharField(max_length=30, verbose_name='用户名')
    rolesto = models.ForeignKey(Roles, verbose_name='角色')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
