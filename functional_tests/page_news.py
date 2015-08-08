from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class NewsPage(object):
    id_page = "id_news_page"
    id_news_list_container = "id_news_list_container"

    def __init__(self, test):
        self.test = test

    def show(self):
        self.test.browser.get(reverse("news_page"))
        self.test.wait_for(self._is_news_page)
        return self

    def _is_news_page(self):
        return self.test.browser.find_element_by_id(self.id_page)
