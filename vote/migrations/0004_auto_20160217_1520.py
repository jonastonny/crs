# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-17 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20160217_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.TextField(),
        ),
    ]