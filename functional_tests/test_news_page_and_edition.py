from unittest import skip
from .base import FunctionalTest
import time

from .page_news import NewsPage
from selenium import webdriver


class LayoutAndStylingTest(FunctionalTest):

    def test_can_add_news_to_news_page(self):
        ## Prepopulating the news page
        #@todo Add some automatically generated news to the page

        # Alpha gets connected, then goes to the news page
        self.create_autoconnected_session("alpha@mail.com")
        news_page_alpha = NewsPage(self).show()
        previous_content_alpha = self.get_element_content_by_id(news_page_alpha.id_news_list_container)
        alpha_browser = self.browser

        # Bravo, his friend, also goes to this page, but without connexion
        bravo_browser = webdriver.Firefox()
        self.browser = bravo_browser
        news_page_bravo = NewsPage(self).show()
        previous_content_bravo = self.get_element_content_by_id(news_page_bravo.id_news_list_container)

        # Alpha and bravo are seeing the same news
        self.assertHTMLEqual(previous_content_alpha, previous_content_bravo,
                             "Alpha and bravo should see the same news")

        # Alpha goes to the administration page, and adds a news
        self.browser = alpha_browser

        # Bravo refreshes his screen, and sees that brand new news

        # Alpha modifies this last news, as there was a typo in it

        # Bravo confirms it has been modified too

        # Alpha removes a previous news that had nothing to do there

        # Bravo confirms the news has disappeared

        # Alpha goes to check the news page himself, and they see the same things
