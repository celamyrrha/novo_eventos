# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-03 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0007_auto_20160902_1150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='palestra',
            options={'ordering': ['release_date'], 'verbose_name': 'Palestra', 'verbose_name_plural': 'Palestras'},
        ),
        migrations.RemoveField(
            model_name='palestra',
            name='numero',
        ),
    ]
