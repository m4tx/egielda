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

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver

from books.models import BookType

from categories.models import Category
from utils.test_utils import create_test_superuser, login


class CategoriesLiveTest(StaticLiveServerTestCase):
    def setUp(self):
        category = Category(name="Test category")
        category.save()
        book_type = BookType(isbn="9788375940794", publisher="Some", title="A book", publication_year=1995, price=20.50,
                             visible=False)
        book_type.save()
        book_type.categories.add(category)
        create_test_superuser()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(CategoriesLiveTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CategoriesLiveTest, cls).tearDownClass()

    def test_categories(self):
        login(self.selenium, self.live_server_url, "test", "test")
        self.selenium.get('%s%s' % (self.live_server_url, '/manage/categories/'))

        book_list_a = self.selenium.find_element_by_xpath('//a[contains(@href, "/list")]')
        self.assertEqual(book_list_a.text, "1")  # Ensure the list says there's 1 book in category
        book_list_a.click()
        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr')
        self.assertEqual(len(trs), 1)  # Check if there's one book in the table

        self.selenium.back()
        self.selenium.find_element_by_xpath('//table//tbody//tr//a[contains(@href, "/remove")]').click()
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        # Ensure that "There's nothing to display" alert is displaying
        self.selenium.find_element_by_xpath('//div[contains(@class, "alert-info")]')
        self.assertEqual(Category.objects.count(), 0)

        self.selenium.find_element_by_xpath('//a[contains(@href, "categories/add")]').click()
        self.selenium.find_element_by_name('name').send_keys("A test category")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr')
        # Ensure the category was added
        self.assertEqual(len(trs), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.all()[0].name, "A test category")

        self.selenium.find_element_by_xpath('//table//tbody//tr//a[contains(@href, "/edit")]').click()
        self.selenium.find_element_by_name('name').clear()
        self.selenium.find_element_by_name('name').send_keys("Brand new name!")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr')
        # Ensure the category was added
        self.assertEqual(len(trs), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.all()[0].name, "Brand new name!")
