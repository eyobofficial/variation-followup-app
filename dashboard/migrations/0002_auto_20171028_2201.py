# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-28 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, help_text='Short description of the status meaning. (Optional)', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title for the variation works', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Short description about the variation works and/or work order. (Optional)', null=True)),
                ('work_order', models.CharField(blank=True, help_text='Work order no. of the variation works. (Optional)', max_length=10, null=True)),
                ('recieved_date', models.DateField(help_text='Recieved date of the variation or work order. (Use yyyy-mm-dd format)')),
                ('submitted_date', models.DateField(blank=True, help_text='Submitted date of the variation. (Use yyyy-mm-dd format)', null=True)),
                ('submitted_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Submitted amount in ETB', max_digits=14, null=True)),
                ('approved_date', models.DateField(blank=True, help_text='Approved date of the variation. (Use yyyy-mm-dd format)', null=True)),
                ('approved_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Approved amount in ETB', max_digits=14, null=True)),
                ('remark', models.TextField(blank=True, help_text='Short helpfull remark or not regarding the current status. (Optional)', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='consultant',
            name='description',
            field=models.TextField(blank=True, help_text='Short description of the Consultant firm. (Optional)', null=True),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='description',
            field=models.TextField(blank=True, help_text='Short description of the Contractor firm. (Optional)', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, help_text='Short description of the construction project. (Optional)', null=True),
        ),
        migrations.AddField(
            model_name='variation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Project'),
        ),
        migrations.AddField(
            model_name='variation',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Status'),
        ),
    ]