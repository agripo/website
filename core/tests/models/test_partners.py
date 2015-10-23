from unittest.mock import Mock
from core.exceptions import AddedMoreToCartThanAvailable
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from core.tests.base import CoreTestCase
from core.models.partners import Partner


class DeliveryModelTest(CoreTestCase):

    def _get_one_partner_full_data(self, name="One partner"):
        description = "Some description for partner {}".format(name)
        website = name.replace(" ", "_")
        return dict(name=name, description=description, website=website)

    def create_partner(self, name="One partner"):
        return Partner.objects.create(**self._get_one_partner_full_data(name=name))

    def test_has_an_explicit__str__(self):
        partner = self.create_partner(name="Point")
        self.assertNotEquals(partner.__str__(), 'Partner object')

    def test_requires_name(self):
        fields = self._get_one_partner_full_data()
        fields.pop("name")
        partner = Partner(**fields)
        self.assertRaises(IntegrityError, partner.save)

    def test_name_is_unique(self):
        fields = self._get_one_partner_full_data()
        Partner.objects.create(**fields)
        partner2 = Partner(**fields)
        self.assertRaises(IntegrityError, partner2.save)

    def test_requires_description(self):
        fields = self._get_one_partner_full_data()
        fields.pop("description")
        partner = Partner(**fields)
        self.assertRaises(IntegrityError, partner.save)

    def test_requires_website(self):
        fields = self._get_one_partner_full_data()
        fields.pop("website")
        partner = Partner(**fields)
        self.assertRaises(IntegrityError, partner.save)

    def test_requires_valid_website(self):
        fields = self._get_one_partner_full_data()
        fields['website'] = "#Not a domain name"
        partner = Partner(**fields)
        self.assertRaises(ValidationError, partner.full_clean)
