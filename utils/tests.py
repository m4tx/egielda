from django.contrib.auth.models import User


def create_test_superuser():
    if User.objects.filter(username="test").count() == 0:
        User.objects.create_superuser("test", "test@localhost", "test")


def login(selenium, live_server_url, username, password):
    selenium.get('%s%s' % (live_server_url, '/accounts/login/'))
    selenium.find_element_by_name('username').send_keys(username)
    selenium.find_element_by_name('password').send_keys(password)
    selenium.find_element_by_xpath('//button[@type="submit"]').click()