# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-11 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0008_auto_20170511_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illumination',
            name='illumination_frequency',
            field=models.CharField(help_text='Care frequency', max_length=11),
        ),
        migrations.AlterField(
            model_name='watering',
            name='watering_frequency',
            field=models.CharField(help_text='Care frequency', max_length=11),
        ),
    ]
