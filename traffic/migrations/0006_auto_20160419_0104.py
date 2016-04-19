# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 01:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0005_auto_20160419_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='moving',
            name='agency',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='traffic.Agency'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moving',
            name='violation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='traffic.Violation'),
            preserve_default=False,
        ),
    ]
