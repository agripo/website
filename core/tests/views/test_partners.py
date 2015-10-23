from django.core.urlresolvers import reverse

from core.tests.views.base import ViewsBaseTestCase
from core.models.partner import Partner


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

    def test_display_all_partners(self):
        self._insert_random_partners(5)
        for partner in Partner.objects.all():
            self._assert_partners_page_contains(partner.name, 1)

    def test_display_link_to_each_partner(self):
        partners = self._insert_random_partners(5)
        for partner in partners:
            self._assert_partners_page_contains('<a href="{}"'.format(reverse("partner_page", partner.id)), 1)

    def test_partners_page_displays_message_if_no_partners(self):
        self._assert_partners_page_contains('id="no_partner_to_show_message', 1)

    def test_right_module_hides_block_if_no_partners(self):
        response = self.client.get(reverse('home_page'))
        self.assertNotContains(response, "")


class OnePartnerViewTest(PartnersBaseTestCase):

    def _assert_partner_page_contains(self, partner_id, text, quantity):
        response = self.client.get(reverse('partner_page', partner_id))
        self.assertContains(response, text, quantity)

    def test_use_template(self):
        self._insert_random_partners(1)
        response = self.client.get(reverse('partner_page', 1))
        self.assertTemplateUsed(response, 'core/partner_page.html')

    def test_contains_partners_name(self):
        partner = self._insert_random_partners(1)
        self._assert_partner_page_contains(1, '<h1>{}'.format(partner.website))

    def test_contains_partners_description(self):
        partner = self._insert_random_partners(1)
        self._assert_partner_page_contains(1, '<p>{}</p>'.format(partner.description))

    def test_contains_partners_website(self):
        partner = self._insert_random_partners(1)
        self._assert_partner_page_contains(1, '<a href="{}"'.format(partner.website))

    def test_contains_link_to_partners_list(self):
        self._insert_random_partners(1)
        self._assert_partner_page_contains(1, '<a href="{}"'.format(reverse('partners_page')))
