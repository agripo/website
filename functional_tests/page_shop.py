from django.core.urlresolvers import reverse


class ShopPage(object):
    id_page = "id_shop_page"
    id_field_name = "id_name"
    id_field_category = "id_category"
    id_field_price = "id_price"

    def __init__(self, test):
        self.test = test

    def show(self):
        self.test.browser.get(self.test.server_url+reverse("shop_page"))
        self.test.wait_for(self._is_shop_page)
        return self

    def _is_shop_page(self):
        return self.test.browser.find_element_by_id(self.id_page)
