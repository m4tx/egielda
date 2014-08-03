# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_dummypermissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dummypermissions',
            options={'permissions': (('view_books_index', 'View books.index'), ('view_books_add_book', 'View books.add_book'), ('view_books_edit_book', 'View books.edit_book'), ('view_books_remove_book', 'View books.remove_book'), ('view_books_book_details', 'View books.book_details'), ('view_books_bulk_actions', 'View books.bulk_actions'), ('view_categories_index', 'View categories.index'), ('view_categories_add_category', 'View categories.add_category'), ('view_categories_edit_category', 'View categories.edit_category'), ('view_categories_remove_category', 'View categories.remove_category'), ('view_categories_list_books', 'View categories.list_books'), ('view_managemenu_index', 'View managemenu.index'), ('view_orders_order_details', 'View orders.order_details'), ('view_orders_not_executed', 'View orders.not_executed'), ('view_orders_outdated', 'View orders.outdated'), ('view_orders_executed', 'View orders.executed'), ('view_orders_execute', 'View orders.execute'), ('view_orders_execute_accept', 'View orders.execute_accept'), ('view_sellers_index', 'View sellers.index'), ('view_sellers_accept_books', 'View sellers.accept_books'), ('view_sellers_accept_edit_book', 'View sellers.accept_edit_book'), ('view_settings_index', 'View settings.index'), ('view_stats_index', 'View stats.index'), ('view_stats_books_sold', 'View stats.books_sold'), ('view_stats_users', 'View stats.users'), ('view_stats_list_books', 'View stats.list_books'), ('view_stats_books', 'View stats.books'))},
        ),
    ]