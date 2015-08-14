from django.core.urlresolvers import reverse


class NewsPage(object):
    id_page = "id_news_list_page"
    id_news_list_container = "id_news_list_container"
    id_field_title = 'id_title'
    id_field_publication_date = 'id_publication_date'
    id_field_content = 'id_content'
    id_field_writer = 'id_writer'
    id_news_title = 'id_news_title'

    def __init__(self, test):
        self.test = test

    def show(self):
        self.test.browser.get(self.test.server_url+reverse("news_page"))
        self.test.wait_for(self._is_news_page)
        return self

    def _is_news_page(self):
        return self.test.browser.find_element_by_id(self.id_page)
