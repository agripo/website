from django.core.urlresolvers import reverse


class PartnersPage(object):
    id_page = "id_shop_partners"

    def __init__(self, test):
        self.test = test

    def show(self):
        self.test.browser.get(self.test.server_url+reverse("partners_page"))
        self.test.wait_for(self._is_partners_page)
        return self

    def _is_partners_page(self):
        return self.test.browser.find_element_by_id(self.id_page)
