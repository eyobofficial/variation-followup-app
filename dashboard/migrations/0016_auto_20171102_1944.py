# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-02 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20171102_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, help_text='Short description of the construction project. (Optional)', null=True, verbose_name='Short Project Description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='full_name',
            field=models.CharField(help_text='Official full name of the construction project', max_length=100, verbose_name='Official Prject Title'),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_name',
            field=models.CharField(help_text='Short common name of the construction project', max_length=100, verbose_name='Short Unofficial Project Title'),
        ),
    ]
