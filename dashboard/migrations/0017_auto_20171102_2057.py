# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-02 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20171102_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='commencement_date',
            field=models.DateTimeField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Commenecment Date'),
        ),
        migrations.AddField(
            model_name='project',
            name='completion_date',
            field=models.DateTimeField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Intended Completion Date'),
        ),
        migrations.AddField(
            model_name='project',
            name='mobilzation_period',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='project_code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Project Code (Optional)'),
        ),
        migrations.AddField(
            model_name='project',
            name='signing_date',
            field=models.DateTimeField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Agreement Signing Date'),
        ),
        migrations.AddField(
            model_name='project',
            name='site_handover',
            field=models.DateTimeField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Site Handover Date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='full_name',
            field=models.CharField(help_text='Official full name of the construction project', max_length=100, verbose_name='Official Project Title'),
        ),
    ]
