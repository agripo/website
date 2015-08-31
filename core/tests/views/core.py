from django.test import TestCase
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

from core.authentication import force_production_server
from core.models import SiteConfiguration


config = SiteConfiguration.objects.get()
NUMBER_OF_NEWS_BY_PAGE = config.news_count


class CoreTestCase(TestCase):

    def setUp(self):
        # We add a SocialApp as we get an error if it's not done
        app = SocialApp(pk=1, provider="facebook", name="Facebook", client_id="001122334455667",
                        secret="00112233445566778899aabbccddeeff")
        app.sites.add(Site.objects.get_current().id)
        app.save()

    def tearDown(self):
        # We reset the session to the default (dev/staging/prod) server
        force_production_server(False)

    def auto_connect(self, email):
        return self.client.get('/core/auto_login/{}'.format(email))

    def auto_manager_connect(self, email):
        return self.client.get('/core/auto_manager_login/{}'.format(email))
