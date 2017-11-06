# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-03 18:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20171102_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Type of the work activity. Example: Concrete works, Electrical works, Finishing works..', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConstructionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Type of the construction. Example: Building, Highway etc..', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='construction_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.ConstructionType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variation',
            name='activity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Activity'),
            preserve_default=False,
        ),
    ]