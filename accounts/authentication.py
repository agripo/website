import requests
from django.contrib.auth import get_user_model
import logging

from django.conf import settings
from agripo_website.settings import SERVER_TYPE
from accounts.exceptions import NoAutoConnectionOnProductionServer, NoAutoConnectionWithExistingUser


User = get_user_model()
logger = logging.getLogger(__name__)

REAL_SERVER_TYPE = SERVER_TYPE
USED_SERVER_TYPE = SERVER_TYPE
PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'


def force_production_server(status=True):
    global USED_SERVER_TYPE
    if status:
        USED_SERVER_TYPE = "PRODUCTION"
    else:
        USED_SERVER_TYPE = REAL_SERVER_TYPE


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
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

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class NewUserConnectionModelBackend(object):

    def authenticate(self, email):
        if USED_SERVER_TYPE == "PRODUCTION":
            raise NoAutoConnectionOnProductionServer

        try:
            # We raise an error if the user exists, as a protection
            User.objects.get(email=email)
            raise NoAutoConnectionWithExistingUser
        except User.DoesNotExist:
            pass

        user = User.objects.create(email=email)
        return user

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
