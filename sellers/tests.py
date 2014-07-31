from django.test import LiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver

from books.models import BookType, Book

from common.models import AppUser
from utils.tests import create_test_superuser, login


class SellersLiveTests(LiveServerTestCase):
    def setUp(self):
        user = AppUser(first_name="Test", last_name="Test", student_class="1A", phone_number="111222333")
        user.save()
        type1 = BookType(isbn="9788375940794", publisher="Some", title="Test book", publication_year=2010, price=0,
                         visible=False)
        type2 = BookType(isbn="9788376804538", publisher="Other", title="Another test book", publication_year=2000,
                         price=65.5, visible=True)
        type1.save()
        type2.save()
        Book(book_type=type1, owner=user, accepted=True).save()
        Book(book_type=type1, owner=user, accepted=False).save()
        Book(book_type=type2, owner=user, accepted=False).save()
        Book(book_type=type2, owner=user, accepted=False).save()

        create_test_superuser()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SellersLiveTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SellersLiveTests, cls).tearDownClass()

    def test_accept(self):
        login(self.selenium, self.live_server_url, "test", "test")
        self.selenium.get('%s%s' % (self.live_server_url, '/manage/sellers/'))

        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr')
        self.assertEqual(len(trs), 1)  # Ensure there's only one seller
        trs[0].find_element_by_xpath('//a[contains(@href, "accept")]').click()

        trs = self.selenium.find_elements_by_xpath('//table//tbody//tr')
        self.assertEqual(len(trs), 2)  # Ensure there are two book types

        self.selenium.find_element_by_xpath('//table//tbody//tr//a[contains(@href, "edit")]').click()
        pub_year_field = self.selenium.find_element_by_name('publication_year')
        pub_year_field.clear()
        pub_year_field.send_keys("1990")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        tds = self.selenium.find_elements_by_xpath('//table//tbody//tr//td[text()[normalize-space(.)="1990"]]')
        self.assertEqual(len(tds), 1)  # Ensure we actually changed the book type publication year

        price_field = self.selenium.find_element_by_xpath('//input[contains(@name, "price")]')
        price_field.clear()
        price_field.send_keys("99")
        amount_field = self.selenium.find_element_by_xpath('//input[contains(@name, "amount") and @value=1]')
        amount_field.clear()
        amount_field.send_keys("3")
        amount_field = self.selenium.find_element_by_xpath('//input[contains(@name, "amount") and @value=2]')
        amount_field.clear()
        amount_field.send_keys("0")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        books = Book.objects.all()
        # Check if we actually created and deleted Books by modifying quantities
        self.assertEqual(len(books), 4)
        self.assertEqual(len(books.filter(accepted=True)), 4)  # Check if the Books are accepted now
        # Check whether the BookType which was not visible, is visible now
        self.assertEqual(len(BookType.objects.filter(visible=True)), 2)