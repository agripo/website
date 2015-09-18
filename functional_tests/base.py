import os
import time

from core.data.data_migrations import insert_all_permissions
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import WebDriverException, TimeoutException, ElementNotVisibleException, StaleElementReferenceException
from faker import Factory as FakerFactory
from django.utils import timezone
from django.core.urlresolvers import reverse
from core.authentication import is_production_server, is_staging_server
from core.models.general import Icon, SiteConfiguration
from core.models.users import AgripoUser as User
from functional_tests.page_home_page import HomePage

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

    def populate_db(self, news_count=0, products_count=0, categories_count=0):
        from core.data.icons import import_icons
        import_icons(Icon)
        url = reverse('populate_db', kwargs=dict(
            news_count=news_count, products_count=products_count, categories_count=categories_count))
        self.show_page(url, searched_element="ok")

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

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(0)
        self.faker = FakerFactory.create('fr_FR')
        self.faker.seed(None)

        # @todo remove this when it is not needed anymore (should be done by the migration #3 and some others
        from django.contrib.auth.models import Group
        if not Group.objects.all():
            insert_all_permissions()
        # End of the removable stuff

        self.config = SiteConfiguration.objects.get()

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
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

    def not_implemented(self):
        self.fail("Test not implemented yet")

    def dev_point(self, delay=0):
        if delay:
            time.sleep(delay)

        self.fail("Active development pointer")

    def insert_flat_pages_contents(self):
        from core.data.data_migrations import insert_flatpages_contents
        insert_flatpages_contents()

    def assert_is_hidden(self, element_id, by='id'):
        try:
            if by == 'id':
                el = self.browser.find_element_by_id(element_id)
            el.click()
            self.fail("Element {} should have been hidden")
        except ElementNotVisibleException:
            pass

    def admin_save(self, next_page=None):
        self.browser.find_element_by_css_selector('input[name="_save"]').click()
        # We wait for the confirmation to show up
        self.wait_for(lambda: self.browser.find_element_by_css_selector("li.success"), 10)
        if next_page:
            self.assertEqual(self.browser.current_url, "{}{}".format(self.server_url, next_page))

        return self.browser.find_element_by_css_selector("li.success").get_attribute('innerHTML')

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

    def wait_to_be_logged_in(self, timeout=DEFAULT_TIMEOUT):
        self.wait_for_element_with_id(HomePage(self).id_logout, timeout=timeout)

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
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()

    def show_page(self, page, timeout=DEFAULT_TIMEOUT, searched_element='id_top_container'):
        if page[0] != '/':
            page = '/{}'.format(page)
        self.browser.get("{}{}".format(self.server_url, page))
        return self.wait_for(lambda: self.browser.find_element_by_id(searched_element), timeout)

    def show_admin_page(self, *args, directly=False):
        if not directly:
            self.show_page('admin/', searched_element="user-tools")
            next_page = '/admin/'
            for arg in args:
                next_page += arg + "/"
            self.click_link(next_page, timeout=DEFAULT_TIMEOUT)
        else:
            self.show_page('admin/{}/'.format("/".join(args)), searched_element="user-tools")

    def create_autoconnected_session(self, email, as_manager=False, as_farmer=False):
        active_page = self.browser.current_url
        # We visit the page that immediately creates the session :
        if as_manager:
            page = 'auto_manager_login'
            connected_as = "manager"
        else:
            page = 'auto_login'
            connected_as = "user"

        page = "{}/core/{}/{}?as_farmer={}".format(self.server_url, page, email, as_farmer)
        print("Getting page {}".format(page))
        self.browser.get(page)
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

    def select_option_by_text(self, select_id, option_text, raise_error_if_not_found=True):
        return self.select_option(select_id, "text", option_text, raise_error_if_not_found)

    def select_option_by_index(self, select_id, index, raise_error_if_not_found=True):
        return self.select_option(select_id, "index", index, raise_error_if_not_found)

    def select_option(self, select_id, by, value, raise_error_if_not_found=True):
        select = Select(self.browser.find_element_by_id(select_id))
        index = 0
        for opt in select.options:
            if by == "text" and opt.text == value:
                opt.click()
                return

            if by == "index" and index == value:
                opt.click()
                return

            index += 1

        if raise_error_if_not_found:
            if by == "index":
                error_message = 'No option with index {} in the select #{}'
            else:
                error_message = 'Option with value "{}" not found in the select #{}'

            raise ValueError(error_message.format(value, select_id))
