# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '__first__'),
        ('common', '__first__'),
        ('orders', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField()),
                ('reserved_until', models.DateTimeField(null=True, blank=True)),
                ('sold', models.BooleanField()),
                ('sold_date', models.DateTimeField(null=True, blank=True)),
                ('order', models.ForeignKey(blank=True, to='orders.Order', null=True)),
                ('owner', models.ForeignKey(to='common.AppUser')),
                ('purchaser', models.ForeignKey(blank=True, to='common.AppUser', null=True)),
                ('reserver', models.ForeignKey(blank=True, to='common.AppUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.CharField(max_length=13, blank=True)),
                ('publisher', models.CharField(max_length=150, blank=True)),
                ('title', models.CharField(max_length=150, blank=True)),
                ('publication_year', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('visible', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(to='categories.Category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.ForeignKey(to='books.BookType'),
            preserve_default=True,
        ),
    ]
