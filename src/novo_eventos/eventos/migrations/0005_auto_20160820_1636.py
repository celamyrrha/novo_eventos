# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-20 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_auto_20160815_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Atalho'),
        ),
        migrations.AlterField(
            model_name='inscricao',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pendente'), (1, 'Aprovado'), (2, 'Conclu\xeddo')], default=0, verbose_name='Situa\xe7\xe3o'),
        ),
    ]