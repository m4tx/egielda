# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models


class DummyPermissions(models.Model):
    class Meta:
        permissions = (
            ('view_books_index', "View books.index"),
            ('view_books_add_book', "View books.add_book"),
            ('view_books_edit_book', "View books.edit_book"),
            ('view_books_remove_book', "View books.remove_book"),
            ('view_books_book_details', "View books.book_details"),
            ('view_books_duplicated', "View books.duplicated"),

            ('view_categories_index', "View categories.index"),
            ('view_categories_add_category', "View categories.add_category"),
            ('view_categories_edit_category', "View categories.edit_category"),
            ('view_categories_remove_category', "View categories.remove_category"),
            ('view_categories_list_books', "View categories.list_books"),

            ('view_managemenu_index', "View managemenu.index"),

            ('view_orders_index', "View orders.index"),
            ('view_orders_order_details', "View orders.order_details"),
            ('view_orders_not_fulfilled', "View orders.not_fulfilled"),
            ('view_orders_fulfilled', "View orders.fulfilled"),
            ('view_orders_fulfill', "View orders.fulfill"),
            ('view_orders_fulfill_accept', "View orders.fulfill_accept"),
            ('view_orders_remove_order', "View orders.remove_order"),

            ('view_sellers_index', "View sellers.index"),
            ('view_sellers_accept_books', "View sellers.accept_books"),
            ('view_sellers_accept_edit_book', "View sellers.accept_edit_book"),
            ('view_sellers_remove_seller', "View sellers.remove_seller"),

            ('view_settings_index', "View settings.index"),

            ('view_stats_index', "View stats.index"),
            ('view_stats_books_sold', "View stats.books_sold"),
            ('view_stats_books', "View stats.books"),

            ('view_users_index', "View users.index"),
            ('view_users_verified', "View users.verified"),
            ('view_users_unverified', "View users.unverified"),
            ('view_users_needing_data_correction', "View users.needing_data_correction"),
            ('view_users_verify', "View users.verify"),
            ('view_users_profile', "View users.profile"),
            ('view_users_profile_purchased', "View users.profile_purchased"),
            ('view_users_profile_sold', "View users.profile_sold"),

            ('view_authentication_profile', "View authentication.profile"),
            ('view_authentication_profile_purchased', "View authentication.purchased"),
            ('view_authentication_profile_sold', "View authentication.sold"),

            ('purchase_sell_books', "Purchase and sell books")
        )
