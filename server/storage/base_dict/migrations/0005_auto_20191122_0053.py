# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-22 00:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_dict', '0004_roles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roles',
            old_name='role',
            new_name='roleof',
        ),
    ]