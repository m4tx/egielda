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
from decimal import Decimal

from django.contrib.staticfiles.testing import StaticLiveServerCase

from selenium.webdriver.firefox.webdriver import WebDriver

from selenium.webdriver.support.wait import WebDriverWait

from books.models import BookType

from utils.tests import create_test_superuser, login


class BooksLiveTest(StaticLiveServerCase):
    def setUp(self):
        BookType(pk=1, isbn="9788375940794", publisher="Some", title="A book",
                 publication_year=1995, price=20.50, visible=False).save()
        create_test_superuser()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(BooksLiveTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BooksLiveTest, cls).tearDownClass()

    def test_books(self):
        login(self.selenium, self.live_server_url, "test", "test")
        self.selenium.get('%s%s' % (self.live_server_url, '/manage/books/'))

        self.selenium.find_element_by_xpath('//a[contains(@href, "books/add")]').click()
        self.selenium.find_element_by_name('isbn').send_keys("9780262033848")
        # "Find by ISBN" button
        self.selenium.find_element_by_name('isbn').find_element_by_xpath('..//button').click()
        self.selenium.find_element_by_name('price').send_keys("60.99")
        WebDriverWait(self.selenium, 15).until(lambda driver: self.get_input_value('title', driver) != "")
        self.assertEqual(self.get_input_value('publisher'), "MIT Press")
        self.assertEqual(self.get_input_value('title'), "Introduction to Algorithms")
        self.assertEqual(self.get_input_value('publication_year'), "2009")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        BookType.objects.get(isbn="9780262033848", publisher="MIT Press", title="Introduction to Algorithms",
                             publication_year=2009, price=Decimal("60.99"), visible=True)
        self.assertEqual(BookType.objects.count(), 2)

        # Create one more book
        self.selenium.find_element_by_xpath('//a[contains(@href, "books/add")]').click()
        self.selenium.find_element_by_name('isbn').send_keys("9780262033840")
        self.selenium.find_element_by_name('publisher').send_keys("Test publisher")
        self.selenium.find_element_by_name('title').send_keys("Test book")
        self.selenium.find_element_by_name('publication_year').send_keys("2000")
        self.selenium.find_element_by_name('price').send_keys("30")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr[not(contains(@class, "info"))]')
        self.assertEqual(len(trs), 3)  # Ensure admin sees 3 book types

        self.assertEqual(BookType.objects.get(pk=1).visible, False)
        self.selenium.find_element_by_xpath('//a[contains(@href, "1/edit")]').click()
        self.selenium.find_element_by_name('title').clear()
        self.selenium.find_element_by_name('title').send_keys("Brand new title!")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        # Ensure the title was changed
        self.assertEqual(BookType.objects.get(pk=1).title, "Brand new title!")
        # Ensure that visible was set to true
        self.assertEqual(BookType.objects.get(pk=1).visible, True)

        self.selenium.find_element_by_xpath('//a[contains(@href, "1/remove")]').click()
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr[not(contains(@class, "info"))]')
        self.assertEqual(len(trs), 2)
        self.assertEqual(BookType.objects.count(), 2)

        self.selenium.find_element_by_xpath('//table//thead//input[@id="select-all"]').click()
        trs = self.selenium.find_elements_by_xpath(
            '//table//tbody//tr[contains(@class, "active")]//input[@type="checkbox"]')
        self.assertEqual(len(trs), 2)  # Ensure everything is selected

        # Bulk remove button
        self.selenium.find_element_by_xpath(
            '//table//tfoot//tr[contains(@class, "info")]//button[@type="submit"]').click()
        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr')
        self.assertEqual(len(trs), 2)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Ensure user sees the "Nothing to display" alert
        self.selenium.find_element_by_xpath('//div[contains(@class, "alert-info")]')

        self.assertEqual(BookType.objects.count(), 0)

    def get_input_value(self, name, driver=None):
        if driver is None:
            driver = self.selenium
        return driver.find_element_by_name(name).get_attribute('value')
