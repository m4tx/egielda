# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20140828_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(related_name='appuser_owner', to='common.AppUser'),
        ),
        migrations.AlterField(
            model_name='book',
            name='purchaser',
            field=models.ForeignKey(related_name='appuser_purchaser', null=True, to='common.AppUser', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='reserver',
            field=models.ForeignKey(related_name='appuser_reserver', null=True, to='common.AppUser', blank=True),
        ),
    ]
