# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import Group, Permission


def create_groups(apps, schema_editor):
    moderator_group = Group.objects.get_or_create(name='moderator')[0]
    admin_group = Group.objects.get_or_create(name='admin')[0]
    sysadmin_group = Group.objects.get_or_create(name='sysadmin')[0]

    moderator_permissions = [
        'view_books_index',
        'view_books_add_book',
        'view_books_edit_book',
        'view_books_book_details',

        'view_categories_index',
        'view_categories_list_books',

        'view_managemenu_index',

        'view_orders_index',
        'view_orders_order_details',
        'view_orders_not_executed',
        'view_orders_outdated',
        'view_orders_executed',
        'view_orders_execute',
        'view_orders_execute_accept',

        'view_sellers_index',
        'view_sellers_accept_books',
        'view_sellers_accept_edit_book',
        'view_sellers_remove_seller',

        'view_stats_index',
    ]

    moderator_permissions_objects = Permission.objects.filter(codename__in=moderator_permissions).exclude(
        pk__in=[permission.pk for permission in moderator_group.permissions.all()])
    moderator_permissions_objects_list = [o for o in moderator_permissions_objects]

    moderator_group.permissions.add(*moderator_permissions_objects_list)

    admin_permissions = moderator_permissions + [
        'view_books_remove_book',

        'view_categories_add_category',
        'view_categories_edit_category',
        'view_categories_remove_category',

        'view_settings_index',

        'view_stats_books_sold',
        'view_stats_users',
        'view_stats_list_books',
        'view_stats_books',
    ]

    admin_permissions_objects = Permission.objects.filter(codename__in=admin_permissions).exclude(
        pk__in=[permission.pk for permission in admin_group.permissions.all()])
    admin_permissions_objects_list = [o for o in admin_permissions_objects]

    admin_group.permissions.add(*admin_permissions_objects_list)

    sysadmin_permissions = admin_permissions

    sysadmin_permissions_objects = Permission.objects.filter(codename__in=sysadmin_permissions).exclude(
        pk__in=[permission.pk for permission in sysadmin_group.permissions.all()])
    sysadmin_permissions_objects_list = [o for o in sysadmin_permissions_objects]

    sysadmin_group.permissions.add(*sysadmin_permissions_objects_list)


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20140804_1118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dummypermissions',
            options={'permissions': (('view_books_index', 'View books.index'), ('view_books_add_book', 'View books.add_book'), ('view_books_edit_book', 'View books.edit_book'), ('view_books_remove_book', 'View books.remove_book'), ('view_books_book_details', 'View books.book_details'), ('view_categories_index', 'View categories.index'), ('view_categories_add_category', 'View categories.add_category'), ('view_categories_edit_category', 'View categories.edit_category'), ('view_categories_remove_category', 'View categories.remove_category'), ('view_categories_list_books', 'View categories.list_books'), ('view_managemenu_index', 'View managemenu.index'), ('view_orders_index', 'View orders.index'), ('view_orders_order_details', 'View orders.order_details'), ('view_orders_not_executed', 'View orders.not_executed'), ('view_orders_outdated', 'View orders.outdated'), ('view_orders_executed', 'View orders.executed'), ('view_orders_execute', 'View orders.execute'), ('view_orders_execute_accept', 'View orders.execute_accept'), ('view_sellers_index', 'View sellers.index'), ('view_sellers_accept_books', 'View sellers.accept_books'), ('view_sellers_accept_edit_book', 'View sellers.accept_edit_book'), ('view_sellers_remove_seller', 'View sellers.remove_seller'), ('view_settings_index', 'View settings.index'), ('view_stats_index', 'View stats.index'), ('view_stats_books_sold', 'View stats.books_sold'), ('view_stats_users', 'View stats.users'), ('view_stats_list_books', 'View stats.list_books'), ('view_stats_books', 'View stats.books'))},
        ),
        migrations.RunPython(create_groups),
    ]
