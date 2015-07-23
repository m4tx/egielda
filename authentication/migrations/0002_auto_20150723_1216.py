# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import authentication.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='document',
            field=models.ImageField(max_length=200, upload_to=authentication.models.new_document_filename, blank=True),
        ),
    ]
