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

from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from books.models import BookType, Book
from settings.settings import Settings
from utils.dates import datetime_to_string
from utils.test_utils import create_test_accepted_user, login


class SellWizardLiveTest(StaticLiveServerTestCase):
    def setUp(self):
        Settings().start_sell = datetime_to_string(timezone.now())
        Settings().end_sell = datetime_to_string(timezone.now() + timedelta(1))
        BookType(isbn='9788375940794', publisher="Some", title="Test book",
                 publication_year=2000, price=16.00, visible=False).save()
        BookType(isbn='9788376804538', publisher="Other", title="Another test book",
                 publication_year=2010, price=32.00, visible=True).save()
        create_test_accepted_user()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SellWizardLiveTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SellWizardLiveTest, cls).tearDownClass()

    def test_sell_wizard(self):
        login(self.selenium, self.live_server_url, "test", "test")

        # # Books
        # Book list
        self.selenium.get('%s%s' % (self.live_server_url, '/sell/'))
        book_trs = self.selenium.find_elements_by_xpath('//div[@id="bookList"]//table//tbody//tr')
        self.assertEqual(len(book_trs), 1)  # Ensure we only see the book with visible=True
        book_trs[0].find_element_by_xpath('//button[contains(@class, "btn-add-book")]').click()  # Add the book
        # Add book form
        self.selenium.find_element_by_xpath('//div[@id="addBookForm"]/preceding-sibling::div[contains(@class, "title")][1]').click()
        WebDriverWait(self.selenium, 5).until(lambda driver: driver.find_element_by_name('isbn').is_displayed())
        self.selenium.find_element_by_name('isbn').send_keys('9781849696845')
        self.selenium.find_element_by_name('publisher').send_keys("Some other")
        self.selenium.find_element_by_name('title').send_keys("Yet another test book")
        self.selenium.find_element_by_name('publication_year').send_keys("2010")
        self.selenium.find_element_by_xpath('//button[@id="btn-add-new-book"]').click()
        # Next
        self.selenium.find_element_by_name('btn-next').click()

        ## Summary
        book_trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(book_trs), 2)
        self.selenium.find_element_by_name('btn-next').click()

        # Success page
        alerts = self.selenium.find_elements_by_xpath('//div[contains(@class, "message") '
                                                      'and contains(@class, "success")]')
        self.assertEqual(len(alerts), 1)  # Ensure the user see the Success alert
        self.assertEqual(len(BookType.objects.all()), 3)  # Check whether the new BookType was actually added
        self.assertEqual(len(Book.objects.all()), 2)  # Check if the Books from the user were added
