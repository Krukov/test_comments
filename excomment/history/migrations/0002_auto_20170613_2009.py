# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commenthistory',
            name='when',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]