# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 14:50
from __future__ import unicode_literals

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0006_auto_20160826_2026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aviso',
            old_name='conteuto',
            new_name='conteudo',
        ),
        migrations.AlterField(
            model_name='evento',
            name='imagem_evento',
            field=stdimage.models.StdImageField(default=1, upload_to='eventos/images', verbose_name='Imagem'),
            preserve_default=False,
        ),
    ]
