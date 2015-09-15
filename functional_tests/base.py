import os
import time
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import WebDriverException, TimeoutException, StaleElementReferenceException
from faker import Factory as FakerFactory
from django.utils import timezone

from core.authentication import is_production_server, is_staging_server
from .page_home_page import HomePage
from core.models import AgripoUser as User


DEFAULT_TIMEOUT = 5
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


def quit_if_possible(browser):
    try:
        browser.quit()
    except ProcessLookupError:
        pass


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if is_production_server():
            cls.server_url = 'http://not_a_valid_domain_name/at_all'
        elif is_staging_server():
            cls.server_url = 'http://' + settings.SERVER_URL
        else:
            super().setUpClass()
            cls.server_url = cls.live_server_url

    def setUp(self):
        if is_production_server():
            self.fail("Tests should never be launched on production server")
            return
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(0)
        self.faker = FakerFactory.create('fr_FR')

        # @todo remove this when it is not needed anymore (should be done by the migration #3
        from django.contrib.auth.models import Group, Permission
        if not Group.objects.all():
            from core.models import make_permissions
            make_permissions(Group, Permission)
        # End of the removable stuff

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
        timestamp = timezone.now().isoformat().replace(':', '.')[:19]
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

    def wait(self, duration):
        time.sleep(duration)

    def wait_for_element_with_id(self, element_id, timeout=DEFAULT_TIMEOUT):
        selector = '#{}'.format(element_id)
        return self.wait_for_element_with_selector(selector, timeout)

    def wait_for_element_with_selector(self, selector, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.browser, timeout=timeout).until(
            lambda b: b.find_element_by_css_selector(selector),
            'Could not find element with selector "{}". Page text was:\n{}'.format(
                selector, self.browser.find_element_by_tag_name('body').text
            )
        )
        return self.browser.find_element_by_css_selector(selector)

    def wait_for_stale(self, existing_element, timeout=DEFAULT_TIMEOUT):

        def element_has_gone_stale(element):
            try:
                element.is_displayed()
                return False
            except StaleElementReferenceException:
                return True

        while not element_has_gone_stale(existing_element):
            timeout -= 0.1
            self.wait(0.1)
            if timeout <= 0:
                raise Exception("The element {} never became stale".format(existing_element))

    def click_link(self, link, timeout=DEFAULT_TIMEOUT, search_in=None, changes_page=True):
        if timeout > 0:
            self.wait_for_link_with_destination(link, timeout=timeout, search_in=search_in)

        link = self.get_link_by_destination(link, search_in=search_in)
        link.click()
        if changes_page:
            start_time = time.time()
            self.wait_for_stale(link)

    def wait_for_element_to_be_displayed(self, element, timeout=DEFAULT_TIMEOUT):
        self.wait_for(
            lambda: self.assertTrue(element.is_displayed()), timeout, exception=AssertionError)

        return element

    def get_link_by_destination(self, destination, search_in=None):
        if not search_in:
            search_in = self.browser

        return search_in.find_element_by_css_selector('a[href="{}"]'.format(destination))

    def wait_for_link_with_destination(self, destination, timeout=DEFAULT_TIMEOUT, search_in=None):
        WebDriverWait(self, timeout=timeout).until(
            lambda b: b.get_link_by_destination(destination, search_in=search_in),
            'Could not find link with href={}. Page text was:\n{}'.format(
                destination, self.browser.find_element_by_tag_name('body').text
            )
        )

    def get_element_content_by_id(self, id_element):
        return self.browser.find_element_by_id(id_element).text

    def get_body_content(self):
        return self.browser.find_element_by_css_selector('body').text

    def logout(self):
        HomePage(self).get_logout_button().click()
        self.wait_to_be_logged_out()

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id(HomePage(self).id_logout)

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id(HomePage(self).id_login)

    def assertElementNotFoundById(self, element_id):
        try:
            self.wait_for_element_with_id(element_id, 2)
        except TimeoutException:
            return True
        self.fail("The element {} shouldn't have been found in the dom".format(element_id))

    def wait_for(self, function_with_assertion, timeout=DEFAULT_TIMEOUT, exception=(AssertionError, WebDriverException)):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except exception:
                print("Exception intercepted")
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()

    def show_page(self, page, timeout=DEFAULT_TIMEOUT, searched_element='id_top_container'):
        if page[0] != '/':
            page = '/{}'.format(page)
        self.browser.get("{}{}".format(self.server_url, page))
        return self.wait_for(lambda: self.browser.find_element_by_id(searched_element), timeout)

    def show_admin_page(self, *args):
        self.show_page('admin/', searched_element="user-tools")
        next_page = '/admin/'
        for arg in args:
            next_page += arg + "/"
            self.click_link(next_page, timeout=DEFAULT_TIMEOUT)

    def create_autoconnected_session(self, email, as_manager=False):
        active_page = self.browser.current_url
        # We visit the page that immediately creates the session :
        if as_manager:
            page = 'auto_manager_login'
            connected_as = "manager"
        else:
            page = 'auto_login'
            connected_as = "user"
        self.browser.get("{}/core/{}/{}".format(self.server_url, page, email))
        # We check that we are authenticated
        body = self.browser.find_element_by_css_selector('body')
        self.assertEqual("{} is connected as {}".format(email, connected_as), body.text)
        # We go back to previous page or home page if there was none
        if active_page != "about:blank":
            self.browser.get(active_page)
        else:
            HomePage(self).show()
        self.wait_to_be_logged_in()
        return self

    def add_user_to_managers(self, email):
        user = User.objects.get(email=email)
        user.add_to_managers()

    def select_option_by_text(self, select_id, option_text, raised_error_if_not_found=None):
        select = Select(self.browser.find_element_by_id(select_id))
        for opt in select.options:
            if opt.text == option_text:
                opt.click()
                return

        if raised_error_if_not_found:
            raise raised_error_if_not_found('"{}" not found in the select #{}'.format(option_text, select_id))
