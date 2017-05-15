# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-12 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0014_auto_20170512_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='air_humidity',
            field=models.FloatField(default=-1.0, help_text='Air humidity inside box', null=True),
        ),
        migrations.AddField(
            model_name='box',
            name='soil_humidity',
            field=models.FloatField(default=-1.0, help_text='Soil humidity inside box', null=True),
        ),
        migrations.AddField(
            model_name='box',
            name='temperature',
            field=models.FloatField(default=-1.0, help_text='Temperature inside box', null=True),
        ),
    ]
