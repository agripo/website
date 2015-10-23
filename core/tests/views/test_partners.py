from django.core.urlresolvers import reverse

from core.tests.views.base import ViewsBaseTestCase
from core.models.partners import Partner


class PartnersBaseTestCase(ViewsBaseTestCase):

    def _insert_random_partners(self, quantity):
        created_partners = []
        for i in range(quantity):
            partner_name = "Partner #{}".format(i)
            partner = Partner.objects.create(
                name=partner_name,
                description="Description of {}".format(partner_name),
                website="http://{}".format(partner_name.replace(" ", "_")))
            created_partners.append(partner)

        return created_partners


class PartnersViewTest(PartnersBaseTestCase):

    def _assert_partners_page_contains(self, text, quantity):
        response = self.client.get(reverse('partners_page'))
        self.assertContains(response, text, quantity)

    def test_use_template(self):
        response = self.client.get(reverse('partners_page'))
        self.assertTemplateUsed(response, 'core/partners_page.html')

    def test_display_each_partner_s_name(self):
        partners = self._insert_random_partners(5)
        for partner in partners:
            self._assert_partners_page_contains('<h2>{}</h2>'.format(partner.name), 1)

    def test_contains_each_partner_s_description(self):
        partners = self._insert_random_partners(5)
        for partner in partners:
            self._assert_partners_page_contains('<p>{}</p>'.format(partner.description), 1)

    def test_contains_each_partner_s_website(self):
        partners = self._insert_random_partners(5)
        for partner in partners:
            self._assert_partners_page_contains('<a href="{}"'.format(partner.website), 1)

    def test_partners_page_displays_message_if_no_partners(self):
        self._assert_partners_page_contains('id="no_partner_to_show_message', 1)


class PartnersRightModuleTest(PartnersBaseTestCase):

    def test_right_module_displays_block_if_there_are_partners(self):
        self._insert_random_partners(5)
        response = self.client.get(reverse('home_page'))
        self.assertContains(response, '"partnersCarousel"')

    def test_right_module_displays_all_partners(self):
        self._insert_random_partners(5)
        response = self.client.get(reverse('home_page'))
        self.assertContains(response, '"carousel_one_partner_name"', 5)

    def test_right_module_hides_block_if_no_partners(self):
        response = self.client.get(reverse('home_page'))
        self.assertNotContains(response, '"partnersCarousel"')
