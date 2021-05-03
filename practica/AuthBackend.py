from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

model = get_user_model()


class UsernameAuthBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = model.objects.get(username=username)
            if user.check_password(password):
                return user
        except model.DoesNotExist:
            model().set_password(password)

    def get_user(self, user_id):
        try:
            return model.objects.get(pk=user_id)
        except model.DoesNotExist:
            return None
