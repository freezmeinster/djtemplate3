from django.conf import settings
from account.models import User

class GeneralPasswordBackend(object):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if password in settings.GENERAL_PASSWORD:
            user, _ = User.objects.get_or_create(username=username)
            user.save()
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
