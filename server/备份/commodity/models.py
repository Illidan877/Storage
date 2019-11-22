from django.db import models

# 商品
class Commodity(models.Model):
    commodity = models.CharField(max_length=30, verbose_name='商品名称')
    provider = models.ForeignKey(Provider, verbose_name='供应商')
    type = models.ForeignKey(Dict_con, verbose_name='商品类别')
    intro = models.CharField(max_length=50, verbose_name='商品简介')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品单价')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
    is_active = models.BooleanField(default=True)
    #     商品单位 | 吨/个/间/件/桶/包台/平方米/再议...
    weight = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='理论重量')
    x = models.IntegerField(verbose_name='x标')
    y = models.IntegerField(verbose_name='y标')
    z = models.IntegerField(verbose_name='z标')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'