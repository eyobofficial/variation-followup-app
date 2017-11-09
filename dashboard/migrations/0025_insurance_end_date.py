# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-08 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_auto_20171108_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='end_date',
            field=models.DateField(blank=True, help_text='Expiration date of this insurance. (Use yyyy-mm-dd format)', null=True, verbose_name='Expiration date'),
        ),
    ]