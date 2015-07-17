# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUserHasCorrectData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('incorrect_fields', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(unique=True, max_length=100, error_messages={'unique': 'Ta nazwa użytkownika już istnieje w bazie danych.'}),
        ),
        migrations.AddField(
            model_name='appuserhascorrectdata',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
