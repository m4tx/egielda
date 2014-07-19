# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('valid_until', models.DateTimeField()),
                ('books', models.ManyToManyField(to='common.Book')),
                ('user', models.ForeignKey(to='common.AppUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
