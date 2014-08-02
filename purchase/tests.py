from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.utils import timezone
from selenium.webdriver.firefox.webdriver import WebDriver

from books.models import Book
from common.models import AppUser
from orders.models import Order


class PurchaseWizardTests(StaticLiveServerCase):
    fixtures = ['purchase-test-data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(PurchaseWizardTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(PurchaseWizardTests, cls).tearDownClass()

    def test_purchase_wizard(self):
        self.selenium.get(self.live_server_url + "/purchase/")
        self.selenium.find_element_by_name('first_name').send_keys("User2")
        self.selenium.find_element_by_name('last_name').send_keys("Test2")
        self.selenium.find_element_by_name('student_class').send_keys("1B")
        self.selenium.find_element_by_name('phone_number').send_keys("333222111")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Click "Add" 3 times (twice on one book and once on another)
        for i in range(3):
            self.selenium.find_element_by_xpath('//div[@id="bookList"]//button[not(@disabled="disabled")]').click()
        trs = self.selenium.find_elements_by_xpath('//div[@id="bookList"]//table//tbody//tr[contains('
                                                   '@class, "bg-danger")]')
        self.assertEqual(len(trs), 3)  # Check if the user see 3 "disabled" book types
        self.selenium.find_element_by_id('btn-next').click()

        trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(trs), 2)  # Ensure user actually see 2 book types

        self.selenium.find_element_by_name('btn-back').click()
        # Remove one book
        self.selenium.find_element_by_xpath('//table[@id="chosen-book-list"]//tbody//tr[@data-pk="1"]//button[contains'
                                            '(@class, "btn-remove-book")]').click()
        self.selenium.find_element_by_id('btn-next').click()

        trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(trs), 2)  # Check if after removing a book we still have 2 book types

        Book.objects.filter(pk=1).update(reserved_until=timezone.now() + timedelta(1), reserver_id=1)
        self.selenium.find_element_by_name('btn-next').click()
        # Ensure user sees now "Your order was modified" alert because of other user that just stole their book
        self.selenium.find_element_by_xpath('//div[contains(@class, "alert-warning")]')
        trs = self.selenium.find_elements_by_xpath('//table[@id="chosen-book-list"]//tbody//tr')
        self.assertEqual(len(trs), 1)  # ...and we have one book type now
        self.selenium.find_element_by_name('btn-next').click()

        self.assertEqual(Order.objects.count(), 1)  # Check if the Order was added
        self.assertEqual(AppUser.objects.count(), 2)  # Check if the AppUser was added
        # Check if user reserves the book now
        self.assertEqual(Book.objects.filter(reserved_until__isnull=False,
                                             reserver=AppUser.objects.get(first_name="User2")).count(), 1)
