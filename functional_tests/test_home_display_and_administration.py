from .base import FunctionalTest, quit_if_possible
from core.authentication import get_username_from_email
from selenium import webdriver

from .page_home_page import HomePage


class HomeTest(FunctionalTest):

    def test_display_and_update_homepage(self):
        faker = self.faker

        # Alpha gets connected as manager
        user_alpha_email = faker.email()
        user_alpha_username = get_username_from_email(user_alpha_email)
        self.create_autoconnected_session(user_alpha_email, as_manager=True)

        # Alpha goes to the home page
        home_alpha = HomePage(self).show()
        alpha_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(alpha_browser))

        # Bravo, his friend, also goes to this page, but without connexion
        bravo_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(bravo_browser))
        self.browser = bravo_browser
        home_bravo = HomePage(self).show()

        #@todo : alpha should go to the edition page and change the content
        self.browser = alpha_browser
        self.show_admin_page("core", 'siteconfiguration')  # Base admin page

        #@todo : alpha should also insert an image from ckeditor, and use
        # another that is already on the server

        #@todo : bravo should go to the homepage and confirm the images are
        # present, as well as the text

        self.fail('Some tests are missing here !')
