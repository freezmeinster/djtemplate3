from base64 import b64encode
from django.conf import settings
from account.models import User
import requests

class ApiAuthBackend(object):

    # Please modify this URL accordingly
    AUTH_URL = getattr(settings, "API_AUTH_URL", "https://auth.example/account/validate")

    def _run_login(self,username, password):
        payload = {"account": username, "privatekey": password}
        res = requests.post(self.AUTH_URL, data=payload)
        if res.json().get("login", "0") == "1":
            return True
        else:
            return False
   
    def authenticate(self, request, username=None, password=None, **kwargs):
        if self._run_login(username, password):
            user, _ = User.objects.get_or_create(username=username)
            new_token = b64encode(password.encode("utf-8"))
            user.token = new_token
            user.save()
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
