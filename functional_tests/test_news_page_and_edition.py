import datetime
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time


from .base import FunctionalTest
from .page_news import NewsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except ProcessLookupError:
        pass


class LayoutAndStylingTest(FunctionalTest):

    def test_can_add_news_to_news_page(self):
        ## Prepopulating the news page
        #@todo Add some automatically generated news to the page

        faker = self.faker

        # Alpha gets connected as manager
        user_alpha = self.create_autoconnected_session(self.faker.email(), as_manager=True)

        # He goes to the news page
        news_page_alpha = NewsPage(self).show()
        previous_content_alpha = self.get_element_content_by_id(news_page_alpha.id_news_list_container)
        alpha_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(alpha_browser))

        # Bravo, his friend, also goes to this page, but without connexion
        bravo_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(bravo_browser))
        self.browser = bravo_browser
        news_page_bravo = NewsPage(self).show()
        previous_content_bravo = self.get_element_content_by_id(news_page_bravo.id_news_list_container)

        # Alpha and bravo are seeing the same news
        self.assertHTMLEqual(previous_content_alpha, previous_content_bravo,
                             "Alpha and bravo should see the same news")

        # Alpha goes to the administration page
        self.browser = alpha_browser
        self.show_admin_page("core", 'news', 'add')  # Base admin page

        # Alpha fills and saves the form to create a news published today
        the_news_title = faker.sentence()
        the_news_content = "\n".join(faker.paragraphs())
        self.browser.find_element_by_id(news_page_alpha.id_field_title).send_keys(the_news_title)
        self.browser.find_element_by_css_selector(
            'input#{} ~ span a'.format(news_page_alpha.id_field_publication_date)).click()
        self.browser.find_element_by_id(news_page_alpha.id_field_content).send_keys(the_news_content)
        self.select_option_by_text(news_page_alpha.id_field_writer, user_alpha.username, ValueError)
        self.browser.find_element_by_css_selector('input[name="_save"]').click()

        # He waits for for the confirmation to show up
        self.wait_for(lambda: self.browser.find_element_by_css_selector("li.success"), 10)
        self.assertEqual(self.browser.current_url, self.server_url+'/admin/core/news/')

        # Bravo refreshes his screen, and sees that brand new news
        self.browser = bravo_browser
        self.browser.refresh()

        all_news = self.browser.find_elements_by_class_name('one_news_title')
        found = False
        for one_news in all_news:
            if one_news.text == the_news_title:
                found = True
                the_news_element = one_news

        self.assertTrue(found, "The new news hasn't been found in the page")

        # He goes to check the news on its page
        l = reverse("one_news_page", kwargs={'pk': 1})
        the_news_element.find_element_by_css_selector("a[href='{}']".format(l)).click()

        # and sees the news is displayed correctly
        news_element = self.browser.find_element_by_id(NewsPage.id_news_title) # Should not raise
        self.assertEqual(news_element.text, the_news_title)

        # Alpha modifies this last news, as there was a typo in it
        self.browser = alpha_browser
        self.click_link(reverse('admin:core_news_change', args=(1,)), timeout=10)
        id_field = self.browser.find_element_by_id(news_page_alpha.id_field_title)
        id_field.clear()

        the_news_title = faker.sentence()  # Generating a new different title
        id_field.send_keys(the_news_title)
        self.browser.find_element_by_css_selector('input[name="_save"]').click()

        # He waits for for the confirmation to show up
        self.wait_for(lambda: self.browser.find_element_by_css_selector("li.success"), 10)
        self.assertEqual(self.browser.current_url, self.server_url+'/admin/core/news/')

        # Bravo confirms it has been modified too
        self.browser = bravo_browser
        self.browser.refresh()
        h1 = self.browser.find_element_by_css_selector('h1')

        self.assertEqual(h1.text, the_news_title, "The new news hasn't been found in the page")

        # Alpha removes a previous news that had nothing to do there

        # Bravo confirms the news has disappeared

        # Alpha goes to check the news page himself, and they see the same things

        # Bravo tries to access the edition page, but gets a 403 error

        # He creates an account, to be able to edit the news

        # He still gets a 403 error, as he isn't in the managers group
        time.sleep(5)
        self.fail('This is where we are!')
