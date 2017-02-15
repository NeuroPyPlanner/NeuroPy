# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 22:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('medication', '0003_auto_20170215_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='post_peak_easy_end',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medication',
            name='post_peak_easy_start',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medication',
            name='post_peak_medium_end',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medication',
            name='post_peak_medium_start',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
    ]
