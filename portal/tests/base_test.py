import socket
import time

from django.contrib.sites.models import Site
from django.urls import reverse

from deploy import captcha

# Uncomment to use FireFox
# master_browser = webdriver.Firefox()
from portal.tests.pageObjects.portal.home_page import HomePage
from .selenium_test_case import SeleniumTestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from saucebindings.options import SauceOptions
from saucebindings.session import SauceSession


# class BaseTest(SeleniumTestCase):
class BaseTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()
        cls.orig_captcha_enabled = captcha.CAPTCHA_ENABLED
        captcha.CAPTCHA_ENABLED = False

        options = SauceOptions.chrome()
        options.screen_resolution = "1920x1080"

        cls.sauce_session = SauceSession(options=options)
        cls.sauce_session.start()
        cls.selenium = cls.sauce_session.driver

    @classmethod
    def tearDownClass(cls):
        captcha.CAPTCHA_ENABLED = cls.orig_captcha_enabled
        cls.sauce_session.stop(True)
        super(BaseTest, cls).tearDownClass()

    def go_to_homepage(self):
        path = reverse("home")
        self._go_to_path(path)
        return HomePage(self.selenium)

    def _go_to_path(self, path):
        socket.setdefaulttimeout(20)
        attempts = 0
        while attempts <= 3:
            try:
                self.selenium.get(self.live_server_url + path)
            except socket.timeout:
                if attempts > 2:
                    raise
                time.sleep(10)
            else:
                break
            attempts += 1

    def __call__(self, result=None):
        self._set_site_to_local_domain()
        return super().__call__(result)

    def _set_site_to_local_domain(self):
        """
        Sets the Site Django object to the local domain (locally, localhost:8000).
        Needed to generate valid registration and password reset links in tests.
        """
        current_site = Site.objects.get_current()
        current_site.domain = f"{self.server_thread.host}:{self.server_thread.port}"
        current_site.save()
