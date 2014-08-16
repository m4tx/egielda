# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import Group, Permission, ContentType
from django.db.models.signals import post_migrate


def create_groups(sender, **kwargs):
    if ContentType.objects.filter(name='dummy permissions').count() > 0:

        moderator_group = Group.objects.get_or_create(name='moderator')[0]
        admin_group = Group.objects.get_or_create(name='admin')[0]
        sysadmin_group = Group.objects.get_or_create(name='sysadmin')[0]

        if moderator_group.permissions.count() > 0 and admin_group.permissions.count() > 0 and \
                sysadmin_group.permissions.count() > 0:
            return

        if kwargs['verbosity'] != 0:
            print("Creating groups...")

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

        moderator_group.permissions.clear()
        moderator_permissions_objects = Permission.objects.filter(codename__in=moderator_permissions)
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

        admin_group.permissions.clear()
        admin_permissions_objects = Permission.objects.filter(codename__in=admin_permissions)
        admin_permissions_objects_list = [o for o in admin_permissions_objects]

        admin_group.permissions.add(*admin_permissions_objects_list)

        sysadmin_permissions = admin_permissions

        sysadmin_group.permissions.clear()
        sysadmin_permissions_objects = Permission.objects.filter(codename__in=sysadmin_permissions)
        sysadmin_permissions_objects_list = [o for o in sysadmin_permissions_objects]

        sysadmin_group.permissions.add(*sysadmin_permissions_objects_list)


post_migrate.connect(create_groups)