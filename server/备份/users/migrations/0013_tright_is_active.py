# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-19 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_tright_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='tright',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
    ]
