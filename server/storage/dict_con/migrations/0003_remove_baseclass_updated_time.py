# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-08 19:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dict_con', '0002_auto_20191108_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseclass',
            name='updated_time',
        ),
    ]
