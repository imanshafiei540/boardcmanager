# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-09 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0002_auto_20181109_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_time',
            field=models.TimeField(default='00:00', null=True),
        ),
    ]
