# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20140731_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='accept_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
