from django.contrib.staticfiles.testing import StaticLiveServerCase
from selenium.webdriver.firefox.webdriver import WebDriver

from books.models import Book

from utils.tests import create_test_superuser, login


class OrdersLiveTest(StaticLiveServerCase):
    fixtures = ['execute-test-data.json']

    def setUp(self):
        create_test_superuser()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(OrdersLiveTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(OrdersLiveTest, cls).tearDownClass()

    def test_orders(self):
        login(self.selenium, self.live_server_url, "test", "test")
        self.selenium.get(self.live_server_url + "/manage/orders/notexecuted")
        self.selenium.find_element_by_xpath('//td//a[contains(@href, "execute")]').click()
        self.selenium.find_element_by_xpath('//input[@value="2"]').clear()
        self.selenium.find_element_by_xpath('//input[@value="2"]').send_keys("0")
        self.selenium.find_element_by_xpath('//input[@value="1"]').clear()
        self.selenium.find_element_by_xpath('//input[@value="1"]').send_keys("2")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr[not(contains(@class, "bg-info"))]')
        self.assertEqual(len(trs), 2)  # Ensure user see 2 books with the same book types
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        tables = self.selenium.find_elements_by_xpath('//table')
        self.assertEqual(len(tables), 0)  # Ensure there's no table with orders
        self.assertEqual(len(Book.objects.filter(sold=True)), 2)