# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getrecipe', '0002_priprava_kolicina'),
    ]

    operations = [
        migrations.AddField(
            model_name='recept',
            name='povezava_do_slike_jedi',
            field=models.URLField(null=True),
        ),
    ]
