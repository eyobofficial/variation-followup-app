# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-28 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20171028_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='approved_date',
            field=models.DateField(blank=True, help_text='Approved date of the variation. (Use yyyy-mm-dd format)', null=True, verbose_name='Approved/Rejected Date'),
        ),
    ]
