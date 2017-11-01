# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-31 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_variation_recieved_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='approved_letter',
            field=models.CharField(blank=True, help_text='Ref. No. for the approval letter. (Optional)', max_length=100, null=True, verbose_name='Ref. No. for Approval letter (Optional)'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='recieved_letter',
            field=models.CharField(blank=True, help_text='Ref. No. for the recieved letter. (Optional)', max_length=100, null=True, verbose_name='Ref. No. for Recieved Order (Optional)'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='submitted_letter',
            field=models.CharField(blank=True, help_text='Ref. No. for the submission letter. (Optional)', max_length=100, null=True, verbose_name='Ref. No. for Submission letter (Optional)'),
        ),
    ]