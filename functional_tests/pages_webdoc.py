from django.core.urlresolvers import reverse


class WebdocPages(object):
    id_webdoc_pages = "id_webdoc_pages"
    all_pages = ['home_page', 'project', 'support', 'partners', 'credits']

    def __init__(self, test):
        self.test = test

    def show(self, page="home"):
        self.test.assertIn(page, self.all_pages)
        page_url = reverse("webdoc:{}".format(page))
        self.test.browser.get("{}{}".format(self.test.server_url, page_url))
        self.test.wait_for(self._is_a_webdoc_s_page)
        return self

    def _is_a_webdoc_s_page(self):
        return self.test.browser.find_element_by_id(self.id_webdoc_pages)
