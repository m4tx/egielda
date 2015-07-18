# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20150717_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUserIncorrectFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('incorrect_fields', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='appuserhascorrectdata',
            name='user',
        ),
        migrations.DeleteModel(
            name='AppUserHasCorrectData',
        ),
    ]
