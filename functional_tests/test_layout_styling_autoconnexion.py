from unittest import skip
from .base import FunctionalTest
import time


class LayoutAndStylingTest(FunctionalTest):

    def test_can_autoconnect(self):
        # Alpha goes to the home page
        self.show_page("", 1)

        # He sees he's not connected
        self.browser.find_element_by_id('id_login')

        # He gets connected automatically using the test environment
        self.create_autoconnected_session("alpha@mail.com")

        # He goes back to the home page to verify he is connected
        self.show_page("", 1)

        # He sees he is
        self.browser.find_element_by_id('id_logout')

    def _test_centering_for_width(self, width):
        self.browser.set_window_size(width, 1000)
        time.sleep(1)
        self.show_page("")
        new_width = self.browser.get_window_size()['width']
        if new_width != width:
            print("The width has been resized from {} to {} because the screen wasn't "
                  "big enough".format(width, new_width))

        top_container = self.browser.find_element_by_id('id_top_container')
        self.assertAlmostEqual(
            top_container.location['x'] + top_container.size['width'] / 2,
            new_width / 2,
            delta=8
        )

    def test_layout_and_styling(self):
        # Alpha goes to the home page with various screen sizes and check that the menu bar is centered
        self._test_centering_for_width(600)
        self._test_centering_for_width(800)
        self._test_centering_for_width(1024)
        self._test_centering_for_width(1920)
