# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-30 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_time',
            field=models.BooleanField(default=False),
        ),
    ]
