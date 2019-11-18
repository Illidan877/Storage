# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-15 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict_con', '0009_auto_20191112_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='category',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='stock_sum',
            field=models.IntegerField(default=None, verbose_name='总库存'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='stocked',
            field=models.IntegerField(default=None, verbose_name='已入库库存'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='stocking',
            field=models.IntegerField(default=None, verbose_name='可容纳库存'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Provider',
        ),
    ]
