# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20160204_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
    ]
