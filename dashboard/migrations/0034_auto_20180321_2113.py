# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-21 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_insurancetype_short_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='thumbanil',
            field=models.ImageField(blank=True, null=True, upload_to='user/thumbanils/'),
        ),
        migrations.AlterField(
            model_name='package',
            name='max_projects',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Max number of projects allowed'),
        ),
        migrations.AlterField(
            model_name='package',
            name='max_users',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Max number of users allowed'),
        ),
    ]
