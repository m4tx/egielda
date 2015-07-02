# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('accept_date', models.DateTimeField(null=True, blank=True)),
                ('sold', models.BooleanField(default=False)),
                ('sold_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.CharField(max_length=13, blank=True)),
                ('publisher', models.CharField(max_length=150, blank=True)),
                ('title', models.CharField(max_length=250, blank=True)),
                ('publication_year', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('visible', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(to='categories.Category', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('book_type', models.ForeignKey(to='books.BookType')),
                ('order', models.ForeignKey(to='orders.Order')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.ForeignKey(to='books.BookType'),
        ),
        migrations.AddField(
            model_name='book',
            name='order',
            field=models.ForeignKey(blank=True, to='orders.Order', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(related_name='appuser_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='purchaser',
            field=models.ForeignKey(related_name='appuser_purchaser', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
