# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
