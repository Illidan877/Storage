# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-16 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuser',
            name='count',
        ),
        migrations.RemoveField(
            model_name='tuser',
            name='updated_time',
        ),
    ]