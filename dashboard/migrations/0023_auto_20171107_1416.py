# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-07 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20171106_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimstatus',
            name='group',
            field=models.IntegerField(blank=True, help_text='To group different status with different level, give them the same group number', null=True),
        ),
        migrations.AddField(
            model_name='projectstatus',
            name='group',
            field=models.IntegerField(blank=True, help_text='To group different status with different level, give them the same group number', null=True),
        ),
        migrations.AddField(
            model_name='variationstatus',
            name='group',
            field=models.IntegerField(blank=True, help_text='To group different status with different level, give them the same group number', null=True),
        ),
    ]
