from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from settings.settings import Settings
from utils.tests import create_test_book_type, create_test_category, create_test_app_user, create_test_book, \
    create_test_order


class ManagePermissionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@localhost", password="test")
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
                              reverse('books.views.remove_book', args=(create_test_book_type().pk,)))

    def test_view_books_book_details(self):
        self.check_permission('view_books_book_details',
                              reverse('books.views.book_details', args=(create_test_book_type().pk,)))

    def test_view_categories_index(self):
        self.check_permission('view_categories_index', reverse('categories.views.index'))

    def test_view_categories_add_category(self):
        self.check_permission('view_categories_add_category',
                              reverse('categories.views.add_category'))

    def test_view_categories_edit_category(self):
        self.check_permission('view_categories_edit_category',
                              reverse('categories.views.edit_category', args=(create_test_category().pk,)))

    def test_view_categories_remove_category(self):
        self.check_permission('view_categories_remove_category',
                              reverse('categories.views.remove_category', args=(create_test_category().pk,)))

    def test_view_categories_list_books(self):
        category = create_test_category()
        book_type = create_test_book_type()
        book_type.categories.add(category)
        self.check_permission('view_categories_list_books', reverse('categories.views.list_books', args=(category.pk,)))

    def test_view_managemenu_index(self):
        self.check_permission('view_managemenu_index', reverse('managemenu.views.index'))

    def test_view_orders_orders_index(self):
        self.check_permission('view_orders_index', reverse('orders.views.index'))

    def test_view_orders_order_details(self):
        self.check_permission('view_orders_order_details',
                              reverse('orders.views.order_details', args=(self.create_test_order_with_book().pk,)))

    def test_view_orders_not_executed(self):
        self.check_permission('view_orders_not_executed', reverse('orders.views.not_executed'))

    def test_view_orders_outdated(self):
        self.check_permission('view_orders_outdated', reverse('orders.views.outdated'))

    def test_view_orders_executed(self):
        self.check_permission('view_orders_executed', reverse('orders.views.executed'))

    def test_view_orders_execute(self):
        self.check_permission('view_orders_execute',
                              reverse('orders.views.execute', args=(self.create_test_order_with_book().pk,)))

    def test_view_orders_execute_accept(self):
        self.check_permission('view_orders_execute_accept',
                              reverse('orders.views.execute_accept', args=(self.create_test_order_with_book().pk,)))

    def test_view_sellers_index(self):
        self.check_permission('view_sellers_index', reverse('sellers.views.index'))

    def test_view_sellers_accept_books(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        create_test_book(book_type, app_user, False)
        self.check_permission('view_sellers_accept_books', reverse('sellers.views.accept_books', args=(app_user.pk,)))

    def test_view_sellers_accept_edit_book(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        create_test_book(book_type, app_user, False)
        self.check_permission('view_sellers_accept_edit_book',
                              reverse('sellers.views.accept_edit_book', args=(app_user.pk, book_type.pk)))

    def test_view_books_remove_seller(self):
        self.check_permission('view_sellers_remove_seller',
                              reverse('sellers.views.remove_seller', args=(create_test_app_user().pk,)))

    def test_view_settings_index(self):
        self.check_permission('view_settings_index', reverse('settings.views.index'))

    def test_view_stats_index(self):
        self.check_permission('view_stats_index', reverse('stats.views.index'))

    def test_view_stats_books_sold(self):
        self.check_permission('view_stats_books_sold', reverse('stats.views.books_sold'))

    def test_view_stats_users(self):
        self.check_permission('view_stats_users', reverse('stats.views.users'))

    def test_view_stats_list_books(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        create_test_book(book_type, app_user)
        Settings().profit_per_book = 1
        self.check_permission('view_stats_list_books', reverse('stats.views.list_books', args=(app_user.pk,)))

    def test_view_stats_books(self):
        self.check_permission('view_stats_books', reverse('stats.views.books'))

    def check_permission(self, permission_name, url, response_func=None):
        if response_func is None:
            response_func = self.client.get

        response = response_func(url)
        self.assertEqual(response.status_code, 403)
        self.user.user_permissions.add(Permission.objects.get(codename=permission_name))
        response = response_func(url)
        self.assertIn(response.status_code, (200, 302))

    def create_test_order_with_book(self):
        app_user = create_test_app_user()
        book_type = create_test_book_type()
        book = create_test_book(book_type, app_user)
        order = create_test_order(user=app_user)
        book.order = order
        book.save()
        return order