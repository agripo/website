import requests
from django.contrib.auth import get_user_model
import logging

from django.conf import settings


User = get_user_model()
logger = logging.getLogger(__name__)

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'


class PersonaAuthenticationBackend(object):

    @staticmethod
    def authenticate(assertion):
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': settings.DOMAIN}
        )
        
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)
        else:
            logger.warning(
                'Persona says no. Json was: {}'.format(response.json())
            )

    @staticmethod
    def get_user(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
