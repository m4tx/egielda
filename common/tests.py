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

from django.contrib.auth.models import Permission
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse

from django.test import TestCase, Client

from authentication.models import AppUser
from utils.test_utils import (
    create_test_book_type, create_test_category, create_test_app_user, create_test_book,
    create_test_order, set_sell_purchase_timespan
)


# Utility regex to create tests out of permission definitions from models.py:
# Search: \('(.+)', "View (.+)\.(.+)"\),
# Replace: def test_$1(self):\n\t\t\tself.check_permission('$1', reverse('$2.views.$3'))


class ManagePermissionsTest(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(username="test", email="test@localhost",
                                                password="test", first_name="Test",
                                                last_name="Test", student_class="1A",
                                                phone_number="111222333")
        self.user.groups.clear()  # Default 'user' group already has some permissions
        self.client = Client()
        self.client.login(username="test", password="test")

    def test_view_books_index(self):
        self.check_permission('view_books_index', reverse('books.views.index'))

    def test_view_books_add_book(self):
        self.check_permission('view_books_add_book', reverse('books.views.add_book'))

    def test_view_books_edit_book(self):
        self.check_permission('view_books_edit_book',
                              reverse('books.views.edit_book', args=(create_test_book_type().pk,)))

    def test_view_books_remove_book(self):
        self.check_permission('view_books_remove_book',
                              reverse('books.views.remove_book',
                                      args=(create_test_book_type().pk,)))

    def test_view_books_book_details(self):
        self.check_permission('view_books_book_details',
                              reverse('books.views.book_details',
                                      args=(create_test_book_type().pk,)))

    def test_view_books_duplicated(self):
        self.check_permission('view_books_duplicated', reverse('books.views.duplicated'))

    def test_view_categories_index(self):
        self.check_permission('view_categories_index', reverse('categories.views.index'))

    def test_view_categories_add_category(self):
        self.check_permission('view_categories_add_category',
                              reverse('categories.views.add_category'))

    def test_view_categories_edit_category(self):
        self.check_permission('view_categories_edit_category',
                              reverse('categories.views.edit_category',
                                      args=(create_test_category().pk,)))

    def test_view_categories_remove_category(self):
        self.check_permission('view_categories_remove_category',
                              reverse('categories.views.remove_category',
                                      args=(create_test_category().pk,)))

    def test_view_categories_list_books(self):
        category = create_test_category()
        book_type = create_test_book_type()
        book_type.categories.add(category)
        self.check_permission('view_categories_list_books',
                              reverse('categories.views.list_books', args=(category.pk,)))

    def test_view_managemenu_index(self):
        self.check_permission('view_managemenu_index', reverse('managemenu.views.index'))

    def test_view_orders_orders_index(self):
        self.check_permission('view_orders_index', reverse('orders.views.index'))

    def test_view_orders_order_details(self):
        order = self.create_test_order_with_book()
        order.fulfilled = True
        order.save()
        self.check_permission('view_orders_order_details',
                              reverse('orders.views.order_details', args=(order.pk,)))

    def test_view_orders_not_fulfilled(self):
        self.check_permission('view_orders_not_fulfilled', reverse('orders.views.not_fulfilled'))

    def test_view_orders_fulfilled(self):
        self.check_permission('view_orders_fulfilled', reverse('orders.views.fulfilled'))

    def test_view_orders_fulfill(self):
        self.check_permission('view_orders_fulfill',
                              reverse('orders.views.fulfill',
                                      args=(self.create_test_order_with_book().pk,)))

    def test_view_orders_fulfill_accept(self):
        sessions = Session.objects.all()
        for session in sessions:
            if session.get_decoded():
                user_session = SessionStore(session_key=session.session_key)
                break
        else:
            raise Exception('User session was not found')

        order = self.create_test_order_with_book()
        user_session['books_to_purchase'] = {str(order.pk): '1337'}
        user_session['owners_by_book'] = {str(order.pk): '1337'}
        user_session.save()
        self.check_permission('view_orders_fulfill_accept',
                              reverse('orders.views.fulfill_accept', args=(order.pk,)))

    def test_view_sellers_index(self):
        self.check_permission('view_sellers_index', reverse('sellers.views.index'))

    def test_view_sellers_accept_books(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        create_test_book(book_type, app_user, False)
        self.check_permission('view_sellers_accept_books',
                              reverse('sellers.views.accept_books', args=(app_user.pk,)))

    def test_view_sellers_accept_edit_book(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        create_test_book(book_type, app_user, False)
        self.check_permission('view_sellers_accept_edit_book',
                              reverse('sellers.views.accept_edit_book',
                                      args=(app_user.pk, book_type.pk)))

    def test_view_books_remove_seller(self):
        self.check_permission('view_sellers_remove_seller',
                              reverse('sellers.views.remove_seller',
                                      args=(create_test_app_user().pk,)))

    def test_view_settings_index(self):
        self.check_permission('view_settings_index', reverse('settings.views.index'))

    def test_view_stats_index(self):
        self.check_permission('view_stats_index', reverse('stats.views.index'))

    def test_view_stats_books_sold(self):
        self.check_permission('view_stats_books_sold', reverse('stats.views.books_sold'))

    def test_view_stats_books(self):
        self.check_permission('view_stats_books', reverse('stats.views.books'))

    def test_view_users_index(self):
        self.check_permission('view_users_index', reverse('users.views.index'))

    def test_view_users_verified(self):
        self.check_permission('view_users_verified', reverse('users.views.verified'))

    def test_view_users_unverified(self):
        self.check_permission('view_users_unverified', reverse('users.views.unverified'))

    def test_view_users_needing_data_correction(self):
        self.check_permission('view_users_needing_data_correction',
                              reverse('users.views.needing_data_correction'))

    def test_view_users_verify(self):
        user = create_test_app_user()
        self.check_permission('view_users_verify', reverse('users.views.verify', args=(user.pk,)))

    def test_view_users_verify2(self):
        # users.views.needs_correction uses the same permission as .verify
        user = create_test_app_user()
        self.check_permission('view_users_verify',
                              reverse('users.views.needs_correction', args=(user.pk,)),
                              self.client.post, incorrect_fields='idunno')

    def test_view_users_profile(self):
        self.check_permission('view_users_profile',
                              reverse('users.views.profile', args=(create_test_app_user().pk,)))

    def test_view_users_profile_purchased(self):
        self.check_permission('view_users_profile_purchased',
                              reverse('users.views.profile_purchased',
                                      args=(create_test_app_user().pk,)))

    def test_view_users_profile_sold(self):
        self.check_permission('view_users_profile_sold', reverse('users.views.profile_sold',
                                                                 args=(create_test_app_user().pk,)))

    def test_view_authentication_profile(self):
        self.check_permission('view_authentication_profile',
                              reverse('authentication.views.profile'))

    def test_view_authentication_profile_purchased(self):
        self.check_permission('view_authentication_profile_purchased',
                              reverse('authentication.views.purchased'))

    def test_view_authentication_profile_sold(self):
        self.check_permission('view_authentication_profile_sold',
                              reverse('authentication.views.sold'))

    def test_purchase_sell_books(self):
        set_sell_purchase_timespan()
        self.check_permission('purchase_sell_books', reverse('purchase:books'))

    def test_purchase_sell_books2(self):
        set_sell_purchase_timespan()
        self.check_permission('purchase_sell_books', reverse('purchase:summary'))

    def test_purchase_sell_books3(self):
        set_sell_purchase_timespan()
        self.check_permission('purchase_sell_books', reverse('sell:books'))

    def test_purchase_sell_books4(self):
        set_sell_purchase_timespan()
        self.check_permission('purchase_sell_books', reverse('sell:summary'))

    def check_permission(self, permission_name, url, response_func=None, **data):
        if response_func is None:
            response_func = self.client.get

        response = response_func(url, data=data)
        self.assertEqual(response.status_code, 403)
        self.user.user_permissions.add(Permission.objects.get(codename=permission_name))
        response = response_func(url, data=data)
        self.assertIn(response.status_code, (200, 302))

    def create_test_order_with_book(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        book = create_test_book(book_type, app_user)
        order = create_test_order(user=app_user)
        book.order = order
        book.save()
        return order
