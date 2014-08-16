# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('orders', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('accept_date', models.DateTimeField(null=True, blank=True)),
                ('reserved_until', models.DateTimeField(null=True, blank=True)),
                ('sold', models.BooleanField(default=False)),
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
