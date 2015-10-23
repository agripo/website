import re
from django.utils import timezone

from .base import FunctionalTest
from django.core.urlresolvers import reverse
from functional_tests.page_home_page import HomePage
from functional_tests.rich_text_editor import RichTextEditor
from .page_partners import PartnersPage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select


class PartnersPageTest(FunctionalTest):


    def test_can_add_partner(self):
        faker = self.faker
        user_alpha_email = faker.email()  # We want a different email each time (for staging)

        HomePage(self).show()

        # Alpha gets connected as manager
        self.create_autoconnected_session(user_alpha_email, as_manager=True)

        # He adds a partner
        self.show_admin_page("core", 'partner', 'add')
        name_field = self.browser.find_element_by_id("id_name")
        name_field.clear()
        partner_name = faker.sentence()[:50]
        name_field.send_keys(partner_name)

        faker.seed(500)  # There sometimes are problems with generated texts, so we send some that is working
        title = faker.sentence()
        content = faker.paragraphs()
        editor = RichTextEditor(self, "id_description")
        editor.empty_content()
        bold_button = self.browser.find_element_by_css_selector(".cke_button__bold")
        bold_button.click()
        editor.insert_content(title)
        bold_button.click()
        editor.insert_content("\n")
        for p in content:
            editor.insert_content(p)
            editor.insert_content("\n")

        self.admin_save('/admin/core/partner/')

        # He then goes to the home page and sees a link to the partners page
        self.browser.find_elements_by_link_text("Tous les partenaires").click()

        # On this page, he sees a link to the new partner's page
        self.browser.find_elements_by_link_text(partner_name).click()

        # He sees all the contents he inserted in the partner's description
        index_content = self.browser.find_element_by_css_selector("#partners_content").get_attribute('innerHTML')
        self.assertInHTML(
            '<p><strong>{}</strong></p>'.format(title),
            index_content)

        for p in content:
            self.assertInHTML(
                '<p>{}</p>'.format(p),
                index_content)
