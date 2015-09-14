from time import sleep
from django.core.management import call_command

from functional_tests.base import FunctionalTest
from functional_tests.page_home_page import HomePage


class StaticPagesTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        call_command('loaddata', 'core/flatpages_contents.json')

    def _go_to_page_from_menu(self, menu, page):
        if self._small_screen:
            self.browser.find_element_by_css_selector(".navbar-toggle").click()

        menu_link = "/menu_{}/".format(menu.lower())
        self.click_link(menu_link)
        link = "/{}/".format(page)
        self.click_link(link)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '[data-url="{}"]'.format(link)), 10)

    def _test_display_all_static_pages(self):
        # Alpha goes to the home page
        HomePage(self).show()

        # He follows the pages' links one by one
        self._go_to_page_from_menu("Agripo", "qui-sommes-nous")

        sleep(5)

    def test_display_all_static_pages_big_screen(self):
        self.browser.set_window_size(1280, 500)
        self._small_screen = False
        self._test_display_all_static_pages()

    def test_display_all_static_pages_small_screen(self):
        self.browser.set_window_size(500, 500)
        self._small_screen = True
        self._test_display_all_static_pages()
