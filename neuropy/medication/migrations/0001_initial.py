# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='CONCERTA', max_length=20)),
                ('med_type', models.CharField(default='stimulant', max_length=20)),
                ('treating_dis', models.CharField(default='ADD/ADHD', max_length=25)),
                ('half_life', models.TimeField()),
                ('ramp_up', models.DurationField()),
                ('peak_period', models.DurationField()),
            ],
        ),
    ]
