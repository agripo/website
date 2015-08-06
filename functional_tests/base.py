import os
import time
from datetime import datetime
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException


from accounts.authentication import is_production_server, is_staging_server


DEFAULT_WAIT = 5
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if is_production_server():
            cls.server_url = 'http://not_a_valid_domain_name/at_all'
        elif is_staging_server():
            cls.server_url = 'http://' + settings.STAGING_SERVER
        else:
            super().setUpClass()
            cls.server_url = cls.live_server_url

    def setUp(self):
        if is_production_server():
            self.fail("Tests should never be launched on production server")
            return
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def logout(self):
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_login')

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()

    def show_page(self, page, timeout=DEFAULT_WAIT):
        self.browser.get("{}/{}".format(self.server_url, page))
        return self.wait_for(lambda: self.browser.find_element_by_id('id_top_container'), timeout)

    def create_autoconnected_session(self, email):
        # We visit the page that immediately creates the session :
        self.browser.get("{}/accounts/auto_login/{}".format(self.server_url, email))
        # We check that we are authenticated
        body = self.browser.find_element_by_css_selector('body')
        self.assertEqual("{} is connected".format(email), body.text)
