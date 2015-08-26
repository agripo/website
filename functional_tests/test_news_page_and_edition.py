from django.core.urlresolvers import reverse
from selenium import webdriver
import time

from core.models import SiteConfiguration
from core.authentication import get_username_from_email
from core.models import News, Icon
from .base import FunctionalTest, quit_if_possible
from .page_news import NewsPage

config = SiteConfiguration.objects.get()

class NewsAndNewsListPagesTest(FunctionalTest):

    def populate_db(self, count):
        from core.icons import import_icons
        import_icons(Icon)
        url = reverse('populate_db', kwargs={'news_count': count})
        self.show_page(url, searched_element="ok")

    def test_can_add_news_to_news_page(self):
        faker = self.faker

        # Alpha gets connected as manager
        user_alpha_email = faker.email()
        user_alpha_username = get_username_from_email(user_alpha_email)
        self.create_autoconnected_session(user_alpha_email, as_manager=True)

        # # Prepopulating the news page
        randomly_created_news_count = config.news_count * 2 + 1
        self.populate_db(randomly_created_news_count)

        # He goes to the news page
        news_page_alpha = NewsPage(self).show()
        previous_content_alpha = self.get_element_content_by_id(news_page_alpha.id_news_list_container)
        alpha_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(alpha_browser))

        # He sees that there are already some news on the page, and a paginator for the next ones
        all_news = self.browser.find_elements_by_css_selector('#id_news_list_container .news_container h4')
        self.assertEqual(
            len(all_news), config.news_count, 'Did not find the right number of news on the page')
        self.browser.find_element_by_css_selector('.pagination_block a.pagination-next')  # should not raise an error

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
            'input#{} ~ span a'.format(news_page_alpha.id_field_publication_date_date)).click()
        self.browser.find_element_by_css_selector(
            'input#{} ~ span a'.format(news_page_alpha.id_field_publication_date_time)).click()
        self.browser.find_element_by_id(news_page_alpha.id_field_content).send_keys(the_news_content)
        self.select_option_by_text(news_page_alpha.id_field_writer, user_alpha_username, ValueError)
        self.browser.find_element_by_css_selector('input[name="_save"]').click()
        # He selects an icon for this news
        #@todo : create a test for the icon selector

        #@todo : create tests to check that the icons are present in all pages where the news are shown

        # He waits for for the confirmation to show up
        self.wait_for(lambda: self.browser.find_element_by_css_selector("li.success"), 10)
        self.assertEqual(self.browser.current_url, self.server_url+'/admin/core/news/')

        # Bravo refreshes his screen, and sees that brand new news
        self.browser = bravo_browser
        news_page_bravo.show(True)

        all_news = self.browser.find_elements_by_css_selector('#id_news_list_container .news_container h4')
        found = False
        for one_news in all_news:
            if the_news_title[:25] in one_news.text:
                found = True
                the_news_element = one_news

        self.assertTrue(found, "The new news hasn't been found in the page")

        # He goes to check the news on its page
        l = reverse("one_news_page", kwargs={'pk': randomly_created_news_count + 1})
        the_news_element.find_element_by_css_selector('a[href="{}"]'.format(l)).click()

        # and sees the news is displayed correctly
        news_element = self.browser.find_element_by_id(NewsPage.id_news_title) # Should not raise
        self.assertEqual(news_element.text[:25], the_news_title[:25])

        #@todo : He shoud also take a look at the news block at the bottom of the page

        # Alpha modifies this last news, as there was a typo in it
        self.browser = alpha_browser
        self.click_link(reverse('admin:core_news_change', args=(randomly_created_news_count + 1,)), timeout=10)
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
        self.assertEqual(h1.text[:25], the_news_title[:25], "The new news hasn't been found in the page")

        # Bravo notices that there is an "Older news" button, so he follows it
        #@todo : create another news to check the link to previous and to next news
        #self.click_link(reverse("one_news_page", kwargs={'pk': randomly_created_news_count}))

        # Alpha removes a previous news that had nothing to do there

        # Bravo confirms the news has disappeared

        # Alpha goes to check the news page himself, and they see the same things

        # Bravo tries to access the edition page, but gets a 403 error

        # He creates an account, to be able to edit the news

        # He still gets a 403 error, as he isn't in the managers group
        time.sleep(5)

        self.fail('Some tests are missing here !')
