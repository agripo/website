import logging
from django.conf import settings

from core.exceptions import NoAutoConnectionOnProductionServer, NoAutoConnectionWithExistingUser
from core.models.users import AgripoUser as User

logger = logging.getLogger(__name__)

REAL_SERVER_TYPE = settings.SERVER_TYPE
USED_SERVER_TYPE = settings.SERVER_TYPE


def force_production_server(status=True):
    global USED_SERVER_TYPE
    if status:
        USED_SERVER_TYPE = settings.SERVER_TYPE_PRODUCTION
    else:
        USED_SERVER_TYPE = REAL_SERVER_TYPE


def is_production_server():
    global USED_SERVER_TYPE
    return USED_SERVER_TYPE == settings.SERVER_TYPE_PRODUCTION


def is_development_server():
    global USED_SERVER_TYPE
    return USED_SERVER_TYPE == settings.SERVER_TYPE_DEVELOPMENT


def is_staging_server():
    global USED_SERVER_TYPE
    return USED_SERVER_TYPE == settings.SERVER_TYPE_STAGING


def get_username_from_email(email):
    return email.replace("@", " ")


class NewUserAutoconnectionModelBackend(object):

    def authenticate(self, email):
        username = get_username_from_email(email)
        if is_production_server():
            raise NoAutoConnectionOnProductionServer

        try:
            # We raise an error if the user exists, as a
            # protection
            User.objects.get(email=email)
            raise NoAutoConnectionWithExistingUser
        except User.DoesNotExist:
            pass

        user = User.objects.create(
            username=username, password="auto_password",
            email=email)
        return user

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
