from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD,
                                  kwargs.get(UserModel.EMAIL_FIELD))
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(
                Q(username__exact=username) |
                (Q(email__iexact=username) &
                 Q(email_verified=True))
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if (
                user.check_password(password) and
                self.user_can_authenticate(user)
            ):
                return user
