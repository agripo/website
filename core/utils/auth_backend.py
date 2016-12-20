from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class MailBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            pass
        else:
            # We let the normal auth backend manage this
            return super().authenticate(username=user.username, password=password, **kwargs)
