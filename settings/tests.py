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

from datetime import datetime, timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from settings.settings import Settings
from utils.dates import datetime_html_format
from utils.test_utils import login, create_test_superuser


class SettingsTest(TestCase):
    def test_settings(self):
        Settings().int_val = 15
        self.assertEqual(Settings('int_val').int_val, '15')
        Settings().str_val = "test"
        self.assertEqual(Settings('str_val').str_val, "test")
        settings = Settings('int_val', 'str_val')
        self.assertEqual(settings.int_val, '15')
        self.assertEqual(settings.str_val, "test")


class SettingsLiveTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        create_test_superuser()
        cls.selenium = WebDriver()
        super(SettingsLiveTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SettingsLiveTest, cls).tearDownClass()

    def test_dates(self):
        # Check if there're no Sell/Purchase buttons on homepage
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        sell_buttons = self.selenium.find_elements_by_css_selector("a[href^='/sell/']")
        self.assertEqual(len(sell_buttons), 0)
        purchase_buttons = self.selenium.find_elements_by_css_selector("a[href^='/purchase/']")
        self.assertEqual(len(purchase_buttons), 0)

        # Sign in as superuser
        login(self.selenium, self.live_server_url, "test", "test")

        # Go to Settings => Dates and set new values for start/end dates
        self.selenium.get('%s%s' % (self.live_server_url, '/manage/settings/'))
        self.selenium.find_element_by_name('start_sell').send_keys(
            datetime_html_format(datetime.now()).replace('T', ' '))
        self.selenium.find_element_by_name('end_sell').send_keys(
            datetime_html_format(datetime.now() + timedelta(1)).replace('T', ' '))
        self.selenium.find_element_by_name('start_purchase').send_keys(
            datetime_html_format(datetime.now()).replace('T', ' '))
        self.selenium.find_element_by_name('end_purchase').send_keys(
            datetime_html_format(datetime.now() + timedelta(1)).replace('T', ' '))
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Check if the buttons shows up now
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        sell_buttons = self.selenium.find_elements_by_css_selector("a[href^='/sell/']")
        self.assertEqual(len(sell_buttons), 1)
        purchase_buttons = self.selenium.find_elements_by_css_selector("a[href^='/purchase/']")
        self.assertEqual(len(purchase_buttons), 1)
