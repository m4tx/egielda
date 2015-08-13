# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20150723_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='student_class',
        ),
        migrations.AddField(
            model_name='appuser',
            name='class_letter',
            field=models.CharField(default='A', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appuser',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2000)], default=2013),
            preserve_default=False,
        ),
    ]
