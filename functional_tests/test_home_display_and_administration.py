from .base import FunctionalTest, quit_if_possible
from selenium import webdriver

from .page_home_page import HomePage
from .rich_text_editor import RichTextEditor


class HomeTest(FunctionalTest):

    def test_display_and_update_homepage(self):
        faker = self.faker

        # Alpha gets connected as manager
        user_alpha_email = faker.email()
        self.create_autoconnected_session(user_alpha_email, as_manager=True)

        # Alpha goes to the home page
        home_alpha = HomePage(self).show()
        alpha_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(alpha_browser))

        # Alpha creates a content for the home page with a bold first sentence, and set the news number to 8
        faker.seed(1000)  # There sometimes are problems with generated texts, so we send some that is working
        title = faker.sentence()
        content = faker.paragraphs()
        self.browser = alpha_browser
        self.show_admin_page("core", 'siteconfiguration')  # Base admin page

        editor = RichTextEditor(self, home_alpha.id_admin_homepage_content)
        editor.empty_content()
        bold_button = self.browser.find_element_by_css_selector(".cke_button__bold")
        bold_button.click()
        editor.insert_content(title)
        bold_button.click()
        editor.insert_content("\n")
        for p in content:
            editor.insert_content(p)
            editor.insert_content("\n")

        self.browser.find_element_by_css_selector('input[name="_save"]').click()

        # After saving, he sees the message
        self.wait_for(lambda: self.browser.find_element_by_css_selector("ul.messagelist li.info"), 10)
        self.assertEqual(self.browser.current_url, self.server_url+'/admin/')

        # Bravo, his friend, goes to the home page, but without getting connected
        bravo_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(bravo_browser))
        self.browser = bravo_browser
        home_bravo = HomePage(self).show()

        # He sees all the contents inserted by alpha, with the good markup
        index_content = self.browser.find_element_by_css_selector("#main_content .panel-body").get_attribute('innerHTML')
        self.assertInHTML(
            '<p><strong>{}</strong></p>'.format(title),
            index_content)

        for p in content:
            self.assertInHTML(
                '<p>{}</p>'.format(p),
                index_content)
