# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-06 09:24
from __future__ import unicode_literals

import blogapp.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20160806_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourite',
            name='members',
            field=models.ManyToManyField(through='blogapp.Membership', to='blogapp.Profile'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='blog',
            field=models.ForeignKey(default=blogapp.models.Profile, on_delete=django.db.models.deletion.CASCADE, to='blogapp.Profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 6, 11, 24, 56, 393623)),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 6, 11, 24, 56, 393597)),
        ),
    ]
