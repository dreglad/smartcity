# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 01:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('condominios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nivel',
            name='desarrollo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveles', to='condominios.Desarrollo'),
        ),
    ]
