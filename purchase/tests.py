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

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from books.models import OrderedBook
from authentication.models import AppUser
from orders.models import Order
from utils.test_utils import create_test_accepted_user, login


class PurchaseWizardLiveTest(StaticLiveServerTestCase):
    fixtures = ['purchase-test-data.json']

    def setUp(self):
        create_test_accepted_user()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(PurchaseWizardLiveTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(PurchaseWizardLiveTest, cls).tearDownClass()

    def test_purchase_wizard(self):
        login(self.selenium, self.live_server_url, "test", "test")

        self.selenium.get('%s%s' % (self.live_server_url, '/purchase/'))
        # Click "Add" 3 times (twice on one book and once on another)
        for i in range(3):
            self.selenium.find_element_by_xpath('//div[@id="bookList"]//button[not(@disabled="disabled")]').click()
        trs = self.selenium.find_elements_by_xpath('//div[@id="bookList"]//table//tbody//tr[contains('
                                                   '@class, "bg-error")]')
        self.assertEqual(len(trs), 2)  # Check if the user see 2 "disabled" book types
        self.selenium.find_element_by_name('btn-next').click()

        trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(trs), 2)  # Ensure user actually see 2 book types

        self.selenium.find_element_by_name('btn-back').click()
        # Remove one book
        self.selenium.find_element_by_xpath('//table[@id="chosen-book-list"]//tbody//tr[@data-pk="1"]//button[contains'
                                            '(@class, "btn-remove-book")]').click()
        self.selenium.find_element_by_name('btn-next').click()

        trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(trs), 2)  # Check if after removing a book we still have 2 book types

        self.__create_test_order(1, 2)
        self.selenium.find_element_by_name('btn-next').click()
        # Ensure user sees now "Your order was modified" alert because of other user that just stole their book
        self.selenium.find_element_by_xpath('//div[contains(@class, "message") and '
                                            'contains(@class, "warning")]')
        trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(trs), 1)  # ...and we have one book type now
        self.selenium.find_element_by_name('btn-next').click()

        self.assertEqual(Order.objects.count(), 2)  # Check if the Order was added
        # Check if user reserves the book now
        self.__check_ordered_book_added()

    def __create_test_order(self, user, book_type, count=1):
        order = Order(user_id=user)
        order.save()
        OrderedBook(book_type_id=book_type, count=count, order=order).save()

    def __check_ordered_book_added(self):
        user = AppUser.objects.get(username="test")
        order = Order.objects.get(user=user)
        ordered_book = OrderedBook.objects.filter(order=order)
        self.assertEqual(ordered_book.count(), 1)
        self.assertEqual(ordered_book[0].count, 1)
