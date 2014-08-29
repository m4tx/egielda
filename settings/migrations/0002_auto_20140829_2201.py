# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='id',
        ),
        migrations.AlterField(
            model_name='setting',
            name='name',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
    ]
