from unittest import skip
from .base import FunctionalTest
import time

from .page_home_page import HomePage


class LayoutAndStylingTest(FunctionalTest):

    @skip
    def test_can_autoconnect_and_connect_with_persona(self):
        # Alpha goes to the home page
        home = HomePage(self).show()
        window_handle = self.browser.current_window_handle

        # He sees he's not connected
        home.check_connection_status(False)

        # He gets connected automatically using the test environment
        self.create_autoconnected_session("alpha@mail.com")

        # He goes back to the home page to verify he is connected
        home.show()
        content_autoconnected = self.get_body_content()

        # He sees he is, and he disconnects
        self.logout()

        # He now sees he is disconnected
        connect_button = home.get_login_button()

        # He connects through persona
        connect_button.click()

        # A Persona login box appears. He switches to it
        ## Getting the last opened window
        last_handle = ''
        for temp_handle in self.browser.window_handles:
            last_handle = temp_handle

        self.browser.switch_to.window(last_handle)

        # He logs in with his other email address
        ## Uses mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email').send_keys('alpha@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.browser.switch_to.window(window_handle)

        # He goes back to the home page to verify he is connected again
        self.wait_to_be_logged_in()
        home.show()
        content_with_persona = self.get_body_content()

        # He confirms that the content of the page is the same as with the other login
        self.assertHTMLEqual(
            content_autoconnected.replace('alpha@mail.com', '[EMAIL]'),
            content_with_persona.replace('alpha@mockmyid.com', '[EMAIL]'))

        # Refreshing the page, he sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in()

    def test_can_autoconnect(self):
        # Alpha goes to the home page
        home = HomePage(self).show()
        window_handle = self.browser.current_window_handle

        # He sees he's not connected
        home.check_connection_status(False)

        # He gets connected automatically using the test environment
        self.create_autoconnected_session(self.faker.email())

        # He goes back to the home page to verify he is connected
        home.show()
        self.get_body_content()

        # He sees he is, and he disconnects
        self.logout()

        # He now sees he is disconnected
        home.get_login_button()

    def _test_centering_for_width(self, width):
        self.browser.set_window_size(width, 1000)
        time.sleep(1)
        HomePage(self).show()
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

    def test_general_contents(self):
        # Alpha goes to the homepage
        home = HomePage(self).show()

        # He sees that there is a message telling the site is using cookies
        link = self.browser.find_element_by_id(home.id_page_uses_cookies)

        # He reloads the page and notices that the box is still there
        self.browser.refresh()

        # He closes the box, then reload the page. He notices that the box doesn't appear anymore
        self.browser.find_element_by_id(home.id_page_uses_cookies).click()
        self.browser.refresh()
        self.assertElementNotFoundById(home.id_page_uses_cookies)
